#!/usr/bin/env python3
"""
Setup script for Rundeck MCP Server
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements from requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rundeck-mcp-server",
    version="1.0.0",
    author="Rundeck MCP Server Team",
    description="Model Context Protocol (MCP) server for Rundeck automation platform",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/rundeck-mcp-server",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rundeck-mcp-server=rundeck_mcp_server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "*.txt"],
    },
    zip_safe=False,
    keywords="rundeck mcp server automation devops",
    project_urls={
        "Bug Reports": "https://github.com/your-username/rundeck-mcp-server/issues",
        "Source": "https://github.com/your-username/rundeck-mcp-server",
        "Documentation": "https://github.com/your-username/rundeck-mcp-server/blob/main/README.md",
    },
)