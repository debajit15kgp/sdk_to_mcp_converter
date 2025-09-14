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
    """Test converting comprehensive Azure SDK to MCP server."""
    print("\n🧪 Testing Comprehensive Azure SDK conversion...")
    
    # Check if Azure SDK modules are installed
    azure_modules = [
        "azure.mgmt.resource",
        "azure.mgmt.compute",
        "azure.mgmt.storage", 
        "azure.mgmt.network",
        "azure.mgmt.sql",
        "azure.mgmt.web",
        "azure.mgmt.containerservice",
        "azure.mgmt.keyvault",
        "azure.mgmt.monitor",
        "azure.mgmt.cosmosdb",
        "azure.mgmt.redis",
        "azure.mgmt.search",
        "azure.mgmt.cognitiveservices",
        "azure.mgmt.datafactory",
        "azure.mgmt.eventhub",
        "azure.mgmt.servicebus",
        "azure.mgmt.cdn",
        "azure.mgmt.dns",
        "azure.mgmt.security",
        "azure.mgmt.authorization"
    ]
    
    installed_modules = []
    missing_modules = []
    
    for module in azure_modules:
        try:
            __import__(module)
            installed_modules.append(module)
        except ImportError:
            missing_modules.append(module)
    
    print(f"✅ Azure modules installed: {len(installed_modules)}")
    if missing_modules:
        print(f"⚠️  Missing modules: {len(missing_modules)}")
        print(f"   Install with: pip install {' '.join([m.replace('azure.mgmt.', 'azure-mgmt-') for m in missing_modules if 'mgmt' in m])}")
    
    # Convert the most comprehensive Azure module (Resource Management)
    # This module includes many sub-modules and will give us the most coverage
    config = ConversionConfig(
        sdk_name="azure-comprehensive",
        sdk_module="azure.mgmt.resource",  # Start with resource management
        output_dir="./test-output/azure-comprehensive-mcp-server",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        include_private_methods=False,
        max_methods_per_tool=100,  # Increased for comprehensive coverage
        generate_tests=True
    )
    
    try:
        # Create converter and run conversion
        converter = SDKToMCPConverter(config)
        result = converter.convert()
        
        print(f"✅ Azure comprehensive conversion successful!")
        print(f"📁 Output: {config.output_dir}")
        print(f"🔧 Methods: {result['methods_discovered']}")
        print(f"🛠️  Tools: {result['tools_generated']}")
        print(f"📊 Coverage: {len(installed_modules)} Azure modules available")
        
        return True
        
    except Exception as e:
        print(f"❌ Azure conversion failed: {e}")
        return False


def test_azure_multiple_modules():
    """Test converting multiple Azure modules individually."""
    print("\n🧪 Testing Multiple Azure Modules conversion...")
    
    # Define Azure modules to convert (comprehensive list)
    azure_configs = [
        {
            "name": "azure-compute",
            "module": "azure.mgmt.compute",
            "description": "Virtual machines, VM scalesets, disks, snapshots"
        },
        {
            "name": "azure-storage", 
            "module": "azure.mgmt.storage",
            "description": "Storage accounts, blobs, files, queues"
        },
        {
            "name": "azure-network",
            "module": "azure.mgmt.network", 
            "description": "Virtual networks, load balancers, security groups"
        },
        {
            "name": "azure-containerservice",
            "module": "azure.mgmt.containerservice",
            "description": "Kubernetes clusters, container registries"
        },
        {
            "name": "azure-keyvault",
            "module": "azure.mgmt.keyvault",
            "description": "Key vaults, secrets, certificates, keys"
        },
        {
            "name": "azure-monitor",
            "module": "azure.mgmt.monitor",
            "description": "Monitoring, metrics, alerts, diagnostic settings"
        },
        {
            "name": "azure-cosmosdb",
            "module": "azure.mgmt.cosmosdb",
            "description": "Cosmos DB databases, containers, throughput"
        },
        {
            "name": "azure-sql",
            "module": "azure.mgmt.sql",
            "description": "SQL databases, servers, elastic pools"
        },
        {
            "name": "azure-web",
            "module": "azure.mgmt.web",
            "description": "Web apps, App Service plans, functions"
        },
        {
            "name": "azure-redis",
            "module": "azure.mgmt.redis",
            "description": "Redis caches, firewall rules, patches"
        },
        {
            "name": "azure-search",
            "module": "azure.mgmt.search",
            "description": "Search services, indexes, data sources"
        },
        {
            "name": "azure-cognitiveservices",
            "module": "azure.mgmt.cognitiveservices",
            "description": "Cognitive Services accounts, deployments"
        },
        {
            "name": "azure-datafactory",
            "module": "azure.mgmt.datafactory",
            "description": "Data Factory pipelines, datasets, linked services"
        },
        {
            "name": "azure-eventhub",
            "module": "azure.mgmt.eventhub",
            "description": "Event Hubs namespaces, hubs, consumer groups"
        },
        {
            "name": "azure-servicebus",
            "module": "azure.mgmt.servicebus",
            "description": "Service Bus namespaces, queues, topics"
        },
        {
            "name": "azure-cdn",
            "module": "azure.mgmt.cdn",
            "description": "CDN profiles, endpoints, custom domains"
        },
        {
            "name": "azure-dns",
            "module": "azure.mgmt.dns",
            "description": "DNS zones, records, virtual network links"
        },
        {
            "name": "azure-security",
            "module": "azure.mgmt.security",
            "description": "Security Center assessments, recommendations"
        },
        {
            "name": "azure-authorization",
            "module": "azure.mgmt.authorization",
            "description": "Role assignments, definitions, permissions"
        }
    ]
    
    results = []
    total_methods = 0
    total_tools = 0
    
    for config_info in azure_configs:
        print(f"\n🔄 Converting {config_info['name']} - {config_info['description']}")
        
        try:
            # Check if module is available
            __import__(config_info['module'])
            
            config = ConversionConfig(
                sdk_name=config_info['name'],
                sdk_module=config_info['module'],
                output_dir=f"./test-output/{config_info['name']}-mcp-server",
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                include_private_methods=False,
                max_methods_per_tool=50,
                generate_tests=True
            )
            
            converter = SDKToMCPConverter(config)
            result = converter.convert()
            
            methods = result['methods_discovered']
            tools = result['tools_generated']
            total_methods += methods
            total_tools += tools
            
            print(f"✅ {config_info['name']}: {methods} methods, {tools} tools")
            results.append(True)
            
        except ImportError:
            print(f"⚠️  {config_info['name']}: Module not installed")
            results.append(False)
        except Exception as e:
            print(f"❌ {config_info['name']}: Failed - {e}")
            results.append(False)
    
    successful = sum(results)
    print(f"\n📊 Azure Multi-Module Results:")
    print(f"✅ Successful: {successful}/{len(azure_configs)}")
    print(f"🔧 Total Methods: {total_methods}")
    print(f"🛠️  Total Tools: {total_tools}")
    
    return successful > 0


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
    # results.append(test_github_conversion())
    
    # Test Kubernetes conversion
    # results.append(test_kubernetes_conversion())
    
    # Test comprehensive Azure conversion
    results.append(test_azure_conversion())
    
    # Test multiple Azure modules for comprehensive coverage
    results.append(test_azure_multiple_modules())
    
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
