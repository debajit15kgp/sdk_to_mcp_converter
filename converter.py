"""
Core converter class that orchestrates the SDK to MCP conversion process.
"""

import os
import json
import importlib
import inspect
from typing import Dict, List, Any, Optional, Type, Callable
from dataclasses import dataclass
from pathlib import Path

from introspector import SDKIntrospector
from generator import MCPGenerator
from llm_client import LLMClient


@dataclass
class ConversionConfig:
    """Configuration for SDK to MCP conversion."""
    sdk_name: str
    sdk_module: str
    output_dir: str
    openai_api_key: Optional[str] = None
    include_private_methods: bool = False
    max_methods_per_tool: int = 50
    generate_tests: bool = True
    custom_mappings: Optional[Dict[str, str]] = None


class SDKToMCPConverter:
    """
    Main converter class that takes a Python SDK and generates an MCP server.
    
    This class orchestrates the entire conversion process:
    1. Introspects the SDK to discover available methods and classes
    2. Uses LLM to understand method purposes and generate descriptions
    3. Generates MCP server code with tools and resources
    4. Creates tests and documentation
    """
    
    def __init__(self, config: ConversionConfig):
        self.config = config
        self.introspector = SDKIntrospector()
        self.generator = MCPGenerator()
        self.llm_client = LLMClient(api_key=config.openai_api_key)
        
    def convert(self) -> Dict[str, Any]:
        """
        Main conversion method that orchestrates the entire process.
        
        Returns:
            Dict containing conversion results and metadata
        """
        print(f"Starting conversion of {self.config.sdk_name} SDK to MCP server...")
        
        # Step 1: Introspect the SDK
        print("Step 1: Introspecting SDK structure...")
        sdk_info = self.introspector.introspect_sdk(
            self.config.sdk_module,
            include_private=self.config.include_private_methods
        )
        
        # Step 2: Analyze methods with LLM
        print("Step 2: Analyzing methods with LLM...")
        analyzed_methods = self._analyze_methods_with_llm(sdk_info)
        
        # Step 3: Generate MCP server code
        print("Step 3: Generating MCP server code...")
        mcp_code = self.generator.generate_mcp_server(
            sdk_info,
            analyzed_methods,
            self.config
        )
        
        # Step 4: Write output files
        print("Step 4: Writing output files...")
        output_files = self._write_output_files(mcp_code)
        
        # Step 5: Generate tests if requested
        if self.config.generate_tests:
            print("Step 5: Generating tests...")
            test_files = self.generator.generate_tests(sdk_info, analyzed_methods)
            self._write_test_files(test_files)
        
        print(f"Conversion complete! Output written to {self.config.output_dir}")
        
        return {
            "sdk_name": self.config.sdk_name,
            "methods_discovered": len(sdk_info.get("methods", [])),
            "tools_generated": len(analyzed_methods.get("tools", [])),
            "output_files": output_files,
            "status": "success"
        }
    
    def _analyze_methods_with_llm(self, sdk_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use LLM to analyze SDK methods and generate descriptions and groupings.
        """
        methods = sdk_info.get("methods", [])
        classes = sdk_info.get("classes", [])
        
        # Group methods by class for better analysis
        method_groups = self._group_methods_by_class(methods, classes)
        
        analyzed_methods = {
            "tools": [],
            "resources": [],
            "descriptions": {}
        }
        
        for class_name, class_methods in method_groups.items():
            print(f"Analyzing {len(class_methods)} methods in {class_name}...")
            
            # Create analysis prompt for this class
            analysis_prompt = self._create_analysis_prompt(class_name, class_methods)
            
            # Get LLM analysis
            llm_response = self.llm_client.analyze_methods(analysis_prompt)
            
            # Parse LLM response and add to analyzed_methods
            self._parse_llm_response(llm_response, analyzed_methods, class_methods)
        
        return analyzed_methods
    
    def _group_methods_by_class(self, methods: List[Dict], classes: List[Dict]) -> Dict[str, List[Dict]]:
        """Group methods by their containing class."""
        groups = {}
        
        for method in methods:
            class_name = method.get("class_name", "standalone")
            if class_name not in groups:
                groups[class_name] = []
            groups[class_name].append(method)
        
        return groups
    
    def _create_analysis_prompt(self, class_name: str, methods: List[Dict]) -> str:
        """Create a prompt for LLM to analyze methods."""
        method_signatures = []
        for method in methods:
            parameters = method.get("parameters", [])
            param_names = []
            for param in parameters:
                if isinstance(param, dict):
                    param_names.append(param.get("name", "unknown"))
                else:
                    param_names.append(str(param))
            signature = f"{method['name']}({', '.join(param_names)})"
            method_signatures.append(signature)
        
        prompt = f"""
Analyze the following methods from the {class_name} class in a Python SDK:

Methods:
{chr(10).join(method_signatures)}

For each method, provide:
1. A clear description of what it does
2. Whether it should be exposed as an MCP tool (for actions) or resource (for data access)
3. Parameter descriptions and types
4. Return value description
5. Any important notes about usage

Format your response as JSON with this structure:
{{
    "tools": [
        {{
            "name": "method_name",
            "description": "Clear description",
            "parameters": [
                {{
                    "name": "param_name",
                    "type": "param_type",
                    "description": "param_description",
                    "required": true/false
                }}
            ],
            "return_description": "What this method returns"
        }}
    ],
    "resources": [
        {{
            "name": "resource_name",
            "description": "Resource description",
            "methods": ["method1", "method2"]
        }}
    ]
}}
"""
        return prompt
    
    def _parse_llm_response(self, response: str, analyzed_methods: Dict, methods: List[Dict]) -> None:
        """Parse LLM response and update analyzed_methods."""
        try:
            # Try to parse JSON response
            parsed = json.loads(response)
            
            # Add tools
            if "tools" in parsed:
                analyzed_methods["tools"].extend(parsed["tools"])
            
            # Add resources
            if "resources" in parsed:
                analyzed_methods["resources"].extend(parsed["resources"])
                
        except json.JSONDecodeError:
            print(f"Warning: Could not parse LLM response as JSON: {response[:200]}...")
            # Fallback: create basic tool entries for all methods
            for method in methods:
                analyzed_methods["tools"].append({
                    "name": method["name"],
                    "description": f"Execute {method['name']} method",
                    "parameters": method.get("parameters", []),
                    "return_description": "Method execution result"
                })
    
    def _write_output_files(self, mcp_code: Dict[str, str]) -> List[str]:
        """Write generated MCP server files to disk."""
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        written_files = []
        
        for filename, content in mcp_code.items():
            file_path = output_dir / filename
            with open(file_path, 'w') as f:
                f.write(content)
            written_files.append(str(file_path))
        
        return written_files
    
    def _write_test_files(self, test_files: Dict[str, str]) -> None:
        """Write generated test files to disk."""
        output_dir = Path(self.config.output_dir) / "tests"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for filename, content in test_files.items():
            file_path = output_dir / filename
            with open(file_path, 'w') as f:
                f.write(content)
