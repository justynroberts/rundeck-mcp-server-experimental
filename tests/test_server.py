#!/usr/bin/env python3
"""
Simple test script for Rundeck MCP Server
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to Python path to import rundeck_mcp_server
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_environment():
    """Test environment configuration"""
    print("=== Environment Test ===")
    
    # Check for single server configuration (backward compatibility)
    base_url = os.getenv('RUNDECK_URL')
    api_token = os.getenv('RUNDECK_API_TOKEN')
    api_version = os.getenv('RUNDECK_API_VERSION', '47')
    
    servers_found = 0
    
    if base_url and api_token and not base_url.startswith('https://your-') and not api_token.startswith('your-'):
        print(f"✓ RUNDECK_URL: {'*' * (len(base_url) - 10) + base_url[-10:] if len(base_url) > 10 else '***'}")
        print(f"✓ RUNDECK_API_TOKEN: {'*' * (len(api_token) - 4) + api_token[-4:] if len(api_token) > 4 else '***'}")
        print(f"✓ RUNDECK_API_VERSION: {api_version}")
        servers_found += 1
    elif base_url and api_token:
        print("ℹ️  Single server configuration found but contains placeholder values")
        print("   Please update .env with your actual Rundeck server details")
    else:
        print("ℹ️  Single server configuration not found")
    
    # Check for multiple server configuration
    for i in range(1, 10):
        url_key = f'RUNDECK_URL_{i}'
        token_key = f'RUNDECK_API_TOKEN_{i}'
        name_key = f'RUNDECK_NAME_{i}'
        
        server_url = os.getenv(url_key)
        server_token = os.getenv(token_key)
        server_name = os.getenv(name_key, f'server_{i}')
        
        if server_url and server_token and not server_url.startswith('https://rundeck-') and not server_token.endswith('-here'):
            print(f"✓ {name_key}: {server_name}")
            print(f"✓ {url_key}: {'*' * (len(server_url) - 10) + server_url[-10:] if len(server_url) > 10 else '***'}")
            print(f"✓ {token_key}: {'*' * (len(server_token) - 4) + server_token[-4:] if len(server_token) > 4 else '***'}")
            servers_found += 1
    
    if servers_found == 0:
        print("\n💡 Multiple Server Configuration:")
        print("   No additional servers configured (this is optional)")
        print("   To add multiple servers, configure RUNDECK_URL_1, RUNDECK_API_TOKEN_1, etc.")
        print("\n✅ Configuration test completed")
        print("   Note: Update .env with real server details to test actual connectivity")
        return True  # Don't fail the test for missing config
    
    print(f"\n✅ Found {servers_found} configured server(s)")
    return True

def test_tool_prompts():
    """Test tool prompts loading"""
    print("\n=== Tool Prompts Test ===")
    
    prompts_file = Path(__file__).parent.parent / "tool_prompts.json"
    
    if not prompts_file.exists():
        print(f"✗ Tool prompts file not found: {prompts_file}")
        return False
    
    try:
        with open(prompts_file, 'r') as f:
            prompts = json.load(f)
        
        print(f"✓ Tool prompts loaded successfully")
        print(f"✓ Found {len(prompts)} tool prompts")
        
        # Check if all expected tools have prompts
        expected_tools = [
            'list_servers', 'get_projects', 'get_jobs', 'get_job_definition', 'run_job',
            'get_execution_status', 'get_execution_output', 'get_executions', 'get_all_executions',
            'get_execution_metrics', 'get_system_info', 'get_project_stats',
            'calculate_job_roi', 'get_bulk_execution_status', 'run_job_with_monitoring'
        ]
        
        missing_prompts = [tool for tool in expected_tools if tool not in prompts]
        if missing_prompts:
            print(f"⚠ Missing prompts for tools: {', '.join(missing_prompts)}")
        else:
            print("✓ All expected tools have prompts")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing tool prompts JSON: {e}")
        return False
    except Exception as e:
        print(f"✗ Error loading tool prompts: {e}")
        return False

def test_server_import():
    """Test server module import"""
    print("\n=== Server Import Test ===")
    
    try:
        import rundeck_mcp_server
        print("✓ Server module imported successfully")
        
        # Test if RundeckClient can be instantiated
        if hasattr(rundeck_mcp_server, 'RundeckClient'):
            print("✓ RundeckClient class found")
        else:
            print("✗ RundeckClient class not found")
            return False
        
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import server module: {e}")
        return False
    except Exception as e:
        print(f"✗ Error testing server import: {e}")
        return False

def main():
    """Run all tests"""
    print("Rundeck MCP Server Test Suite")
    print("=" * 40)
    
    tests = [
        test_environment,
        test_tool_prompts,
        test_server_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())