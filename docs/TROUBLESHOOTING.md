# Rundeck MCP Server Troubleshooting Guide

This guide helps you diagnose and fix common issues with the Rundeck MCP server.

## Quick Diagnostic Steps

### 1. Test Your Setup First

Before troubleshooting Claude Desktop integration, verify your basic setup:

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Test Rundeck connection
python test_server.py

# 3. Check MCP server can start
python rundeck_mcp_server.py --help
```

### 2. Generate Debug Configuration

```bash
# Get your exact configuration
python get_claude_config.py
```

## Common Issues and Solutions

### Issue 1: "Server not found" or "Failed to connect to server"

**Symptoms:**
- Claude Desktop shows "Server not found"
- MCP server doesn't appear in Claude

**Diagnosis:**
```bash
# Check if Python path is correct
ls -la /your/path/.venv/bin/python

# Check if server script exists
ls -la /your/path/rundeck_mcp_server.py

# Test Python can run the script
/your/path/.venv/bin/python /your/path/rundeck_mcp_server.py
```

**Solutions:**
1. **Fix Python path:**
   ```bash
   # Get correct path
   cd /your/rundeck-mcp-server
   pwd
   # Use: /output/from/pwd/.venv/bin/python
   ```

2. **Make script executable:**
   ```bash
   chmod +x rundeck_mcp_server.py
   ```

3. **Check JSON syntax:**
   ```bash
   # Validate your claude_desktop_config.json
   python -m json.tool ~/.config/Claude/claude_desktop_config.json
   ```

### Issue 2: "Connection failed" or Rundeck API errors

**Symptoms:**
- Server starts but can't connect to Rundeck
- "Authentication failed" errors
- "Connection timeout" errors

**Diagnosis:**
```bash
# Test Rundeck connection directly
source .venv/bin/activate
export RUNDECK_URL="https://your-rundeck-server.com"
export RUNDECK_API_TOKEN="your-token"
python test_server.py
```

**Solutions:**
1. **Check Rundeck URL:**
   ```bash
   # Test URL accessibility
   curl -I https://your-rundeck-server.com
   
   # Should return HTTP 200 or redirect
   ```

2. **Verify API token:**
   ```bash
   # Test API token directly
   curl -H "X-Rundeck-Auth-Token: your-token" \
        https://your-rundeck-server.com/api/47/projects
   ```

3. **Check API version:**
   ```bash
   # Try different API versions
   curl https://your-rundeck-server.com/api/1/system/info
   ```

### Issue 3: "Permission denied" or API access errors

**Symptoms:**
- "Insufficient permissions" errors
- "Access denied" messages
- Some tools work, others don't

**Diagnosis:**
```bash
# Test specific API endpoints
curl -H "X-Rundeck-Auth-Token: your-token" \
     https://your-rundeck-server.com/api/47/projects

curl -H "X-Rundeck-Auth-Token: your-token" \
     https://your-rundeck-server.com/api/47/project/PROJECT_NAME/jobs
```

**Solutions:**
1. **Check token permissions in Rundeck:**
   - Log into Rundeck web interface
   - Go to User Profile > User API Tokens
   - Verify token has required permissions:
     - Projects: Read
     - Jobs: Read, Execute
     - Executions: Read, Execute

2. **Generate new token with correct permissions**

### Issue 4: Environment variable issues

**Symptoms:**
- "Environment variables not set" errors
- Server starts but shows placeholder values

**Diagnosis:**
```bash
# Check environment variables
echo $RUNDECK_URL
echo $RUNDECK_API_TOKEN
echo $RUNDECK_API_VERSION

