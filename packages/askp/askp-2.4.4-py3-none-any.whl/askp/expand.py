#!/usr/bin/env python3
"""
Query expansion module for ASKP CLI.
Contains functions to expand queries into related ones.
"""

import json
from typing import List, Dict, Any
from openai import OpenAI
from rich import print as rprint

from .utils import load_api_key


def generate_expanded_queries(
    original_queries: List[str], 
    total_queries: int,
    model: str = "sonar-pro",
    temperature: float = 0.7
) -> List[str]:
    """
    Generate additional related queries based on the original queries.
    
    Args:
        original_queries: List of original queries
        total_queries: Total number of queries desired (including original)
        model: Model to use for generating additional queries
        temperature: Temperature for query generation
        
    Returns:
        List of all queries (original + new)
    """
    if total_queries <= len(original_queries):
        return original_queries
    
    # Number of new queries to generate
    num_new_queries = total_queries - len(original_queries)
    
    try:
        # Load API key
        api_key = load_api_key()
        client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
        
        # Create the prompt for generating additional queries
        prompt = _create_expansion_prompt(original_queries, num_new_queries)
        
        # Make API call
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=1024
        )
        
        # Parse the response
        content = response.choices[0].message.content
        try:
            # Try to extract JSON from the response text
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                result = json.loads(json_str)
                new_queries = result.get("queries", [])
            else:
                # Fallback: try to parse lines that look like queries
                lines = content.split('\n')
                new_queries = []
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('"') or line.startswith('-') or line.startswith('*')):
                        # Clean up the line
                        query = line.lstrip('-*"\' ').rstrip('",\' ')
                        if query:
                            new_queries.append(query)
            
            # Validate and clean up new queries
            valid_new_queries = []
            for query in new_queries:
                if isinstance(query, str) and query.strip() and query not in original_queries:
                    valid_new_queries.append(query.strip())
            
            # Ensure we don't exceed the requested total
            valid_new_queries = valid_new_queries[:num_new_queries]
            
            # Combine original and new queries
            all_queries = original_queries + valid_new_queries
            
            if valid_new_queries:
                rprint(f"Generated {len(valid_new_queries)} additional queries.")
            else:
                rprint("Warning: Could not generate additional queries. Using original queries.")
            
            return all_queries
            
        except json.JSONDecodeError:
            rprint("Warning: Could not parse expanded queries response as JSON. Using original queries.")
            return original_queries
            
    except Exception as e:
        rprint(f"Warning: Failed to expand queries: {e}. Using original queries.")
        return original_queries


def _create_expansion_prompt(original_queries: List[str], num_new_queries: int) -> str:
    """
    Create a prompt for generating additional related queries.
    
    Args:
        original_queries: List of original queries
        num_new_queries: Number of new queries to generate
        
    Returns:
        Prompt string
    """
    queries_str = "\n".join([f"- {q}" for q in original_queries])
    
    prompt = f"""Given the following research queries:

{queries_str}

Generate {num_new_queries} additional, diverse queries that will complement these and help the user get to a solution to their problem or a more comprehensive understanding of the topic.

The new queries should:
1. First, focus on providing a more comprehensive understanding of this topic
2. Identify specific solutions to and around the problem
3. Consider time-sensitive aspects (recent updates, changes, or developments)
4. Take into account that technical solutions may require up-to-date information (e.g., coding solutions from a few years ago may be outdated)
5. Cover different aspects not addressed in the original queries
6. Fill knowledge gaps in the original set
7. Be specific and focused
8. Be directly related to the overall research topic
9. Not duplicate information in the original queries
10. Drive toward practical, actionable solutions when applicable

Return your response as a JSON object with a single key "queries" containing an array of strings.
Example format:
{{
  "queries": [
    "First additional query",
    "Second additional query",
    ...
  ]
}}
"""
    return prompt
