# Claude Desktop Multiple Servers Configuration Guide

This guide shows you how to configure multiple Rundeck servers in Claude Desktop.

## Quick Setup

### Step 1: Configure Your Servers

Edit your `.env` file with multiple server configurations:

```bash
# Main server (backward compatible)
RUNDECK_URL=https://rundeck-main.company.com
RUNDECK_API_TOKEN=main-server-token-here
RUNDECK_API_VERSION=47

# Production server
RUNDECK_URL_1=https://rundeck-prod.company.com
RUNDECK_API_TOKEN_1=prod-server-token-here
RUNDECK_API_VERSION_1=47
RUNDECK_NAME_1=production

# Staging server
RUNDECK_URL_2=https://rundeck-staging.company.com
RUNDECK_API_TOKEN_2=staging-server-token-here
RUNDECK_API_VERSION_2=47
RUNDECK_NAME_2=staging

# Development server
RUNDECK_URL_3=https://rundeck-dev.company.com
RUNDECK_API_TOKEN_3=dev-server-token-here
RUNDECK_API_VERSION_3=47
RUNDECK_NAME_3=development
```

### Step 2: Generate Claude Desktop Configuration

Run the configuration generator:

```bash
source .venv/bin/activate
python get_claude_config.py
```

This will output the complete configuration with all your servers.

### Step 3: Update Claude Desktop

1. **Find your Claude Desktop config file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Add the configuration** from step 2 to your Claude Desktop config file

3. **Restart Claude Desktop**

## Manual Configuration

If you prefer to configure manually, here's the Claude Desktop configuration format:

```json
{
  "mcpServers": {
    "rundeck": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/rundeck_mcp_server.py"],
      "env": {
        "RUNDECK_URL": "https://rundeck-main.company.com",
        "RUNDECK_API_TOKEN": "main-server-token",
        "RUNDECK_API_VERSION": "47",
        "RUNDECK_URL_1": "https://rundeck-prod.company.com",
        "RUNDECK_API_TOKEN_1": "prod-server-token",
        "RUNDECK_API_VERSION_1": "47",
        "RUNDECK_NAME_1": "production",
        "RUNDECK_URL_2": "https://rundeck-staging.company.com",
        "RUNDECK_API_TOKEN_2": "staging-server-token",
        "RUNDECK_API_VERSION_2": "47",
        "RUNDECK_NAME_2": "staging",
        "RUNDECK_URL_3": "https://rundeck-dev.company.com",
        "RUNDECK_API_TOKEN_3": "dev-server-token",
        "RUNDECK_API_VERSION_3": "47",
        "RUNDECK_NAME_3": "development"
      }
    }
  }
}
```

## Using Multiple Servers in Claude

Once configured, you can use multiple servers in Claude:

### List Available Servers
```
Can you list all configured Rundeck servers?
```

### Target Specific Servers
```
Show me projects from the production server
Get jobs from the staging environment for project "web-app"
Run the deployment job on the development server
```

### Server-Specific Commands
```
Get execution metrics for the last 30 days from production
Show me failed jobs from staging in the last week
List all projects from the development server
```

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `RUNDECK_URL` | Main server URL | Yes (for single server) |
| `RUNDECK_API_TOKEN` | Main server API token | Yes (for single server) |
| `RUNDECK_API_VERSION` | Main server API version | No (defaults to 47) |
| `RUNDECK_URL_N` | Additional server URL | Yes (for server N) |
| `RUNDECK_API_TOKEN_N` | Additional server API token | Yes (for server N) |
| `RUNDECK_API_VERSION_N` | Additional server API version | No (defaults to 47) |
| `RUNDECK_NAME_N` | Additional server name | No (defaults to server_N) |

Where `N` is a number from 1 to 9.

## Troubleshooting

### Server Not Found
If Claude says a server is not found:
1. Check the server name spelling
2. Use `list_servers` to see available servers
3. Verify your `.env` configuration

### Connection Issues
If you get connection errors:
1. Verify the server URLs are correct
2. Check that API tokens are valid
3. Ensure the servers are accessible from your network

### Configuration Issues
If the configuration doesn't work:
1. Restart Claude Desktop after making changes
2. Check the Claude Desktop config file syntax
3. Use `python get_claude_config.py` to regenerate the configuration

## Example Workflows

### Multi-Environment Deployment
```
1. "Show me the deployment job from staging"
2. "Run the deployment job on staging with version=1.2.3"
3. "Check the execution status"
4. "If successful, run the same job on production"
```

### Cross-Environment Monitoring
```
1. "List all configured servers"
2. "Get execution metrics from production for the last 7 days"
3. "Compare with staging metrics for the same period"
4. "Show me any failed jobs across all environments"
```

### Development Workflow
```
1. "Get jobs from development server for project 'api'"
2. "Run the test job on development"
3. "If tests pass, run the build job on staging"
4. "Monitor the execution until completion"