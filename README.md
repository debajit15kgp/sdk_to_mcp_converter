# SDK to MCP Converter

A Python tool that automatically converts Python SDKs into MCP (Model Context Protocol) servers, enabling AI assistants to interact with any Python SDK through a standardized interface.

## 🚀 Quick Start

### Prerequisites

```bash
# Install required packages
pip install -r requirements.txt

# Set your OpenAI API key (for LLM analysis)
export OPENAI_API_KEY="sk-proj-your-key-here"
```

### Basic Usage

```bash
# Run the converter with example.py
python example.py
```

This will convert the Kubernetes SDK to an MCP server with 1,900+ tools and 400+ resources.

## 📁 Project Structure

```
sdk_to_mcp_converter/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── example.py                   # Main example script to run conversions
├── cli.py                       # Command-line interface
├── converter.py                 # Core conversion logic
├── generator.py                 # MCP server code generation
├── introspector.py              # SDK introspection and analysis
├── llm_client.py                # OpenAI API integration
├── debug_introspection.py       # Debug utilities
│
├── test-output/                 # Generated MCP servers
│   ├── kubernetes-mcp-server/   # Kubernetes MCP server
│   │   ├── mcp_server.py        # Main server (73K+ lines)
│   │   ├── example_usage.py     # Usage examples
│   │   ├── README.md            # Generated documentation
│   │   ├── requirements.txt     # Dependencies
│   │   ├── config.json          # Configuration
│   │   └── tests/               # Test files
│   │
│   └── github-mcp-server/       # GitHub MCP server
│       ├── mcp_server.py        # Main server
│       ├── example_usage.py     # Usage examples
│       ├── README.md            # Generated documentation
│       └── requirements.txt     # Dependencies
│
└── docs/                        # Additional documentation
    ├── PROJECT_SUMMARY.md       # Project overview
    ├── AZURE_FUNCTIONS.md       # Azure-specific functions
    └── SDK_FUNCTIONS_ANALYSIS.md # SDK analysis results
```

## 🛠️ How to Use

### Method 1: Using example.py (Recommended)

The `example.py` script provides a simple way to convert SDKs:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-proj-your-key-here"

# Run the converter
python example.py
```

**What it does:**
- Converts Kubernetes SDK → MCP server with 1,900+ tools
- Converts Azure SDK → MCP server  
- Generates complete servers in `./test-output/`

### Method 2: Using cli.py (Advanced)

For command-line usage:

```bash
python cli.py convert \
  --sdk-name kubernetes \
  --sdk-module kubernetes.client \
  --output-dir ./my-k8s-server \
  --openai-api-key $OPENAI_API_KEY
```

## 🔧 Configuration Options

### Basic Configuration

```python
from converter import SDKToMCPConverter, ConversionConfig

config = ConversionConfig(
    sdk_name="kubernetes",                    # SDK name
    sdk_module="kubernetes.client",           # Module to analyze
    output_dir="./my-server",                 # Output directory
    openai_api_key=os.getenv("OPENAI_API_KEY"), # OpenAI API key
    include_private_methods=False,            # Include private methods
    max_methods_per_tool=15,                  # Methods per tool group
    generate_tests=True                       # Generate test files
)
```

### Advanced Options

```python
config = ConversionConfig(
    # ... basic options ...
    include_private_methods=True,             # Include _private methods
    max_methods_per_tool=50,                  # More methods per tool
    generate_tests=False,                     # Skip test generation
    custom_prompt="Your custom LLM prompt",   # Custom analysis prompt
    filter_methods=["test_", "debug_"],      # Exclude methods matching patterns
)
```

## 📊 Supported SDKs

### Tested & Working

| SDK | Module | Tools Generated | Status |
|-----|--------|----------------|--------|
| **Kubernetes** | `kubernetes.client` | 1,900+ | ✅ Working |
| **GitHub** | `github` | 50+ | ✅ Working |
| **Azure** | `azure.mgmt.resource` | 200+ | ✅ Working |

### How to Add New SDKs

1. Install the SDK:
   ```bash
   pip install your-sdk-package
   ```

2. Create a conversion config:
   ```python
   config = ConversionConfig(
       sdk_name="your-sdk",
       sdk_module="your.sdk.module",
       output_dir="./your-sdk-server",
       openai_api_key=os.getenv("OPENAI_API_KEY")
   )
   ```

3. Run the conversion:
   ```python
   converter = SDKToMCPConverter(config)
   result = converter.convert()
   ```

## 🚀 Running Generated Servers

After conversion, you'll have a complete MCP server:

```bash
# Navigate to generated server
cd test-output/kubernetes-mcp-server/

# Install dependencies
pip install -r requirements.txt

# Run the server
python mcp_server.py

# Or run examples
python example_usage.py
```

### Example Output

```
Executing: get_api_group
Result: {
  "status": "success", 
  "message": "get_api_group executed successfully"
}

Available resources: 419
```

## 🔐 Authentication Setup

### GitHub
```bash
export GITHUB_TOKEN="your-github-token"
```

### Kubernetes
```bash
# Option 1: Use existing kubeconfig
export KUBECONFIG=~/.kube/config

# Option 2: Set custom kubeconfig
export KUBECONFIG=/path/to/your/kubeconfig
```

### Azure
```bash
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Python SDK    │───▶│  SDK Introspector │───▶│   LLM Client    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Server    │◀───│   MCP Generator   │◀───│  Method Analysis│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Process Flow:**
1. **Introspection**: Discovers all classes, methods, and signatures
2. **LLM Analysis**: Uses OpenAI to understand method purposes
3. **Generation**: Creates complete MCP server code
4. **Documentation**: Generates README, examples, and tests

## 📈 Performance

| SDK | Methods Analyzed | Tools Generated | Generation Time |
|-----|------------------|-----------------|-----------------|
| Kubernetes | 3,147 | 1,909 | ~5-10 minutes |
| GitHub | 150 | 50+ | ~2-3 minutes |
| Azure | 500+ | 200+ | ~3-5 minutes |

*Times depend on OpenAI API response speed and network conditions.*

---

**Ready to get started?** Run `python example.py` to convert your first SDK! 🚀