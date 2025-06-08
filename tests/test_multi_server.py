#!/usr/bin/env python3
"""
Comprehensive test for multi-server Rundeck MCP configuration
"""

import os
import sys
import asyncio
from pathlib import Path

# Add current directory to path
sys.path.append('.')

def test_environment_setup():
    """Test that environment variables are properly configured"""
    print("🔧 Testing Environment Setup")
    print("-" * 40)
    
    # Test main server
    main_url = os.getenv('RUNDECK_URL')
    main_token = os.getenv('RUNDECK_API_TOKEN')
    
    if main_url and main_token:
        print(f"✅ Main server configured: {main_url}")
    else:
        print("❌ Main server not configured")
        return False
    
    # Test additional servers
    servers_found = 0
    for i in range(1, 10):
        url = os.getenv(f'RUNDECK_URL_{i}')
        token = os.getenv(f'RUNDECK_API_TOKEN_{i}')
        name = os.getenv(f'RUNDECK_NAME_{i}', f'server_{i}')
        
        if url and token:
            print(f"✅ Server {i} ({name}): {url}")
            servers_found += 1
    
    if servers_found > 0:
        print(f"✅ Found {servers_found} additional server(s)")
    else:
        print("ℹ️  No additional servers configured")
    
    print()
    return True

def test_server_initialization():
    """Test server initialization"""
    print("🚀 Testing Server Initialization")
    print("-" * 40)
    
    try:
        from rundeck_mcp_server import initialize_rundeck_clients, list_rundeck_servers
        
        # Initialize clients
        initialize_rundeck_clients()
        
        # List servers
        servers = list_rundeck_servers()
        print(f"✅ Initialized {len(servers)} server(s):")
        for server in servers:
            print(f"   - {server}")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Server initialization failed: {e}")
        print()
        return False

def test_client_connectivity():
    """Test client connectivity"""
    print("🌐 Testing Client Connectivity")
    print("-" * 40)
    
    try:
        from rundeck_mcp_server import get_rundeck_client, list_rundeck_servers
        
        servers = list_rundeck_servers()
        success_count = 0
        
        for server_name in servers:
            try:
                client = get_rundeck_client(server_name)
                print(f"✅ {server_name}: Connected to {client.base_url}")
                success_count += 1
            except Exception as e:
                print(f"❌ {server_name}: Connection failed - {e}")
        
        print(f"\n✅ {success_count}/{len(servers)} servers connected successfully")
        print()
        return success_count == len(servers)
        
    except Exception as e:
        print(f"❌ Connectivity test failed: {e}")
        print()
        return False

def test_claude_desktop_config():
    """Test Claude Desktop configuration"""
    print("🖥️  Testing Claude Desktop Configuration")
    print("-" * 40)
    
    # Check if config file exists
    home = Path.home()
    config_path = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    
    if not config_path.exists():
        print("❌ Claude Desktop config file not found")
        print(f"   Expected at: {config_path}")
        print()
        return False
    
    try:
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check for rundeck server
        if 'mcpServers' not in config:
            print("❌ No mcpServers section found")
            return False
        
        if 'rundeck' not in config['mcpServers']:
            print("❌ No rundeck server configured")
            return False
        
        rundeck_config = config['mcpServers']['rundeck']
        
        # Check command
        command = rundeck_config.get('command', '')
        if '.venv/bin/python' in command:
            print(f"✅ Python command: {command}")
        else:
            print(f"❌ Invalid Python command: {command}")
            return False
        
        # Check args
        args = rundeck_config.get('args', [])
        if len(args) > 0 and 'rundeck_mcp_server.py' in args[0]:
            print(f"✅ Server script: {args[0]}")
        else:
            print(f"❌ Invalid server script: {args}")
            return False
        
        # Check environment
        env = rundeck_config.get('env', {})
        env_servers = 0
        
        if 'RUNDECK_URL' in env:
            print(f"✅ Main server URL configured")
            env_servers += 1
        
        for i in range(1, 10):
            if f'RUNDECK_URL_{i}' in env:
                name = env.get(f'RUNDECK_NAME_{i}', f'server_{i}')
                print(f"✅ Server {i} ({name}) configured")
                env_servers += 1
        
        print(f"✅ Total servers in Claude config: {env_servers}")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Config file parsing failed: {e}")
        print()
        return False

def main():
    """Run all tests"""
    print("Rundeck MCP Multi-Server Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Server Initialization", test_server_initialization),
        ("Client Connectivity", test_client_connectivity),
        ("Claude Desktop Config", test_claude_desktop_config),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Multi-server setup is working correctly.")
        print()
        print("Next steps:")
        print("1. Restart Claude Desktop")
        print("2. Test with: 'Can you list all configured Rundeck servers?'")
        print("3. Try: 'Show me projects from the demo server'")
    else:
        print("❌ Some tests failed. Please check the configuration.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)