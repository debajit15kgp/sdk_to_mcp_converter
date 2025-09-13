"""
Command-line interface for the SDK to MCP converter.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from .converter import SDKToMCPConverter, ConversionConfig


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert Python SDKs to MCP servers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert PyGithub SDK
  python -m sdk_to_mcp_converter github github --output-dir ./github-mcp-server

  # Convert Kubernetes SDK with OpenAI API key
  python -m sdk_to_mcp_converter kubernetes kubernetes --openai-api-key sk-... --output-dir ./k8s-mcp-server

  # Convert Azure SDK with custom settings
  python -m sdk_to_mcp_converter azure azure.mgmt.resource --include-private --max-methods 100 --output-dir ./azure-mcp-server

  # Convert Azure Identity SDK
  python -m sdk_to_mcp_converter azure azure.identity --output-dir ./azure-identity-mcp-server
        """
    )
    
    parser.add_argument(
        "sdk_name",
        help="Name of the SDK (e.g., github, kubernetes, azure)"
    )
    
    parser.add_argument(
        "sdk_module",
        help="Python module name of the SDK (e.g., github, kubernetes, azure.identity)"
    )
    
    parser.add_argument(
        "--output-dir",
        "-o",
        default="./mcp-server-output",
        help="Output directory for generated MCP server (default: ./mcp-server-output)"
    )
    
    parser.add_argument(
        "--openai-api-key",
        help="OpenAI API key for LLM analysis (or set OPENAI_API_KEY env var)"
    )
    
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include private methods (starting with _)"
    )
    
    parser.add_argument(
        "--max-methods",
        type=int,
        default=50,
        help="Maximum number of methods per tool (default: 50)"
    )
    
    parser.add_argument(
        "--no-tests",
        action="store_true",
        help="Skip generating test files"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Get OpenAI API key
    openai_api_key = args.openai_api_key or os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Warning: No OpenAI API key provided. LLM analysis will be limited.")
        print("Set OPENAI_API_KEY environment variable or use --openai-api-key")
    
    # Create configuration
    config = ConversionConfig(
        sdk_name=args.sdk_name,
        sdk_module=args.sdk_module,
        output_dir=args.output_dir,
        openai_api_key=openai_api_key,
        include_private_methods=args.include_private,
        max_methods_per_tool=args.max_methods,
        generate_tests=not args.no_tests
    )
    
    # Create converter and run conversion
    try:
        converter = SDKToMCPConverter(config)
        result = converter.convert()
        
        print(f"\n✅ Conversion completed successfully!")
        print(f"📁 Output directory: {args.output_dir}")
        print(f"🔧 Methods discovered: {result['methods_discovered']}")
        print(f"🛠️  Tools generated: {result['tools_generated']}")
        print(f"📄 Files created: {len(result['output_files'])}")
        
        if args.verbose:
            print("\nGenerated files:")
            for file_path in result['output_files']:
                print(f"  - {file_path}")
        
        print(f"\n🚀 To run the MCP server:")
        print(f"  cd {args.output_dir}")
        print(f"  pip install -r requirements.txt")
        print(f"  python mcp_server.py")
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
