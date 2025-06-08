#!/usr/bin/env python3
"""
Debug script to troubleshoot job list issues
"""

import os
import sys
import json
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_job_retrieval():
    """Test job retrieval with detailed logging"""
    print("🔍 Debugging Job Retrieval")
    print("=" * 50)
    
    # Import after adding to path
    from rundeck_mcp_server import RundeckClient
    
    # Get environment variables
    base_url = os.getenv('RUNDECK_URL')
    api_token = os.getenv('RUNDECK_API_TOKEN')
    api_version = os.getenv('RUNDECK_API_VERSION', '47')
    
    if not base_url or not api_token:
        print("❌ Missing environment variables")
        return False
    
    print(f"🌐 Rundeck URL: {base_url}")
    print(f"🔑 API Version: {api_version}")
    print(f"🎫 Token: {'*' * (len(api_token) - 4) + api_token[-4:]}")
    print()
    
    try:
        # Create client
        client = RundeckClient(base_url, api_token, api_version)
        
        # Test 1: Get projects first
        print("📋 Step 1: Testing project access...")
        projects = client.get_projects()
        print(f"✅ Found {len(projects)} projects")
        
        if not projects:
            print("❌ No projects found - check API token permissions")
            return False
        
        # Show first few projects
        for i, project in enumerate(projects[:3]):
            print(f"  {i+1}. {project.get('name', 'Unknown')} - {project.get('description', 'No description')}")
        print()
        
        # Test 2: Try to get jobs for first project
        first_project = projects[0].get('name')
        if not first_project:
            print("❌ First project has no name")
            return False
            
        print(f"🔧 Step 2: Testing job access for project '{first_project}'...")
        
        try:
            jobs = client.get_jobs(first_project)
            print(f"✅ Successfully retrieved {len(jobs)} jobs")
            
            if jobs:
                print("📝 Sample jobs:")
                for i, job in enumerate(jobs[:5]):
                    print(f"  {i+1}. {job.get('name', 'Unknown')} (ID: {job.get('id', 'Unknown')})")
            else:
                print("ℹ️  No jobs found in this project")
                
        except Exception as e:
            print(f"❌ Error retrieving jobs: {e}")
            print(f"🔍 Error type: {type(e).__name__}")
            
            # Check if it's a permissions issue
            if "403" in str(e) or "Forbidden" in str(e):
                print("💡 This appears to be a permissions issue")
                print("   Your API token may lack 'read' permission for jobs")
            elif "404" in str(e):
                print("💡 This appears to be an endpoint issue")
                print("   The jobs endpoint may not exist or project name is wrong")
            else:
                print("💡 This appears to be a connection or server issue")
            
            return False
        
        print()
        print("✅ Job retrieval test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create client or connect: {e}")
        return False

def main():
    """Run the debug tests"""
    print("Rundeck Job Retrieval Debug Tool")
    print("=" * 40)
    
    # Load environment
    env_file = Path(".env")
    if env_file.exists():
        print("📁 Loading .env file...")
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print("✅ Environment loaded")
    else:
        print("⚠️  No .env file found")
    
    print()
    
    # Run tests
    success = test_job_retrieval()
    
    print()
    print("=" * 50)
    if success:
        print("🎉 All tests passed! Job retrieval should work.")
    else:
        print("❌ Tests failed. Check the error messages above.")
        print()
        print("💡 Common solutions:")
        print("  • Check API token permissions in Rundeck")
        print("  • Verify project names are correct")
        print("  • Ensure Rundeck server is accessible")
        print("  • Try using a different API version")

if __name__ == "__main__":
    main()