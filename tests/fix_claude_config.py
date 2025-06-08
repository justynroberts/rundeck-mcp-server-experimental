#!/usr/bin/env python3
"""
Fix Claude Desktop configuration for multi-server setup
"""

import json
import os

def main():
    config_path = "/Users/justynroberts/Library/Application Support/Claude/claude_desktop_config.json"
    
    config = {
        "mcpServers": {
            "rundeck": {
                "command": "/Users/justynroberts/work/rundeck-mcp-server/.venv/bin/python",
                "args": ["/Users/justynroberts/work/rundeck-mcp-server/rundeck_mcp_server.py"],
                "env": {
                    "RUNDECK_URL": "http://emeademo.pagerdutyautomation.com:4440",
                    "RUNDECK_API_TOKEN": "CPjIXQN0Ydekt19l2JeviPCQiqBYmDzw",
                    "RUNDECK_API_VERSION": "47",
                    "RUNDECK_NAME": "emea",
                    "RUNDECK_URL_1": "https://demo.runbook.pagerduty.cloud",
                    "RUNDECK_API_TOKEN_1": "Q8zBG6pUkxInOg9fIA164eW4qyWXryxT",
                    "RUNDECK_API_VERSION_1": "47",
                    "RUNDECK_NAME_1": "demo"
                }
            }
        }
    }
    
    # Write configuration
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration written successfully")
    
    # Validate
    with open(config_path, 'r') as f:
        test = json.load(f)
    
    print("✅ Configuration validated successfully")
    print(f"✅ Servers configured: {len(test['mcpServers'])}")
    
    # Show final config
    print("\n📋 Final configuration:")
    print(json.dumps(config, indent=2))

if __name__ == "__main__":
    main()