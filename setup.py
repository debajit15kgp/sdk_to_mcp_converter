"""
Setup script for SDK to MCP converter.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

setup(
    name="sdk-to-mcp-converter",
    version="0.1.0",
    author="SDK to MCP Converter",
    author_email="",
    description="Convert Python SDKs to MCP (Model Context Protocol) servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/sdk-to-mcp-converter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "mcp>=1.0.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "examples": [
            "github>=1.59.0",  # PyGithub
            "kubernetes>=28.0.0",
            "azure-identity>=1.15.0",
            "azure-mgmt-resource>=23.0.0",
            "azure-core>=1.29.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "sdk-to-mcp=sdk_to_mcp_converter.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
