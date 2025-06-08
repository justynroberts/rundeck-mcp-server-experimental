#!/usr/bin/env python3
"""
Rundeck Enterprise MCP Server

This server provides MCP tools for interacting with Rundeck Enterprise, including:
- Getting jobs with definitions, tags, and options
- Running jobs with options
- Getting job execution status
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import urljoin
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
from pathlib import Path

import requests
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities, ToolsCapability, PromptsCapability
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RundeckClient:
    """Client for interacting with Rundeck Enterprise API"""
    
    def __init__(self, base_url: str, api_token: str, api_version: str = "47"):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.api_version = api_version
        self.session = requests.Session()
        self.session.headers.update({
            'X-Rundeck-Auth-Token': api_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the Rundeck API with enhanced error handling"""
        url = urljoin(f"{self.base_url}/api/{self.api_version}/", endpoint.lstrip('/'))
        
        # Add default timeout and connection settings
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 30
        
        # Add retry logic for connection issues
        max_retries = 3
        response = None
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                
                # Handle empty responses
                if not response.content.strip():
                    return {}
                
                return response.json()
                
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"Connection error on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt == max_retries - 1:
                    raise requests.exceptions.ConnectionError(
                        f"Failed to connect to Rundeck server after {max_retries} attempts. "
                        f"Please check if the server is running and accessible at {self.base_url}"
                    )
                continue
                
            except requests.exceptions.Timeout as e:
                logger.warning(f"Timeout error on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt == max_retries - 1:
                    raise requests.exceptions.Timeout(
                        f"Request timed out after {max_retries} attempts. "
                        f"The Rundeck server may be overloaded or unreachable."
                    )
                continue
                
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error: {e}")
                if e.response and e.response.status_code == 401:
                    raise requests.exceptions.HTTPError(
                        "Authentication failed. Please check your RUNDECK_API_TOKEN."
                    )
                elif e.response and e.response.status_code == 403:
                    raise requests.exceptions.HTTPError(
                        "Access forbidden. Please check your API token permissions."
                    )
                elif e.response and e.response.status_code == 404:
                    raise requests.exceptions.HTTPError(
                        f"Resource not found: {url}. Please check the endpoint and API version."
                    )
                else:
                    raise
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON response: {e}")
                if response:
                    logger.error(f"Response content: {response.content[:500]}")
                    content_preview = response.content[:200].decode('utf-8', errors='ignore')
                else:
                    content_preview = "No response content"
                raise ValueError(f"Invalid JSON response from Rundeck server. Response: {content_preview}")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")
                raise
        
        # This should never be reached due to the retry logic, but added for type safety
        raise requests.exceptions.RequestException("Unexpected error in request handling")
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects"""
        response = self._make_request('GET', 'projects')
        return response if isinstance(response, list) else response.get('projects', [])
    
    def get_jobs(self, project: str, job_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get jobs for a project with optional filtering"""
        try:
            params = {}
            if job_filter:
                params['jobFilter'] = job_filter
            
            logger.info(f"Requesting jobs for project: {project}, filter: {job_filter}")
            response = self._make_request('GET', f'project/{project}/jobs', params=params)
            
            if isinstance(response, list):
                logger.info(f"Retrieved {len(response)} jobs successfully")
                return response
            elif isinstance(response, dict):
                jobs = response.get('jobs', [])
                logger.info(f"Retrieved {len(jobs)} jobs from dict response")
                return jobs
            else:
                logger.warning(f"Unexpected response type: {type(response)}")
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving jobs for project {project}: {e}")
            raise
    
    def get_job_definition(self, job_id: str) -> Dict[str, Any]:
        """Get detailed job definition including options and workflow"""
        response = self._make_request('GET', f'job/{job_id}')
        # Handle both list and dict responses
        if isinstance(response, list) and len(response) > 0:
            return response[0]  # type: ignore
        elif isinstance(response, dict):
            return response
        else:
            return {}
    
    def run_job(self, job_id: str, options: Optional[Dict[str, str]] = None, 
                node_filter: Optional[str] = None) -> Dict[str, Any]:
        """Execute a job with optional parameters"""
        data = {}
        if options:
            data['options'] = options
        if node_filter:
            data['filter'] = node_filter
        
        return self._make_request('POST', f'job/{job_id}/run', json=data)
    
    def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Get the status of a job execution"""
        return self._make_request('GET', f'execution/{execution_id}')
    
    def get_execution_output(self, execution_id: str) -> Dict[str, Any]:
        """Get the output of a job execution"""
        return self._make_request('GET', f'execution/{execution_id}/output')
    
    def get_executions(self, project: str, max_results: int = 100,
                      status: Optional[str] = None, user: Optional[str] = None,
                      job_id: Optional[str] = None, recent_filter: Optional[str] = None,
                      offset: int = 0) -> Dict[str, Any]:
        """Get executions for a project with filtering options and pagination support"""
        params: Dict[str, Any] = {'max': min(max_results, 1000), 'offset': offset}
        if status:
            params['statusFilter'] = status
        if user:
            params['userFilter'] = user
        if job_id:
            params['jobIdListFilter'] = job_id
        if recent_filter:
            params['recentFilter'] = recent_filter
        
        response = self._make_request('GET', f'project/{project}/executions', params=params)
        
        # Handle both list and dict responses, normalize to dict with pagination info
        if isinstance(response, list):
            return {
                'executions': response,
                'total': len(response),
                'offset': offset,
                'max': params['max'],
                'hasMore': len(response) == params['max']
            }
        elif isinstance(response, dict):
            executions = response.get('executions', [])
            return {
                'executions': executions,
                'total': response.get('total', len(executions)),
                'offset': offset,
                'max': params['max'],
                'hasMore': len(executions) == params['max']
            }
        else:
            return {
                'executions': [],
                'total': 0,
                'offset': offset,
                'max': params['max'],
                'hasMore': False
            }
    
    def get_all_executions(self, project: str, max_total: int = 5000,
                          status: Optional[str] = None, user: Optional[str] = None,
                          job_id: Optional[str] = None, recent_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all executions with automatic pagination"""
        all_executions = []
        offset = 0
        page_size = 1000
        
        while len(all_executions) < max_total:
            remaining = max_total - len(all_executions)
            current_page_size = min(page_size, remaining)
            
            result = self.get_executions(
                project, current_page_size, status, user, job_id, recent_filter, offset
            )
            
            executions = result['executions']
            if not executions:
                break
                
            all_executions.extend(executions)
            
            if not result['hasMore']:
                break
                
            offset += len(executions)
        
        return all_executions
    
    def get_execution_metrics(self, project: str, days: int = 30) -> Dict[str, Any]:
        """Get execution metrics and analytics for a project"""
        # Get recent executions using the new method
        recent_filter = f"{days}d"  # Last N days
        executions = self.get_all_executions(project, max_total=5000, recent_filter=recent_filter)
        
        if not executions:
            return {
                "total_executions": 0,
                "success_rate": 0,
                "average_duration": 0,
                "metrics_period_days": days
            }
        
        # Calculate metrics
        total_executions = len(executions)
        successful = sum(1 for ex in executions if ex.get('status') == 'succeeded')
        failed = sum(1 for ex in executions if ex.get('status') == 'failed')
        running = sum(1 for ex in executions if ex.get('status') == 'running')
        
        # Calculate durations for completed executions
        durations = []
        for ex in executions:
            if ex.get('date-started') and ex.get('date-ended'):
                try:
                    start = datetime.fromisoformat(ex['date-started']['date'].replace('Z', '+00:00'))
                    end = datetime.fromisoformat(ex['date-ended']['date'].replace('Z', '+00:00'))
                    duration = (end - start).total_seconds()
                    durations.append(duration)
                except (ValueError, KeyError):
                    continue
        
        avg_duration = statistics.mean(durations) if durations else 0
        median_duration = statistics.median(durations) if durations else 0
        
        # Job frequency analysis
        job_counts = defaultdict(int)
        job_success_rates = defaultdict(lambda: {'total': 0, 'successful': 0})
        
        for ex in executions:
            job_name = ex.get('job', {}).get('name', 'Unknown')
            job_counts[job_name] += 1
            job_success_rates[job_name]['total'] += 1
            if ex.get('status') == 'succeeded':
                job_success_rates[job_name]['successful'] += 1
        
        # Calculate success rates per job
        job_analytics = {}
        for job_name, counts in job_success_rates.items():
            success_rate = (counts['successful'] / counts['total']) * 100 if counts['total'] > 0 else 0
            job_analytics[job_name] = {
                'total_executions': counts['total'],
                'successful_executions': counts['successful'],
                'success_rate_percent': round(success_rate, 2)
            }
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful,
            "failed_executions": failed,
            "running_executions": running,
            "success_rate_percent": round((successful / total_executions) * 100, 2) if total_executions > 0 else 0,
            "average_duration_seconds": round(avg_duration, 2),
            "median_duration_seconds": round(median_duration, 2),
            "metrics_period_days": days,
            "most_frequent_jobs": dict(sorted(job_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            "job_success_rates": job_analytics
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get Rundeck system information and health metrics"""
        try:
            response = self._make_request('GET', 'system/info')
            return response
        except Exception as e:
            logger.warning(f"Could not fetch system info: {e}")
            return {"error": str(e)}
    
    def get_project_stats(self, project: str) -> Dict[str, Any]:
        """Get comprehensive project statistics"""
        try:
            # Get basic project info
            projects = self.get_projects()
            project_info = next((p for p in projects if p.get('name') == project), {})
            
            # Get jobs count
            jobs = self.get_jobs(project)
            total_jobs = len(jobs)
            enabled_jobs = sum(1 for job in jobs if job.get('enabled', True))
            scheduled_jobs = sum(1 for job in jobs if job.get('scheduled', False))
            
            # Get execution metrics
            exec_metrics = self.get_execution_metrics(project, days=30)
            
            return {
                "project_name": project,
                "project_description": project_info.get('description', ''),
                "total_jobs": total_jobs,
                "enabled_jobs": enabled_jobs,
                "disabled_jobs": total_jobs - enabled_jobs,
                "scheduled_jobs": scheduled_jobs,
                "execution_metrics_30_days": exec_metrics
            }
        except Exception as e:
            logger.error(f"Error getting project stats: {e}")
            return {"error": str(e)}
    
    def calculate_job_roi(self, project: str, job_id: str,
                         cost_per_hour: float = 50.0, days: int = 30) -> Dict[str, Any]:
        """Calculate ROI metrics for a specific job"""
        try:
            # Get job definition
            job_def = self.get_job_definition(job_id)
            job_name = job_def.get('name', 'Unknown')
            
            # Get executions for this job
            executions = self.get_all_executions(project, max_total=2000,
                                               job_id=job_id, recent_filter=f"{days}d")
            
            if not executions:
                return {
                    "job_id": job_id,
                    "job_name": job_name,
                    "error": "No executions found for ROI calculation"
                }
            
            # Calculate execution costs
            total_duration_hours = 0
            successful_executions = 0
            failed_executions = 0
            
            for ex in executions:
                if ex.get('date-started') and ex.get('date-ended'):
                    try:
                        start = datetime.fromisoformat(ex['date-started']['date'].replace('Z', '+00:00'))
                        end = datetime.fromisoformat(ex['date-ended']['date'].replace('Z', '+00:00'))
                        duration_hours = (end - start).total_seconds() / 3600
                        total_duration_hours += duration_hours
                        
                        if ex.get('status') == 'succeeded':
                            successful_executions += 1
                        elif ex.get('status') == 'failed':
                            failed_executions += 1
                    except (ValueError, KeyError):
                        continue
            
            total_cost = total_duration_hours * cost_per_hour
            success_rate = (successful_executions / len(executions)) * 100 if executions else 0
            
            # Estimate value based on automation benefits
            # Assume each successful execution saves 1 hour of manual work
            estimated_manual_hours_saved = successful_executions * 1.0
            estimated_value_saved = estimated_manual_hours_saved * cost_per_hour
            
            roi_percentage = ((estimated_value_saved - total_cost) / total_cost * 100) if total_cost > 0 else 0
            
            return {
                "job_id": job_id,
                "job_name": job_name,
                "analysis_period_days": days,
                "total_executions": len(executions),
                "successful_executions": successful_executions,
                "failed_executions": failed_executions,
                "success_rate_percent": round(success_rate, 2),
                "total_execution_hours": round(total_duration_hours, 2),
                "total_execution_cost": round(total_cost, 2),
                "estimated_manual_hours_saved": round(estimated_manual_hours_saved, 2),
                "estimated_value_saved": round(estimated_value_saved, 2),
                "roi_percentage": round(roi_percentage, 2),
                "cost_per_hour_used": cost_per_hour
            }
        except Exception as e:
            logger.error(f"Error calculating job ROI: {e}")
            return {"error": str(e)}
    
    def get_bulk_execution_status(self, execution_ids: List[str]) -> List[Dict[str, Any]]:
        """Get status for multiple executions efficiently"""
        results = []
        for exec_id in execution_ids:
            try:
                status = self.get_execution_status(exec_id)
                results.append(status)
            except Exception as e:
                results.append({"id": exec_id, "error": str(e)})
        return results
    
    def run_job_with_monitoring(self, job_id: str, options: Optional[Dict[str, str]] = None,
                               node_filter: Optional[str] = None,
                               wait_for_completion: bool = False,
                               timeout_minutes: int = 30) -> Dict[str, Any]:
        """Execute a job with optional monitoring until completion"""
        import time
        
        # Start the job
        execution = self.run_job(job_id, options, node_filter)
        execution_id = execution.get('id')
        
        if not wait_for_completion or not execution_id:
            return execution
        
        # Monitor execution
        start_time = datetime.now()
        timeout = timedelta(minutes=timeout_minutes)
        
        while datetime.now() - start_time < timeout:
            try:
                status = self.get_execution_status(str(execution_id))
                current_status = status.get('status')
                
                if current_status in ['succeeded', 'failed', 'aborted', 'timedout']:
                    # Execution completed
                    return {
                        **execution,
                        "final_status": status,
                        "monitoring_completed": True,
                        "total_wait_time_seconds": (datetime.now() - start_time).total_seconds()
                    }
                
                # Wait before next check
                time.sleep(5)
                
            except Exception as e:
                logger.warning(f"Error monitoring execution {execution_id}: {e}")
                break
        
        # Timeout reached
        return {
            **execution,
            "monitoring_completed": False,
            "timeout_reached": True,
            "timeout_minutes": timeout_minutes
        }


# Initialize the MCP server
server = Server("rundeck-mcp-server")

# Global Rundeck clients (multiple servers support)
rundeck_clients: Dict[str, RundeckClient] = {}

# Global tool prompts
tool_prompts: Dict[str, Dict[str, str]] = {}


def load_tool_prompts():
    """Load tool prompts from external JSON file"""
    global tool_prompts
    
    prompts_file = Path(__file__).parent / "tool_prompts.json"
    try:
        with open(prompts_file, 'r') as f:
            tool_prompts = json.load(f)
        logger.info(f"Loaded tool prompts from {prompts_file}")
    except FileNotFoundError:
        logger.warning(f"Tool prompts file not found: {prompts_file}")
        tool_prompts = {}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing tool prompts JSON: {e}")
        tool_prompts = {}


def initialize_rundeck_clients():
    """Initialize Rundeck clients from environment variables (supports multiple servers)"""
    global rundeck_clients
    
    # Clear existing clients
    rundeck_clients = {}
    
    # Check for single server configuration (backward compatibility)
    base_url = os.getenv('RUNDECK_URL')
    api_token = os.getenv('RUNDECK_API_TOKEN')
    api_version = os.getenv('RUNDECK_API_VERSION', '47')
    
    if base_url and api_token:
        # Single server configuration
        client = RundeckClient(base_url, api_token, api_version)
        rundeck_clients['default'] = client
        logger.info(f"Initialized default Rundeck client for {base_url}")
    
    # Check for multiple server configuration
    server_count = 0
    for i in range(1, 10):  # Support up to 9 additional servers
        url_key = f'RUNDECK_URL_{i}'
        token_key = f'RUNDECK_API_TOKEN_{i}'
        version_key = f'RUNDECK_API_VERSION_{i}'
        name_key = f'RUNDECK_NAME_{i}'
        
        server_url = os.getenv(url_key)
        server_token = os.getenv(token_key)
        server_version = os.getenv(version_key, '47')
        server_name = os.getenv(name_key, f'server_{i}')
        
        if server_url and server_token:
            client = RundeckClient(server_url, server_token, server_version)
            rundeck_clients[server_name] = client
            logger.info(f"Initialized Rundeck client '{server_name}' for {server_url}")
            server_count += 1
    
    if not rundeck_clients:
        raise ValueError(
            "No Rundeck servers configured. Set RUNDECK_URL and RUNDECK_API_TOKEN "
            "for single server, or RUNDECK_URL_1, RUNDECK_API_TOKEN_1, etc. for multiple servers"
        )
    
    logger.info(f"Initialized {len(rundeck_clients)} Rundeck client(s)")


def get_rundeck_client(server_name: Optional[str] = None) -> RundeckClient:
    """Get a Rundeck client by name, or default if not specified"""
    if not rundeck_clients:
        raise ValueError("No Rundeck clients initialized")
    
    if server_name is None:
        # Return default client or first available
        if 'default' in rundeck_clients:
            return rundeck_clients['default']
        else:
            return next(iter(rundeck_clients.values()))
    
    if server_name not in rundeck_clients:
        available = list(rundeck_clients.keys())
        raise ValueError(f"Rundeck server '{server_name}' not found. Available servers: {available}")
    
    return rundeck_clients[server_name]


def list_rundeck_servers() -> List[str]:
    """Get list of configured Rundeck server names"""
    return list(rundeck_clients.keys())


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools"""
    
    def get_tool_description(tool_name: str, fallback: str) -> str:
        """Get description from external prompts or use fallback"""
        if tool_name in tool_prompts:
            prompt_info = tool_prompts[tool_name]
            return f"{prompt_info.get('description', fallback)}\n\n{prompt_info.get('prompt', '')}"
        return fallback
    
    return [
        Tool(
            name="list_servers",
            description="List all configured Rundeck servers",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_projects",
            description=get_tool_description("get_projects", "Get all Rundeck projects"),
            inputSchema={
                "type": "object",
                "properties": {
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_jobs",
            description=get_tool_description("get_jobs", "Get jobs from a Rundeck project with optional filtering"),
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "The project name"
                    },
                    "job_filter": {
                        "type": "string",
                        "description": "Optional job name filter"
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["project"]
            }
        ),
        Tool(
            name="get_job_definition",
            description=get_tool_description("get_job_definition", "Get detailed job definition including options, workflow, and metadata"),
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "The job ID or UUID"
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["job_id"]
            }
        ),
        Tool(
            name="run_job",
            description=get_tool_description("run_job", "Execute a Rundeck job with optional parameters"),
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "The job ID or UUID to execute"
                    },
                    "options": {
                        "type": "object",
                        "description": "Job options as key-value pairs",
                        "additionalProperties": {"type": "string"}
                    },
                    "node_filter": {
                        "type": "string",
                        "description": "Optional node filter for job execution"
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["job_id"]
            }
        ),
        Tool(
            name="get_execution_status",
            description=get_tool_description("get_execution_status", "Get the status and details of a job execution"),
            inputSchema={
                "type": "object",
                "properties": {
                    "execution_id": {
                        "type": "string",
                        "description": "The execution ID"
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["execution_id"]
            }
        ),
        Tool(
            name="get_execution_output",
            description=get_tool_description("get_execution_output", "Get the output logs of a job execution"),
            inputSchema={
                "type": "object",
                "properties": {
                    "execution_id": {
                        "type": "string",
                        "description": "The execution ID"
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["execution_id"]
            }
        ),
        Tool(
            name="get_executions",
            description=get_tool_description("get_executions", "Get executions for a project with filtering options"),
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "The project name"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return per page",
                        "default": 100
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by execution status (succeeded, failed, running, etc.)"
                    },
                    "user": {
                        "type": "string",
                        "description": "Filter by user who executed the job"
                    },
                    "job_id": {
                        "type": "string",
                        "description": "Filter by specific job ID"
                    },
                    "recent_filter": {
                        "type": "string",
                        "description": "Recent time filter (e.g., '1d', '7d', '30d')"
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset for pagination (0-based)",
                        "default": 0
                    },
                    "summary_only": {
                        "type": "boolean",
                        "description": "Return only summary information instead of full execution details",
                        "default": True
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["project"]
            }
        ),
        Tool(
            name="get_all_executions",
            description=get_tool_description("get_all_executions", "Get all executions with automatic pagination (up to specified limit)"),
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "The project name"
                    },
                    "max_total": {
                        "type": "integer",
                        "description": "Maximum total number of executions to retrieve",
                        "default": 5000
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by execution status (succeeded, failed, running, etc.)"
                    },
                    "user": {
                        "type": "string",
                        "description": "Filter by user who executed the job"
                    },
                    "job_id": {
                        "type": "string",
                        "description": "Filter by specific job ID"
                    },
                    "recent_filter": {
                        "type": "string",
                        "description": "Recent time filter (e.g., '1d', '7d', '30d')"
                    },
                    "summary_only": {
                        "type": "boolean",
                        "description": "Return only summary information instead of full execution details",
                        "default": True
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["project"]
            }
        ),
        Tool(
            name="get_execution_metrics",
            description=get_tool_description("get_execution_metrics", "Get comprehensive execution metrics and analytics for a project"),
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "The project name"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to analyze",
                        "default": 30
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["project"]
            }
        ),
        Tool(
            name="get_system_info",
            description=get_tool_description("get_system_info", "Get Rundeck system information and health metrics"),
            inputSchema={
                "type": "object",
                "properties": {
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_project_stats",
            description=get_tool_description("get_project_stats", "Get comprehensive statistics for a project including jobs and execution metrics"),
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "The project name"
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["project"]
            }
        ),
        Tool(
            name="calculate_job_roi",
            description=get_tool_description("calculate_job_roi", "Calculate ROI metrics for a specific job including cost analysis and value estimation"),
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "The project name"
                    },
                    "job_id": {
                        "type": "string",
                        "description": "The job ID to analyze"
                    },
                    "cost_per_hour": {
                        "type": "number",
                        "description": "Cost per hour for execution resources",
                        "default": 50.0
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to analyze",
                        "default": 30
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["project", "job_id"]
            }
        ),
        Tool(
            name="get_bulk_execution_status",
            description=get_tool_description("get_bulk_execution_status", "Get status for multiple executions efficiently"),
            inputSchema={
                "type": "object",
                "properties": {
                    "execution_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of execution IDs to check"
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["execution_ids"]
            }
        ),
        Tool(
            name="run_job_with_monitoring",
            description=get_tool_description("run_job_with_monitoring", "Execute a job with optional monitoring until completion"),
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "The job ID to execute"
                    },
                    "options": {
                        "type": "object",
                        "description": "Job options as key-value pairs",
                        "additionalProperties": {"type": "string"}
                    },
                    "node_filter": {
                        "type": "string",
                        "description": "Optional node filter for job execution"
                    },
                    "wait_for_completion": {
                        "type": "boolean",
                        "description": "Whether to wait and monitor until job completion"
                    },
                    "timeout_minutes": {
                        "type": "integer",
                        "description": "Timeout in minutes for monitoring",
                        "default": 30
                    },
                    "server": {
                        "type": "string",
                        "description": "Rundeck server name (optional, uses default if not specified)"
                    }
                },
                "required": ["job_id"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool calls"""
    if not rundeck_clients:
        return [TextContent(
            type="text",
            text="Error: No Rundeck clients initialized. Please configure RUNDECK_URL and RUNDECK_API_TOKEN environment variables."
        )]
    
    try:
        if name == "list_servers":
            servers = list_rundeck_servers()
            text_lines = []
            text_lines.append("🖥️  Configured Rundeck Servers:")
            text_lines.append("=" * 40)
            
            for i, server_name in enumerate(servers, 1):
                client = rundeck_clients[server_name]
                text_lines.append(f"{i}. {server_name}")
                text_lines.append(f"   URL: {client.base_url}")
                text_lines.append(f"   API Version: {client.api_version}")
                text_lines.append("")
            
            return [TextContent(
                type="text",
                text="\n".join(text_lines)
            )]
        
        elif name == "get_projects":
            server_name = arguments.get("server")
            client = get_rundeck_client(server_name)
            projects = client.get_projects()
            return [TextContent(
                type="text",
                text=json.dumps(projects, indent=2)
            )]
        
        elif name == "get_jobs":
            project = arguments["project"]
            job_filter = arguments.get("job_filter")
            server_name = arguments.get("server")
            
            try:
                client = get_rundeck_client(server_name)
                jobs = client.get_jobs(project, job_filter)
                
                # Format as human-readable text
                text_lines = []
                text_lines.append(f"📋 Jobs in Project: {project}")
                if job_filter:
                    text_lines.append(f"🔍 Filter: {job_filter}")
                text_lines.append(f"📊 Total Jobs Found: {len(jobs)}")
                text_lines.append("")
                
                if not jobs:
                    text_lines.append("No jobs found in this project.")
                    text_lines.append("")
                    text_lines.append("💡 Possible reasons:")
                    text_lines.append("  • Project has no jobs defined")
                    text_lines.append("  • Job filter is too restrictive")
                    text_lines.append("  • API token lacks 'read' permission for jobs")
                    text_lines.append("  • Project name is incorrect")
                else:
                    # Group jobs by group
                    job_groups = {}
                    for job in jobs:
                        group = job.get("group", "")
                        if group not in job_groups:
                            job_groups[group] = []
                        job_groups[group].append(job)
                    
                    for group_name in sorted(job_groups.keys()):
                        if group_name:
                            text_lines.append(f"📁 Group: {group_name}")
                        else:
                            text_lines.append("📁 Root Level Jobs")
                        text_lines.append("-" * 60)
                        
                        for job in job_groups[group_name]:
                            enabled_icon = "✅" if job.get("enabled", True) else "❌"
                            scheduled_icon = "⏰" if job.get("scheduled", False) else "🔧"
                            
                            text_lines.append(f"  {enabled_icon} {scheduled_icon} {job.get('name', 'Unknown')}")
                            text_lines.append(f"    ID: {job.get('id', 'Unknown')}")
                            
                            if job.get("description"):
                                desc = job.get("description", "")
                                if len(desc) > 80:
                                    desc = desc[:80] + "..."
                                text_lines.append(f"    Description: {desc}")
                            
                            if job.get("tags"):
                                tags = ", ".join(job.get("tags", []))
                                text_lines.append(f"    Tags: {tags}")
                            text_lines.append("")
                        
                        text_lines.append("")
                
                return [TextContent(
                    type="text",
                    text="\n".join(text_lines)
                )]
                
            except Exception as e:
                error_text = f"❌ Error retrieving jobs for project '{project}': {str(e)}\n\n"
                error_text += "💡 Troubleshooting steps:\n"
                error_text += "  • Verify project name is correct\n"
                error_text += "  • Check API token has 'read' permission for jobs\n"
                error_text += "  • Ensure Rundeck server is accessible\n"
                error_text += "  • Try get_projects tool to verify connection"
                
                return [TextContent(
                    type="text",
                    text=error_text
                )]
        
        elif name == "get_job_definition":
            job_id = arguments["job_id"]
            server_name = arguments.get("server")
            client = get_rundeck_client(server_name)
            job_def = client.get_job_definition(job_id)
            
            # Extract key information including options
            formatted_def = {
                "id": job_def.get("id"),
                "name": job_def.get("name"),
                "group": job_def.get("group"),
                "description": job_def.get("description"),
                "project": job_def.get("project"),
                "enabled": job_def.get("enabled"),
                "tags": job_def.get("tags", []),
                "options": job_def.get("options", []),
                "sequence": job_def.get("sequence", {}),
                "nodeFilterEditable": job_def.get("nodeFilterEditable"),
                "scheduleEnabled": job_def.get("scheduleEnabled"),
                "schedule": job_def.get("schedule"),
                "notification": job_def.get("notification")
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(formatted_def, indent=2)
            )]
        
        elif name == "run_job":
            job_id = arguments["job_id"]
            options = arguments.get("options", {})
            node_filter = arguments.get("node_filter")
            server_name = arguments.get("server")
            
            client = get_rundeck_client(server_name)
            execution = client.run_job(job_id, options, node_filter)
            
            return [TextContent(
                type="text",
                text=json.dumps(execution, indent=2)
            )]
        
        elif name == "get_execution_status":
            execution_id = arguments["execution_id"]
            server_name = arguments.get("server")
            client = get_rundeck_client(server_name)
            status = client.get_execution_status(execution_id)
            
            # Format key status information
            formatted_status = {
                "id": status.get("id"),
                "status": status.get("status"),
                "project": status.get("project"),
                "user": status.get("user"),
                "date-started": status.get("date-started"),
                "date-ended": status.get("date-ended"),
                "job": {
                    "id": status.get("job", {}).get("id"),
                    "name": status.get("job", {}).get("name"),
                    "group": status.get("job", {}).get("group")
                },
                "description": status.get("description"),
                "argstring": status.get("argstring"),
                "successfulNodes": status.get("successfulNodes", []),
                "failedNodes": status.get("failedNodes", [])
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(formatted_status, indent=2)
            )]
        
        elif name == "get_execution_output":
            execution_id = arguments["execution_id"]
            server_name = arguments.get("server")
            client = get_rundeck_client(server_name)
            output = client.get_execution_output(execution_id)
            
            return [TextContent(
                type="text",
                text=json.dumps(output, indent=2)
            )]
        
        elif name == "get_executions":
            project = arguments["project"]
            max_results = arguments.get("max_results", 100)
            status = arguments.get("status")
            user = arguments.get("user")
            job_id = arguments.get("job_id")
            recent_filter = arguments.get("recent_filter")
            offset = arguments.get("offset", 0)
            summary_only = arguments.get("summary_only", True)
            server_name = arguments.get("server")
            
            client = get_rundeck_client(server_name)
            result = client.get_executions(
                project, max_results, status, user, job_id, recent_filter, offset
            )
            
            executions = result['executions']
            
            if summary_only:
                # Format as human-readable text
                text_lines = []
                text_lines.append(f"📊 Execution Results for Project: {project}")
                text_lines.append(f"📄 Page Info: {len(executions)} executions returned (offset: {result['offset']}, max per page: {result['max']})")
                if result['hasMore']:
                    text_lines.append("➡️  More results available - use offset parameter to get next page")
                text_lines.append("")
                
                if not executions:
                    text_lines.append("No executions found matching the criteria.")
                else:
                    text_lines.append("🔍 Execution Summary:")
                    text_lines.append("-" * 80)
                    
                    for i, ex in enumerate(executions, 1):
                        status_emoji = {
                            'succeeded': '✅',
                            'failed': '❌',
                            'running': '🔄',
                            'aborted': '⏹️',
                            'timedout': '⏰'
                        }.get(ex.get("status", ""), '❓')
                        
                        job_info = ex.get("job", {})
                        job_name = job_info.get("name", "Unknown Job")
                        job_group = job_info.get("group", "")
                        job_display = f"{job_group}/{job_name}" if job_group else job_name
                        
                        started = ex.get("date-started", {}).get("date", "Unknown") if ex.get("date-started") else "Unknown"
                        user = ex.get("user", "Unknown")
                        exec_id = ex.get("id", "Unknown")
                        
                        text_lines.append(f"{i:3d}. {status_emoji} {job_display}")
                        text_lines.append(f"     ID: {exec_id} | User: {user} | Started: {started}")
                        
                        if ex.get("description"):
                            desc = ex.get("description", "")
                            if len(desc) > 60:
                                desc = desc[:60] + "..."
                            text_lines.append(f"     Description: {desc}")
                        text_lines.append("")
                
                return [TextContent(
                    type="text",
                    text="\n".join(text_lines)
                )]
            else:
                # Return full details
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
        
        elif name == "get_all_executions":
            project = arguments["project"]
            max_total = arguments.get("max_total", 5000)
            status = arguments.get("status")
            user = arguments.get("user")
            job_id = arguments.get("job_id")
            recent_filter = arguments.get("recent_filter")
            summary_only = arguments.get("summary_only", True)
            server_name = arguments.get("server")
            
            client = get_rundeck_client(server_name)
            executions = client.get_all_executions(
                project, max_total, status, user, job_id, recent_filter
            )
            
            if summary_only:
                # Format as human-readable text
                text_lines = []
                text_lines.append(f"📊 All Executions for Project: {project}")
                text_lines.append(f"📈 Total Retrieved: {len(executions)} executions (max requested: {max_total})")
                text_lines.append("")
                
                if not executions:
                    text_lines.append("No executions found matching the criteria.")
                else:
                    # Status summary
                    status_counts = {}
                    for ex in executions:
                        status = ex.get("status", "unknown")
                        status_counts[status] = status_counts.get(status, 0) + 1
                    
                    text_lines.append("📊 Status Summary:")
                    for status, count in sorted(status_counts.items()):
                        emoji = {
                            'succeeded': '✅',
                            'failed': '❌',
                            'running': '🔄',
                            'aborted': '⏹️',
                            'timedout': '⏰'
                        }.get(status, '❓')
                        text_lines.append(f"  {emoji} {status}: {count}")
                    text_lines.append("")
                    
                    # Show first 20 executions in detail
                    display_count = min(20, len(executions))
                    text_lines.append(f"🔍 Recent {display_count} Executions:")
                    text_lines.append("-" * 80)
                    
                    for i, ex in enumerate(executions[:display_count], 1):
                        status_emoji = {
                            'succeeded': '✅',
                            'failed': '❌',
                            'running': '🔄',
                            'aborted': '⏹️',
                            'timedout': '⏰'
                        }.get(ex.get("status", ""), '❓')
                        
                        job_info = ex.get("job", {})
                        job_name = job_info.get("name", "Unknown Job")
                        job_group = job_info.get("group", "")
                        job_display = f"{job_group}/{job_name}" if job_group else job_name
                        
                        started = ex.get("date-started", {}).get("date", "Unknown") if ex.get("date-started") else "Unknown"
                        user = ex.get("user", "Unknown")
                        exec_id = ex.get("id", "Unknown")
                        
                        text_lines.append(f"{i:3d}. {status_emoji} {job_display}")
                        text_lines.append(f"     ID: {exec_id} | User: {user} | Started: {started}")
                        text_lines.append("")
                    
                    if len(executions) > display_count:
                        text_lines.append(f"... and {len(executions) - display_count} more executions")
                
                return [TextContent(
                    type="text",
                    text="\n".join(text_lines)
                )]
            else:
                # Return full details
                return [TextContent(
                    type="text",
                    text=json.dumps(executions, indent=2)
                )]
        
        elif name == "get_execution_metrics":
            project = arguments["project"]
            days = arguments.get("days", 30)
            server_name = arguments.get("server")
            
            client = get_rundeck_client(server_name)
            metrics = client.get_execution_metrics(project, days)
            
            return [TextContent(
                type="text",
                text=json.dumps(metrics, indent=2)
            )]
        
        elif name == "get_system_info":
            server_name = arguments.get("server")
            client = get_rundeck_client(server_name)
            system_info = client.get_system_info()
            
            return [TextContent(
                type="text",
                text=json.dumps(system_info, indent=2)
            )]
        
        elif name == "get_project_stats":
            project = arguments["project"]
            server_name = arguments.get("server")
            
            client = get_rundeck_client(server_name)
            stats = client.get_project_stats(project)
            
            return [TextContent(
                type="text",
                text=json.dumps(stats, indent=2)
            )]
        
        elif name == "calculate_job_roi":
            project = arguments["project"]
            job_id = arguments["job_id"]
            cost_per_hour = arguments.get("cost_per_hour", 50.0)
            days = arguments.get("days", 30)
            server_name = arguments.get("server")
            
            client = get_rundeck_client(server_name)
            roi_data = client.calculate_job_roi(project, job_id, cost_per_hour, days)
            
            return [TextContent(
                type="text",
                text=json.dumps(roi_data, indent=2)
            )]
        
        elif name == "get_bulk_execution_status":
            execution_ids = arguments["execution_ids"]
            server_name = arguments.get("server")
            
            client = get_rundeck_client(server_name)
            statuses = client.get_bulk_execution_status(execution_ids)
            
            return [TextContent(
                type="text",
                text=json.dumps(statuses, indent=2)
            )]
        
        elif name == "run_job_with_monitoring":
            job_id = arguments["job_id"]
            options = arguments.get("options", {})
            node_filter = arguments.get("node_filter")
            wait_for_completion = arguments.get("wait_for_completion", False)
            timeout_minutes = arguments.get("timeout_minutes", 30)
            server_name = arguments.get("server")
            
            client = get_rundeck_client(server_name)
            execution = client.run_job_with_monitoring(
                job_id, options, node_filter, wait_for_completion, timeout_minutes
            )
            
            return [TextContent(
                type="text",
                text=json.dumps(execution, indent=2)
            )]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


@server.list_prompts()
async def handle_list_prompts() -> List[Any]:
    """List available prompts"""
    return []


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
    """Get a specific prompt"""
    return {"messages": []}


async def main():
    """Main entry point"""
    try:
        load_tool_prompts()
        initialize_rundeck_clients()
    except ValueError as e:
        logger.error(f"Failed to initialize Rundeck client: {e}")
        return
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="rundeck-mcp-server",
                server_version="1.0.0",
                capabilities=ServerCapabilities(
                    tools=ToolsCapability(),
                    prompts=PromptsCapability()
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())