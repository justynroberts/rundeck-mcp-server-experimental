# Project Structure

This document outlines the streamlined structure of the Rundeck MCP Server project.

## Core Files

### Server Implementation
- **`rundeck_mcp_server.py`** - Main MCP server implementation with Rundeck API client
- **`tool_prompts.json`** - External tool prompts and descriptions (easily editable)

### Configuration
- **`requirements.txt`** - Python dependencies
- **`config.env.example`** - Example environment configuration
- **`claude_desktop_config.example.json`** - Example Claude Desktop configuration

### Setup and Testing
- **`setup.sh`** - Automated setup script for Linux environments
- **`test_server.py`** - Comprehensive test suite for server functionality
- **`get_claude_config.py`** - Generates Claude Desktop configuration

### Documentation
- **`README.md`** - Main project documentation
- **`TROUBLESHOOTING.md`** - Troubleshooting guide
- **`PROJECT_STRUCTURE.md`** - This file

## Key Features

### Externalized Tool Prompts
Tool descriptions and usage prompts are stored in `tool_prompts.json`, making them easy to edit without modifying the server code. Each tool has:
- `description`: Brief summary of functionality
- `prompt`: Detailed usage guidance

### Streamlined Testing
Single test script (`test_server.py`) covers:
- Environment configuration validation
- Tool prompts loading
- Server module import verification

### Linux-Optimized Setup
- Uses `.venv` virtual environment
- Automated dependency installation
- Proper file permissions

## Removed Files

The following non-essential files were removed to simplify the project:
- Multiple debug scripts (`debug_all.sh`, `debug_claude_desktop.py`)
- Redundant test files (`test_analytics.py`, `test_connection.py`)
- Multiple documentation files (consolidated into main README)
- Duplicate configuration examples

## Usage

1. **Setup**: `./setup.sh`
2. **Configure**: Edit `.env` with your Rundeck details
3. **Test**: `python test_server.py`
4. **Run**: `python rundeck_mcp_server.py`

## Customization

To customize tool prompts:
1. Edit `tool_prompts.json`
2. Restart the server
3. Changes take effect immediately