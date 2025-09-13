"""
LLM Client for OpenAI API integration.
"""

import json
import openai
from typing import Dict, List, Any, Optional
import time


class LLMClient:
    """
    Client for interacting with OpenAI's API to analyze SDK methods and generate descriptions.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize the LLM client.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment.
            model: OpenAI model to use for analysis.
        """
        self.api_key = api_key or self._get_api_key()
        self.model = model
        
        if not self.api_key:
            print("Warning: No OpenAI API key provided. Using fallback analysis.")
            self.client = None
        else:
            # Initialize OpenAI client
            openai.api_key = self.api_key
            self.client = openai.OpenAI(api_key=self.api_key)
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment variables."""
        import os
        return os.getenv("OPENAI_API_KEY")
    
    def analyze_methods(self, prompt: str, max_retries: int = 3) -> str:
        """
        Analyze SDK methods using OpenAI API.
        
        Args:
            prompt: The analysis prompt
            max_retries: Maximum number of retry attempts
            
        Returns:
            LLM response as string
        """
        if not self.client:
            # Fallback analysis without LLM
            return self._fallback_analysis(prompt)
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert Python developer who specializes in analyzing SDK APIs and creating MCP (Model Context Protocol) server interfaces. You understand the purpose of different SDK methods and can categorize them appropriately for AI assistant integration."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1,  # Low temperature for consistent analysis
                    max_tokens=4000
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"LLM analysis failed, using fallback: {e}")
                    return self._fallback_analysis(prompt)
    
    def _fallback_analysis(self, prompt: str) -> str:
        """
        Fallback analysis when LLM is not available.
        Creates basic tool definitions based on method names.
        """
        # Extract method names from the prompt
        import re
        
        # Simple regex to find method names in the prompt
        method_pattern = r'(\w+)\('
        methods = re.findall(method_pattern, prompt)
        
        tools = []
        for method in methods:
            if not method.startswith('_') and method not in ['Methods', 'methods']:
                tools.append({
                    "name": method,
                    "description": f"Execute {method} operation",
                    "parameters": [],
                    "return_description": "Operation result"
                })
        
        return json.dumps({
            "tools": tools,
            "resources": []
        })
    
    def generate_mcp_tool_description(self, method_info: Dict[str, Any]) -> str:
        """
        Generate a description for an MCP tool based on method information.
        
        Args:
            method_info: Dictionary containing method information
            
        Returns:
            Generated description string
        """
        prompt = f"""
Generate a clear, concise description for an MCP tool based on this method:

Method: {method_info.get('name', 'unknown')}
Class: {method_info.get('class_name', 'standalone')}
Docstring: {method_info.get('docstring', 'No documentation available')}
Parameters: {method_info.get('parameters', [])}

The description should:
1. Be clear and concise (1-2 sentences)
2. Explain what the method does
3. Mention key parameters if important
4. Be suitable for an AI assistant to understand when to use this tool

Return only the description text, no additional formatting.
"""
        
        try:
            response = self.analyze_methods(prompt)
            return response.strip()
        except Exception as e:
            print(f"Warning: Could not generate description for {method_info.get('name')}: {e}")
            return f"Execute {method_info.get('name', 'method')} operation"
    
    def categorize_methods(self, methods: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Categorize methods into groups based on their functionality.
        
        Args:
            methods: List of method information dictionaries
            
        Returns:
            Dictionary with categories as keys and method lists as values
        """
        prompt = f"""
Categorize the following SDK methods into logical groups:

Methods:
{chr(10).join([f"- {method.get('name', 'unknown')}: {method.get('docstring', 'No description')[:100]}" for method in methods])}

Group them by functionality (e.g., "Authentication", "Data Retrieval", "Data Modification", "Configuration", etc.).

Return your response as JSON in this format:
{{
    "categories": {{
        "Category Name": [
            {{
                "name": "method_name",
                "reason": "Why this method belongs in this category"
            }}
        ]
    }}
}}
"""
        
        try:
            response = self.analyze_methods(prompt)
            parsed = json.loads(response)
            return parsed.get("categories", {})
        except Exception as e:
            print(f"Warning: Could not categorize methods: {e}")
            # Fallback: put all methods in a single category
            return {"General": [{"name": method.get("name", "unknown"), "reason": "General purpose"} for method in methods]}
    
    def generate_parameter_descriptions(self, method_info: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate descriptions for method parameters.
        
        Args:
            method_info: Dictionary containing method information
            
        Returns:
            List of parameter descriptions
        """
        parameters = method_info.get("parameters", [])
        if not parameters:
            return []
        
        param_names = [p["name"] for p in parameters]
        prompt = f"""
Generate clear descriptions for these method parameters:

Method: {method_info.get('name', 'unknown')}
Parameters: {param_names}
Method docstring: {method_info.get('docstring', 'No documentation')}

For each parameter, provide:
1. A clear description of what it represents
2. The expected data type or format
3. Whether it's required or optional
4. Any important constraints or examples

Return as JSON:
{{
    "parameters": [
        {{
            "name": "param_name",
            "description": "Clear description",
            "type": "Expected type",
            "required": true/false,
            "constraints": "Any constraints or examples"
        }}
    ]
}}
"""
        
        try:
            response = self.analyze_methods(prompt)
            parsed = json.loads(response)
            return parsed.get("parameters", [])
        except Exception as e:
            print(f"Warning: Could not generate parameter descriptions: {e}")
            # Fallback: basic descriptions
            return [
                {
                    "name": p["name"],
                    "description": f"Parameter {p['name']}",
                    "type": p.get("annotation", "unknown"),
                    "required": p.get("default") is None,
                    "constraints": "No constraints specified"
                }
                for p in parameters
            ]
    
    def suggest_mcp_tool_grouping(self, methods: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Suggest how to group methods into MCP tools for better organization.
        
        Args:
            methods: List of method information dictionaries
            
        Returns:
            Dictionary with grouping suggestions
        """
        prompt = f"""
Analyze these SDK methods and suggest how to group them into MCP tools for optimal AI assistant usage:

Methods:
{chr(10).join([f"- {method.get('name', 'unknown')} ({method.get('class_name', 'standalone')}): {method.get('docstring', 'No description')[:150]}" for method in methods])}

Consider:
1. Logical grouping by functionality
2. Common use cases and workflows
3. Parameter similarity
4. Return value types
5. Dependencies between methods

Return as JSON:
{{
    "tool_groups": [
        {{
            "name": "tool_group_name",
            "description": "What this group does",
            "methods": ["method1", "method2"],
            "rationale": "Why these methods are grouped together"
        }}
    ],
    "standalone_tools": [
        {{
            "name": "method_name",
            "description": "Why this should be standalone"
        }}
    ]
}}
"""
        
        try:
            response = self.analyze_methods(prompt)
            return json.loads(response)
        except Exception as e:
            print(f"Warning: Could not generate tool grouping suggestions: {e}")
            return {
                "tool_groups": [],
                "standalone_tools": [{"name": method.get("name", "unknown"), "description": "Standalone method"} for method in methods]
            }