# Check .env file
cat .env
```

**Solutions:**
1. **Create .env file:**
   ```bash
   cp config.env.example .env
   # Edit .env with your values
   ```

2. **Load environment variables:**
   ```bash
   # For testing
   export $(cat .env | xargs)
   
   # Verify
   echo $RUNDECK_URL
   ```

### Issue 5: Claude Desktop doesn't restart properly

**Symptoms:**
- Changes to config don't take effect
- Old server configuration still active

**Solutions:**
1. **Complete restart:**
   ```bash
   # macOS
   killall Claude
   open -a Claude
   
   # Linux
   pkill claude
   claude &
   ```

2. **Clear Claude cache (if needed):**
   ```bash
   # macOS
   rm -rf ~/Library/Caches/Claude
   
   # Linux
   rm -rf ~/.cache/Claude
   ```

## Advanced Debugging

### Enable Debug Logging

1. **Modify server for debug output:**
   ```python
   # In rundeck_mcp_server.py, change:
   logging.basicConfig(level=logging.INFO)
   # to:
   logging.basicConfig(level=logging.DEBUG, 
                      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   ```

2. **Run server manually to see logs:**
   ```bash
   source .venv/bin/activate
   export $(cat .env | xargs)
   python rundeck_mcp_server.py
   ```

### Test Individual Components

1. **Test Rundeck client directly:**
   ```python
   from rundeck_mcp_server import RundeckClient
   import os
   
   client = RundeckClient(
       os.getenv('RUNDECK_URL'),
       os.getenv('RUNDECK_API_TOKEN')
   )
   
   # Test each method
   projects = client.get_projects()
   print(f"Projects: {len(projects)}")
   ```

2. **Test MCP server without Claude:**
   ```bash
   # Install MCP client tools
   pip install mcp-client
   
   # Test server directly
   mcp-client test /path/to/rundeck_mcp_server.py
   ```

### Network Debugging

1. **Check network connectivity:**
   ```bash
   # Test basic connectivity
   ping your-rundeck-server.com
   
   # Test HTTPS
   openssl s_client -connect your-rundeck-server.com:443
   
   # Test with proxy (if applicable)
   curl --proxy http://proxy:port https://your-rundeck-server.com
   ```

2. **Check firewall/proxy settings:**
   ```bash
   # Check if corporate proxy is blocking
   echo $HTTP_PROXY
   echo $HTTPS_PROXY
   ```

## Diagnostic Scripts

### Create a comprehensive test script:

```bash
# Save as debug_all.sh
#!/bin/bash

echo "=== Rundeck MCP Server Debug ==="
echo "Date: $(date)"
echo

echo "1. Environment Check:"
echo "RUNDECK_URL: $RUNDECK_URL"
echo "RUNDECK_API_TOKEN: ${RUNDECK_API_TOKEN:0:10}..."
echo "RUNDECK_API_VERSION: $RUNDECK_API_VERSION"
echo

echo "2. File Check:"
ls -la rundeck_mcp_server.py
ls -la .venv/bin/python
echo

echo "3. Python Environment:"
.venv/bin/python --version
.venv/bin/python -c "import mcp; print('MCP version:', mcp.__version__)"
.venv/bin/python -c "import requests; print('Requests version:', requests.__version__)"
echo

echo "4. Network Test:"
curl -I $RUNDECK_URL 2>/dev/null | head -1
echo

echo "5. API Test:"
curl -s -H "X-Rundeck-Auth-Token: $RUNDECK_API_TOKEN" \
     "$RUNDECK_URL/api/47/system/info" | head -3
echo

echo "6. MCP Server Test:"
timeout 5 .venv/bin/python rundeck_mcp_server.py || echo "Server test completed"
```

### Run the debug script:
```bash
chmod +x debug_all.sh
export $(cat .env | xargs)
./debug_all.sh
```

## Getting Help

### Collect Information for Support

When asking for help, provide:

1. **System information:**
   ```bash
   uname -a
   python --version
   ```

2. **Configuration (sanitized):**
   ```bash
   # Remove sensitive tokens before sharing
   cat claude_desktop_config.json | sed 's/"your-api-token-here"/"[REDACTED]"/g'
   ```

3. **Error messages:**
   - Full error text from Claude Desktop
   - Server logs from manual run
   - Network test results

4. **Test results:**
   ```bash
   python test_server.py 2>&1
   ```

### Common Log Locations

- **Claude Desktop logs (macOS):** `~/Library/Logs/Claude/`
- **Claude Desktop logs (Linux):** `~/.local/share/Claude/logs/`
- **MCP Server logs:** Console output when running manually

## Quick Reference Commands

```bash
# Complete reset and test
./setup.sh
cp config.env.example .env
# Edit .env with your values
source .venv/bin/activate
export $(cat .env | xargs)
python test_server.py
python get_claude_config.py

# Test Claude Desktop config
python -m json.tool ~/.config/Claude/claude_desktop_config.json

# Manual server test
source .venv/bin/activate
export $(cat .env | xargs)
python rundeck_mcp_server.py

# Debug network issues
curl -v -H "X-Rundeck-Auth-Token: $RUNDECK_API_TOKEN" \
     "$RUNDECK_URL/api/47/projects"
```

Remember: Most issues are related to incorrect paths, missing environment variables, or network connectivity. Start with the basic tests and work your way up to more complex debugging.