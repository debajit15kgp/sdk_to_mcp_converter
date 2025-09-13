#!/usr/bin/env python3
"""
Test script for Azure SDK to MCP conversion.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from converter import SDKToMCPConverter, ConversionConfig


def test_azure_resource_conversion():
    """Test converting Azure Resource Management SDK to MCP server."""
    print("🧪 Testing Azure Resource Management SDK conversion...")
    
    # Check if Azure SDK is installed
    try:
        import azure.identity
        import azure.mgmt.resource
        print("✅ Azure SDK is installed")
    except ImportError:
        print("❌ Azure SDK not installed. Install with: pip install azure-identity azure-mgmt-resource")
        return False
    
    # Create configuration
    config = ConversionConfig(
        sdk_name="azure",
        sdk_module="azure.mgmt.resource",
        output_dir="./test-output/azure-mcp-server",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        include_private_methods=False,
        max_methods_per_tool=30,
        generate_tests=True
    )
    
    try:
        # Create converter and run conversion
        converter = SDKToMCPConverter(config)
        result = converter.convert()
        
        print(f"✅ Azure conversion successful!")
        print(f"📁 Output: {config.output_dir}")
        print(f"🔧 Methods: {result['methods_discovered']}")
        print(f"🛠️  Tools: {result['tools_generated']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Azure conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_azure_identity_conversion():
    """Test converting Azure Identity SDK to MCP server."""
    print("\n🧪 Testing Azure Identity SDK conversion...")
    
    # Check if Azure Identity SDK is installed
    try:
        import azure.identity
        print("✅ Azure Identity SDK is installed")
    except ImportError:
        print("❌ Azure Identity SDK not installed. Install with: pip install azure-identity")
        return False
    
    # Create configuration
    config = ConversionConfig(
        sdk_name="azure",
        sdk_module="azure.identity",
        output_dir="./test-output/azure-identity-mcp-server",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        include_private_methods=False,
        max_methods_per_tool=20,
        generate_tests=True
    )
    
    try:
        # Create converter and run conversion
        converter = SDKToMCPConverter(config)
        result = converter.convert()
        
        print(f"✅ Azure Identity conversion successful!")
        print(f"📁 Output: {config.output_dir}")
        print(f"🔧 Methods: {result['methods_discovered']}")
        print(f"🛠️  Tools: {result['tools_generated']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Azure Identity conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run Azure SDK conversion tests."""
    print("🚀 Azure SDK to MCP Converter - Test Suite")
    print("=" * 50)
    
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: No OPENAI_API_KEY found. LLM analysis will be limited.")
        print("   Set OPENAI_API_KEY environment variable for full functionality.")
    
    # Create output directory
    Path("./test-output").mkdir(exist_ok=True)
    
    # Run tests
    results = []
    
    # Test Azure Resource Management conversion
    results.append(test_azure_resource_conversion())
    
    # Test Azure Identity conversion
    results.append(test_azure_identity_conversion())
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Azure Test Results Summary:")
    successful = sum(results)
    total = len(results)
    
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    if successful == total:
        print("\n🎉 All Azure tests passed!")
        print("\n📁 Generated Azure MCP servers are in ./test-output/")
        print("🚀 You can now run the generated servers:")
        print("   cd ./test-output/azure-mcp-server && python mcp_server.py")
        print("   cd ./test-output/azure-identity-mcp-server && python mcp_server.py")
    else:
        print("\n⚠️  Some Azure tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
