# Installation Guide

This guide provides detailed instructions for installing and setting up the Rundeck MCP Server.

## Prerequisites

- Python 3.8 or higher
- Linux operating system (recommended)
- Access to a Rundeck server
- Rundeck API token

## Installation Methods

### Method 1: Quick Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/rundeck-mcp-server.git
   cd rundeck-mcp-server
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure your environment:**
   Edit the `.env` file with your Rundeck server details:
   ```bash
   nano .env
   ```

4. **Test the installation:**
   ```bash
   source .venv/bin/activate
   python tests/test_server.py
   ```

### Method 2: Manual Installation

1. **Clone and navigate:**
   ```bash
   git clone https://github.com/your-username/rundeck-mcp-server.git
   cd rundeck-mcp-server
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp config.env.example .env
   # Edit .env with your settings
   ```

### Method 3: Package Installation

1. **Install from source:**
   ```bash
   git clone https://github.com/your-username/rundeck-mcp-server.git
   cd rundeck-mcp-server
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. **Or install from PyPI (when available):**
   ```bash
   pip install rundeck-mcp-server
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Primary Rundeck Server
RUNDECK_URL=https://your-rundeck-server.com
RUNDECK_API_TOKEN=your-api-token
RUNDECK_API_VERSION=47
RUNDECK_NAME=primary

# Optional: Secondary Rundeck Server
RUNDECK_URL_1=https://your-second-rundeck-server.com
RUNDECK_API_TOKEN_1=your-second-api-token
RUNDECK_API_VERSION_1=47
RUNDECK_NAME_1=secondary
```

### Getting API Tokens

1. Log into your Rundeck web interface
2. Navigate to **User Profile** → **User API Tokens**
3. Click **Generate API Token**
4. Copy the token and add it to your `.env` file

## Claude Desktop Integration

### Automatic Configuration

Use the provided script to configure Claude Desktop:

```bash
source .venv/bin/activate
python tests/get_claude_config.py
```

### Manual Configuration

Add to your Claude Desktop configuration file:

**Location:** `~/.config/claude-desktop/config.json` (Linux) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "rundeck": {
      "command": "/path/to/rundeck-mcp-server/.venv/bin/python",
      "args": ["/path/to/rundeck-mcp-server/rundeck_mcp_server.py"],
      "env": {
        "RUNDECK_URL": "https://your-rundeck-server.com",
        "RUNDECK_API_TOKEN": "your-api-token",
        "RUNDECK_API_VERSION": "47",
        "RUNDECK_NAME": "primary"
      }
    }
  }
}
```

## Testing

### Basic Connection Test

```bash
source .venv/bin/activate
python tests/test_server.py
```

### Multi-Server Test

```bash
source .venv/bin/activate
python tests/test_multi_server.py
```

### Debug Tools

```bash
# Debug job execution
python tests/debug_jobs.py

# Fix Claude configuration
python tests/fix_claude_config.py
```

## Running the Server

### Development Mode

```bash
source .venv/bin/activate
python rundeck_mcp_server.py
```

### Production Mode

```bash
source .venv/bin/activate
nohup python rundeck_mcp_server.py > mcp_server.log 2>&1 &
```

## Troubleshooting

### Common Issues

1. **Python version errors:**
   - Ensure Python 3.8+ is installed
   - Use `python3 --version` to check

2. **Virtual environment issues:**
   - Delete `.venv` directory and recreate
   - Ensure you're activating the environment

3. **API connection errors:**
   - Verify Rundeck URL and token
   - Check network connectivity
   - Validate API version compatibility

4. **Claude Desktop integration:**
   - Restart Claude Desktop after configuration
   - Check configuration file syntax
   - Verify file paths are absolute

### Getting Help

- Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- Review [Claude Desktop Setup](docs/CLAUDE_DESKTOP_SETUP.md)
- Open an issue on GitHub

## Development Setup

### Additional Dependencies

```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

### Running Tests

```bash
source .venv/bin/activate
pytest tests/
```

### Code Formatting

```bash
source .venv/bin/activate
black .
flake8 .
mypy .
```

## Uninstallation

```bash
# Remove virtual environment
rm -rf .venv

# Remove configuration (optional)
rm .env

# Remove the entire directory
cd ..
rm -rf rundeck-mcp-server