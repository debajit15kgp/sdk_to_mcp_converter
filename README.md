# SDK to MCP Converter

A Python library that automatically converts Python SDKs into MCP (Model Context Protocol) servers, enabling AI assistants to interact with any Python SDK through a standardized interface.

## Overview

The SDK to MCP Converter addresses a key limitation in current MCP implementations: while MCP servers expose core functionality, they often omit many useful methods that are available in rich Python SDKs. This converter bridges that gap by automatically generating comprehensive MCP servers from existing Python SDKs.

## Features

- 🔍 **Automatic SDK Introspection**: Discovers classes, methods, and their signatures
- 🤖 **LLM-Powered Analysis**: Uses OpenAI API to understand method purposes and generate descriptions
- 🛠️ **MCP Server Generation**: Creates complete MCP servers with tools and resources
- 🔐 **Authentication Handling**: Manages SDK-specific authentication requirements
- 📝 **Documentation Generation**: Creates README, examples, and configuration files
- 🧪 **Test Generation**: Generates comprehensive test suites
- 🎯 **Generalized Design**: Works with any Python SDK

## Supported SDKs

Currently tested with:
- **PyGithub** - GitHub API integration
- **Kubernetes** - Kubernetes cluster management  
- **Azure SDK** - Azure cloud services (Resource Management, Identity, etc.)

## Installation

```bash
pip install sdk-to-mcp-converter
```

Or install from source:
```bash
git clone https://github.com/your-username/sdk-to-mcp-converter
cd sdk-to-mcp-converter
pip install -e .
```

## Quick Start

### Basic Usage

```bash
# Convert PyGithub SDK to MCP server
sdk-to-mcp github github --output-dir ./github-mcp-server

# Convert Kubernetes SDK
sdk-to-mcp kubernetes kubernetes --output-dir ./k8s-mcp-server

# Convert Azure SDK
sdk-to-mcp azure azure.mgmt.resource --output-dir ./azure-mcp-server

# Convert Azure Identity SDK
sdk-to-mcp azure azure.identity --output-dir ./azure-identity-mcp-server
```

### With OpenAI API Key

```bash
# Set environment variable
export OPENAI_API_KEY="your-api-key-here"

# Or pass directly
sdk-to-mcp github github --openai-api-key sk-... --output-dir ./github-mcp-server
```

### Advanced Options

```bash
# Include private methods and generate more tools
sdk-to-mcp github github --include-private --max-methods 100 --output-dir ./github-mcp-server

# Skip test generation
sdk-to-mcp kubernetes kubernetes --no-tests --output-dir ./k8s-mcp-server

# Verbose output
sdk-to-mcp azure azure.mgmt.resource --verbose --output-dir ./azure-mcp-server
```

## How It Works

The converter follows a multi-step process:

1. **SDK Introspection**: Uses Python's `inspect` module to discover all classes, methods, and their signatures
2. **LLM Analysis**: Leverages OpenAI's API to understand method purposes and generate descriptions
3. **MCP Generation**: Creates complete MCP server code with tools and resources
4. **Documentation**: Generates README, examples, and configuration files
5. **Testing**: Creates comprehensive test suites

## Generated Output

The converter generates a complete MCP server with:

- `mcp_server.py` - Main MCP server implementation
- `requirements.txt` - Python dependencies
- `README.md` - Documentation and usage instructions
- `config.json` - Configuration file
- `example_usage.py` - Usage examples
- `tests/` - Test files (if enabled)

## Example: PyGithub Conversion

```bash
sdk-to-mcp github github --output-dir ./github-mcp-server
```

This generates an MCP server with tools like:
- `create_repository` - Create a new GitHub repository
- `get_user_repos` - List user repositories
- `create_issue` - Create an issue in a repository
- `get_pull_requests` - List pull requests

## Configuration

### Environment Variables

Set SDK-specific environment variables:

```bash
# GitHub
export GITHUB_TOKEN="your-github-token"

# Kubernetes
export KUBECONFIG="/path/to/kubeconfig"

# Azure
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_RESOURCE_GROUP="your-resource-group"
```

### Config File

Create a `config.json` file:

```json
{
  "credentials": {
    "api_key": "your-api-key",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret"
  },
  "settings": {
    "max_retries": 3,
    "timeout": 30,
    "log_level": "INFO"
  }
}
```

## Running Generated MCP Servers

After conversion, run the generated server:

```bash
cd ./github-mcp-server
pip install -r requirements.txt
python mcp_server.py
```

## Architecture

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black sdk_to_mcp_converter/

# Type checking
mypy sdk_to_mcp_converter/
```

## License

MIT License - see LICENSE file for details.

## Roadmap

- [ ] Support for more SDKs (AWS, Google Cloud, etc.)
- [ ] Custom tool grouping strategies
- [ ] Advanced authentication patterns
- [ ] MCP server optimization
- [ ] Web UI for conversion
- [ ] SDK compatibility testing

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure the SDK is installed
   ```bash
   pip install github  # for PyGithub
   pip install kubernetes  # for Kubernetes
   ```

2. **OpenAI API Error**: Check your API key and quota
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

3. **Permission Error**: Ensure write permissions for output directory
   ```bash
   chmod 755 ./output-directory
   ```

### Getting Help

- Check the [Issues](https://github.com/your-username/sdk-to-mcp-converter/issues) page
- Create a new issue with detailed error information
- Include SDK version and Python version in bug reports

## Acknowledgments

- Built for the MCP (Model Context Protocol) ecosystem
- Inspired by the need for comprehensive SDK integration in AI assistants
- Uses OpenAI's API for intelligent method analysis
