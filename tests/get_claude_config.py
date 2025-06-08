#!/usr/bin/env python3
"""
Helper script to generate Claude Desktop configuration for Rundeck MCP Server
This script outputs the exact configuration needed for your system.
"""

import os
import json
import sys
from pathlib import Path


def get_project_path():
    """Get the absolute path to the project directory"""
    return os.path.abspath(os.path.dirname(__file__))


def get_venv_python_path():
    """Get the path to the virtual environment Python"""
    project_path = get_project_path()
    venv_python = os.path.join(project_path, '.venv', 'bin', 'python')
    
    if not os.path.exists(venv_python):
        print(f"❌ Virtual environment not found at: {venv_python}")
        print("Please run './setup.sh' first to create the virtual environment.")
        return None
    
    return venv_python


def get_server_script_path():
    """Get the path to the MCP server script"""
    project_path = get_project_path()
    server_script = os.path.join(project_path, 'rundeck_mcp_server.py')
    
    if not os.path.exists(server_script):
        print(f"❌ Server script not found at: {server_script}")
        return None
    
    return server_script


def load_env_config():
    """Load configuration from .env file"""
    env_file = os.path.join(get_project_path(), '.env')
    
    if not os.path.exists(env_file):
        print("⚠️  .env file not found. Using placeholder values.")
        return {
            'RUNDECK_URL': 'https://your-rundeck-server.com',
            'RUNDECK_API_TOKEN': 'your-api-token-here',
            'RUNDECK_API_VERSION': '47'
        }
    
    env_vars = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    
    return env_vars


def generate_claude_config():
    """Generate the Claude Desktop configuration"""
    venv_python = get_venv_python_path()
    server_script = get_server_script_path()
    
    if not venv_python or not server_script:
        return None
    
    env_config = load_env_config()
    
    # Build environment variables for Claude Desktop
    claude_env = {}
    
    # Add single server configuration (backward compatible)
    if 'RUNDECK_URL' in env_config:
        claude_env['RUNDECK_URL'] = env_config['RUNDECK_URL']
    if 'RUNDECK_API_TOKEN' in env_config:
        claude_env['RUNDECK_API_TOKEN'] = env_config['RUNDECK_API_TOKEN']
    if 'RUNDECK_API_VERSION' in env_config:
        claude_env['RUNDECK_API_VERSION'] = env_config['RUNDECK_API_VERSION']
    
    # Add multiple server configurations
    for i in range(1, 10):
        url_key = f'RUNDECK_URL_{i}'
        token_key = f'RUNDECK_API_TOKEN_{i}'
        version_key = f'RUNDECK_API_VERSION_{i}'
        name_key = f'RUNDECK_NAME_{i}'
        
        if url_key in env_config:
            claude_env[url_key] = env_config[url_key]
        if token_key in env_config:
            claude_env[token_key] = env_config[token_key]
        if version_key in env_config:
            claude_env[version_key] = env_config[version_key]
        if name_key in env_config:
            claude_env[name_key] = env_config[name_key]
    
    # If no environment variables found, use defaults
    if not claude_env:
        claude_env = {
            'RUNDECK_URL': 'https://your-rundeck-server.com',
            'RUNDECK_API_TOKEN': 'your-api-token-here',
            'RUNDECK_API_VERSION': '47'
        }
    
    config = {
        "mcpServers": {
            "rundeck": {
                "command": venv_python,
                "args": [server_script],
                "env": claude_env
            }
        }
    }
    
    return config


def get_claude_config_path():
    """Get the Claude Desktop configuration file path for the current OS"""
    home = Path.home()
    
    if sys.platform == "darwin":  # macOS
        return home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "win32":  # Windows
        return Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"
    else:  # Linux and others
        return home / ".config" / "Claude" / "claude_desktop_config.json"


def main():
    """Main function"""
    print("Rundeck MCP Server - Claude Desktop Configuration Generator")
    print("=" * 60)
    
    # Generate configuration
    config = generate_claude_config()
    if not config:
        print("❌ Failed to generate configuration. Please check the setup.")
        sys.exit(1)
    
    # Display paths
    print(f"📁 Project directory: {get_project_path()}")
    print(f"🐍 Python executable: {get_venv_python_path()}")
    print(f"📜 Server script: {get_server_script_path()}")
    print()
    
    # Display configuration
    print("📋 Claude Desktop Configuration:")
    print("-" * 40)
    print(json.dumps(config, indent=2))
    print()
    
    # Display Claude config file location
    claude_config_path = get_claude_config_path()
    print(f"📍 Claude Desktop config file location:")
    print(f"   {claude_config_path}")
    print()
    
    # Check if Claude config exists
    if claude_config_path.exists():
        print("✅ Claude Desktop config file exists.")
        print("   You can add the 'rundeck' server to the existing 'mcpServers' section.")
    else:
        print("📝 Claude Desktop config file doesn't exist.")
        print("   You can create it with the configuration shown above.")
    
    print()
    print("🔧 Next steps:")
    print("1. Copy the configuration above")
    print("2. Add it to your Claude Desktop config file")
    print("3. Update RUNDECK_URL and RUNDECK_API_TOKEN if needed")
    print("4. Restart Claude Desktop")
    print("5. Test with: 'Can you list my Rundeck projects?'")


if __name__ == "__main__":
    main()