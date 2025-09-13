#!/usr/bin/env python3
"""
Example script demonstrating the SDK to MCP converter.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from converter import SDKToMCPConverter, ConversionConfig


def test_github_conversion():
    """Test converting PyGithub SDK to MCP server."""
    print("🧪 Testing GitHub SDK conversion...")
    
    # Check if PyGithub is installed
    try:
        import github
        print("✅ PyGithub is installed")
    except ImportError:
        print("❌ PyGithub not installed. Install with: pip install PyGithub")
        return False
    
    # Create configuration
    config = ConversionConfig(
        sdk_name="github",
        sdk_module="github",
        output_dir="./test-output/github-mcp-server",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        include_private_methods=False,
        max_methods_per_tool=20,
        generate_tests=True
    )
    
    try:
        # Create converter and run conversion
        converter = SDKToMCPConverter(config)
        result = converter.convert()
        
        print(f"✅ GitHub conversion successful!")
        print(f"📁 Output: {config.output_dir}")
        print(f"🔧 Methods: {result['methods_discovered']}")
        print(f"🛠️  Tools: {result['tools_generated']}")
        
        return True
        
    except Exception as e:
        print(f"❌ GitHub conversion failed: {e}")
        return False


def test_kubernetes_conversion():
    """Test converting Kubernetes SDK to MCP server."""
    print("\n🧪 Testing Kubernetes SDK conversion...")
    
    # Check if Kubernetes is installed
    try:
        import kubernetes
        print("✅ Kubernetes SDK is installed")
    except ImportError:
        print("❌ Kubernetes SDK not installed. Install with: pip install kubernetes")
        return False
    
    # Create configuration
    config = ConversionConfig(
        sdk_name="kubernetes",
        sdk_module="kubernetes.client",
        output_dir="./test-output/kubernetes-mcp-server",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        include_private_methods=False,
        max_methods_per_tool=15,
        generate_tests=True
    )
    
    try:
        # Create converter and run conversion
        converter = SDKToMCPConverter(config)
        result = converter.convert()
        
        print(f"✅ Kubernetes conversion successful!")
        print(f"📁 Output: {config.output_dir}")
        print(f"🔧 Methods: {result['methods_discovered']}")
        print(f"🛠️  Tools: {result['tools_generated']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Kubernetes conversion failed: {e}")
        return False


def test_azure_conversion():
    """Test converting Azure SDK to MCP server."""
    print("\n🧪 Testing Azure SDK conversion...")
    
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
        max_methods_per_tool=25,
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
        return False


def main():
    """Run all conversion tests."""
    print("🚀 SDK to MCP Converter - Test Suite")
    print("=" * 50)
    
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: No OPENAI_API_KEY found. LLM analysis will be limited.")
        print("   Set OPENAI_API_KEY environment variable for full functionality.")
    
    # Create output directory
    Path("./test-output").mkdir(exist_ok=True)
    
    # Run tests
    results = []
    
    # Test GitHub conversion
    results.append(test_github_conversion())
    
    # Test Kubernetes conversion
    results.append(test_kubernetes_conversion())
    
    # Test Azure conversion
    results.append(test_azure_conversion())
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    successful = sum(results)
    total = len(results)
    
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    if successful == total:
        print("\n🎉 All tests passed!")
        print("\n📁 Generated MCP servers are in ./test-output/")
        print("🚀 You can now run the generated servers:")
        print("   cd ./test-output/github-mcp-server && python mcp_server.py")
        print("   cd ./test-output/kubernetes-mcp-server && python mcp_server.py")
        print("   cd ./test-output/azure-mcp-server && python mcp_server.py")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
