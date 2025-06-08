# 🚀 Rundeck MCP Server

```
██████╗ ██╗   ██╗███╗   ██╗██████╗ ███████╗ ██████╗██╗  ██╗    ███╗   ███╗ ██████╗██████╗ 
██╔══██╗██║   ██║████╗  ██║██╔══██╗██╔════╝██╔════╝██║ ██╔╝    ████╗ ████║██╔════╝██╔══██╗
██████╔╝██║   ██║██╔██╗ ██║██║  ██║█████╗  ██║     █████╔╝     ██╔████╔██║██║     ██████╔╝
██╔══██╗██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██║     ██╔═██╗     ██║╚██╔╝██║██║     ██╔═══╝ 
██║  ██║╚██████╔╝██║ ╚████║██████╔╝███████╗╚██████╗██║  ██╗    ██║ ╚═╝ ██║╚██████╗██║     
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝    ╚═╝     ╚═╝ ╚═════╝╚═╝     
```

**A Model Context Protocol (MCP) server for Rundeck and Runbook Automation**

![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status: Experimental](https://img.shields.io/badge/Status-Experimental-orange.svg)

---

## ⚠️ **EXPERIMENTAL PROJECT** ⚠️

**This is an experimental project built for learning and exploration purposes.**  
**Not officially supported by PagerDuty or Rundeck.**

---

## 🌟 Overview

Transform your Rundeck and Runbook Automation with AI-powered job management! This MCP server bridges the gap between Claude AI and your automation infrastructure, enabling intelligent automation workflows, comprehensive analytics, and ROI analysis.

**Compatible with:**
- 🏢 **Rundeck Enterprise** (full feature support)
- ☁️ **Runbook Automation** (PagerDuty's cloud offering)
- 🏠 **Runbook Automation Self-Hosted** (on-premises deployment)
- 🆓 **Rundeck Community** (limited features - see compatibility notes below)

> 🔬 **Built as an Experiment**: This project was created to explore the possibilities of integrating AI with DevOps automation tools. While functional, it's designed for experimentation and learning.

## ✨ Features

### 🎯 Core Job Management
- **🏗️ Project Management**: List and explore all Rundeck projects
- **⚙️ Job Discovery**: Find jobs with intelligent filtering
- **📋 Job Definitions**: Get detailed job configurations and workflows
- **🚀 Job Execution**: Run jobs with custom parameters and node filters
- **📊 Execution Monitoring**: Track job status and retrieve output logs

### 📈 Advanced Analytics & Monitoring
- **📊 Execution Analytics**: Comprehensive success rates and performance metrics
- **🔍 Smart Filtering**: Advanced execution queries with pagination
- **🏥 System Health**: Monitor Rundeck system status and resources
- **📋 Project Statistics**: Detailed project insights and job counts
- **⏱️ Real-time Monitoring**: Live job execution tracking

### 💰 ROI & Cost Analysis *(Enterprise/Commercial versions only)*
- **💵 Cost Calculation**: Analyze automation costs vs manual work
- **📈 ROI Metrics**: Calculate return on automation investment
- **🎯 Value Assessment**: Quantify time and resource savings
- **📊 Business Intelligence**: Transform data into actionable insights

> ⚠️ **Note**: ROI and advanced analytics features require commercial versions (Rundeck Enterprise, Runbook Automation). These features are not available in Rundeck Community Edition.

### 🔧 Enhanced Capabilities
- **🔄 Multi-Server Support**: Manage multiple Rundeck environments
- **⚡ Bulk Operations**: Efficient batch status checking
- **🎛️ Customizable Prompts**: Externalized tool descriptions
- **🔐 Secure Configuration**: Environment-based credential management

## 🚨 Important Disclaimers

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  EXPERIMENTAL SOFTWARE                                      │
│                                                                 │
│  • This project is NOT officially supported by PagerDuty       │
│  • This project is NOT officially supported by Rundeck         │
│  • Built as a learning experiment and proof of concept         │
│  • Use at your own risk in production environments             │
│  • No warranty or support guarantees provided                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Platform Compatibility

### Feature Matrix

| Feature | Rundeck Community | Rundeck Enterprise | Runbook Automation | Runbook Automation Self-Hosted |
|---------|-------------------|-------------------|-------------------|--------------------------------|
| ✅ Core Job Management | ✅ Full Support | ✅ Full Support | ✅ Full Support | ✅ Full Support |
| ✅ Project Management | ✅ Full Support | ✅ Full Support | ✅ Full Support | ✅ Full Support |
| ✅ Job Execution | ✅ Full Support | ✅ Full Support | ✅ Full Support | ✅ Full Support |
| ✅ Basic Analytics | ✅ Full Support | ✅ Full Support | ✅ Full Support | ✅ Full Support |
| ✅ Multi-Server Support | ✅ Full Support | ✅ Full Support | ✅ Full Support | ✅ Full Support |
| 💰 ROI Analysis | ❌ Not Available | ✅ Full Support | ✅ Full Support | ✅ Full Support |
| 📊 Advanced Analytics | ❌ Limited | ✅ Full Support | ✅ Full Support | ✅ Full Support |
| 🏥 System Health Metrics | ❌ Limited | ✅ Full Support | ✅ Full Support | ✅ Full Support |

### Notes
- **Rundeck Community**: Free version with core automation features
- **Rundeck Enterprise**: Commercial version with full feature set
- **Runbook Automation**: PagerDuty's cloud-hosted automation platform
- **Runbook Automation Self-Hosted**: On-premises deployment of PagerDuty's platform

## �️ Quick Start

### 📋 Prerequisites

- 🐍 Python 3.8 or higher
- 🏗️ Rundeck server with API access
- 🔑 Valid Rundeck API token
- 🖥️ Linux environment (recommended)

### ⚡ Installation

#### 🚀 Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/rundeck-mcp-server.git
cd rundeck-mcp-server

# Run the automated setup
chmod +x setup.sh
./setup.sh

# Configure your environment
nano .env
```

#### 🔧 Manual Installation

```bash
# Clone and setup
git clone https://github.com/your-username/rundeck-mcp-server.git
cd rundeck-mcp-server

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp config.env.example .env
# Edit .env with your settings
```

#### 📦 Package Installation

```bash
# Development installation
git clone https://github.com/your-username/rundeck-mcp-server.git
cd rundeck-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

#### 🛠️ Using Make

```bash
# Quick development setup
make dev-setup

# Or individual commands
make install          # Basic installation
make dev-install      # Development installation
make test            # Run tests
make configure-claude # Setup Claude Desktop
```

### 🔧 Configuration

#### 🏢 Single Server Setup

```bash
# Edit your .env file
RUNDECK_URL=https://your-rundeck-server.com
RUNDECK_API_TOKEN=your-api-token-here
RUNDECK_API_VERSION=47
RUNDECK_NAME=production
```

#### 🌐 Multi-Server Setup

```bash
# Primary server
RUNDECK_URL=https://rundeck-main.company.com
RUNDECK_API_TOKEN=main-token
RUNDECK_API_VERSION=47
RUNDECK_NAME=main

# Additional environments
RUNDECK_URL_1=https://rundeck-prod.company.com
RUNDECK_API_TOKEN_1=prod-token
RUNDECK_API_VERSION_1=47
RUNDECK_NAME_1=production

RUNDECK_URL_2=https://rundeck-staging.company.com
RUNDECK_API_TOKEN_2=staging-token
RUNDECK_API_VERSION_2=47
RUNDECK_NAME_2=staging
```

### 🧪 Testing

```bash
# Test your setup
source .venv/bin/activate
python tests/test_server.py

# Test multi-server configuration
python tests/test_multi_server.py
```

## 🤖 Claude Desktop Integration

### 🎯 Automatic Configuration

```bash
# Generate Claude Desktop configuration
source .venv/bin/activate
python tests/get_claude_config.py
```

### 📝 Manual Configuration

Add to your Claude Desktop config file:

**📍 Config Locations:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "rundeck": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/rundeck_mcp_server.py"],
      "env": {
        "RUNDECK_URL": "https://your-rundeck-server.com",
        "RUNDECK_API_TOKEN": "your-api-token",
        "RUNDECK_API_VERSION": "47"
      }
    }
  }
}
```

## 🎮 Usage Examples

### 🏗️ Project & Job Management

```
# List all servers
Use the list_servers tool

# Get all projects
Use the get_projects tool

# Find backup jobs
Use the get_jobs tool with:
- project: "infrastructure"
- job_filter: "backup"

# Get job details
Use the get_job_definition tool with:
- job_id: "your-job-uuid"
```

### 🚀 Job Execution

```
# Run a job
Use the run_job tool with:
- job_id: "your-job-uuid"
- options: {"environment": "production"}

# Monitor execution
Use the run_job_with_monitoring tool with:
- job_id: "your-job-uuid"
- wait_for_completion: true
- timeout_minutes: 30
```

### 📊 Analytics & Reporting

```
# Get execution metrics
Use the get_execution_metrics tool with:
- project: "my-project"
- days: 30

# Calculate ROI
Use the calculate_job_roi tool with:
- project: "my-project"
- job_id: "automation-job-uuid"
- cost_per_hour: 75.0

# Project health report
Use the get_project_stats tool with:
- project: "my-project"
```

## 🛠️ Available Tools

### Complete Tools Reference

| Tool | Category | Description | Commercial Only |
|------|----------|-------------|-----------------|
| `list_servers` | 🖥️ **Server Management** | List all configured Rundeck servers | ❌ |
| `get_projects` | 🏗️ **Project Management** | Get all available Rundeck projects | ❌ |
| `get_jobs` | ⚙️ **Job Management** | Get jobs from a project with filtering | ❌ |
| `get_job_definition` | 📋 **Job Management** | Get detailed job definition and workflow | ❌ |
| `run_job` | 🚀 **Job Execution** | Execute a job with optional parameters | ❌ |
| `run_job_with_monitoring` | 🚀 **Job Execution** | Execute job with monitoring until completion | ❌ |
| `get_execution_status` | 📊 **Execution Monitoring** | Get status and details of job execution | ❌ |
| `get_execution_output` | 📄 **Execution Monitoring** | Get complete output logs from execution | ❌ |
| `get_executions` | 📈 **Analytics** | Get execution history with filtering/pagination | ❌ |
| `get_all_executions` | 📈 **Analytics** | Get all executions with automatic pagination | ❌ |
| `get_bulk_execution_status` | 📊 **Execution Monitoring** | Check status for multiple executions | ❌ |
| `get_execution_metrics` | 📊 **Analytics** | Get comprehensive execution analytics | ⚠️ Limited |
| `get_system_info` | 🏥 **System Health** | Get Rundeck system information and health | ⚠️ Limited |
| `get_project_stats` | 📋 **Analytics** | Get comprehensive project statistics | ⚠️ Limited |
| `calculate_job_roi` | 💰 **ROI Analysis** | Calculate ROI metrics and cost analysis | ✅ Yes |

**Legend:**
- ❌ **Available on all platforms** (including Rundeck Community)
- ⚠️ **Limited on Community** (reduced functionality on free version)
- ✅ **Commercial only** (Rundeck Enterprise, Runbook Automation only)

## 💡 Example Questions You Can Ask

### 🏗️ Project & Infrastructure Questions
1. **"What Rundeck servers do I have configured?"**
   - Lists all your configured servers with their details

2. **"Show me all projects in my Rundeck instance"**
   - Displays all available projects across your servers

3. **"What jobs are available in the 'infrastructure' project?"**
   - Lists all jobs in a specific project with their status

### ⚙️ Job Management Questions
4. **"Show me the details of job 'backup-database'"**
   - Provides complete job definition, workflow, and options

5. **"Run the 'deploy-application' job with environment=staging"**
   - Executes a job with specific parameters

6. **"What are the required options for the 'server-maintenance' job?"**
   - Shows job parameters and their requirements

### 📊 Monitoring & Status Questions
7. **"What's the status of execution ID 12345?"**
   - Checks current status of a running or completed job

8. **"Show me the output logs from the last deployment job"**
   - Retrieves execution logs for troubleshooting

9. **"What jobs have run in the last 24 hours?"**
   - Lists recent executions with their status

### 📈 Analytics & Reporting Questions
10. **"Give me execution metrics for the 'production' project over the last 30 days"**
    - Provides comprehensive analytics and success rates

11. **"Which jobs fail most frequently in my environment?"**
    - Identifies problematic jobs needing attention

12. **"Show me project statistics for 'infrastructure'"**
    - Comprehensive project health overview

### 💰 ROI & Cost Analysis Questions *(Commercial versions only)*
13. **"Calculate the ROI for my 'automated-backup' job"**
    - Analyzes cost savings and automation value

14. **"What's the cost impact of running deployment jobs daily?"**
    - Estimates operational costs and savings

### 🔧 Advanced Operations Questions
15. **"Run the 'system-health-check' job and wait for completion"**
    - Executes job with real-time monitoring until finished

## � Documentation

| Document | Description |
|----------|-------------|
| 📖 [`INSTALL.md`](INSTALL.md) | Comprehensive installation guide |
| 🔧 [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) | Common issues and solutions |
| 🖥️ [`docs/CLAUDE_MULTIPLE_SERVERS_GUIDE.md`](docs/CLAUDE_MULTIPLE_SERVERS_GUIDE.md) | Multi-server setup guide |
| 🏗️ [`docs/PROJECT_STRUCTURE.md`](docs/PROJECT_STRUCTURE.md) | Project organization |

## 🔐 Security & Permissions

### 🔑 Required API Permissions

- **Projects**: Read access
- **Jobs**: Read access
- **Executions**: Read and Execute permissions
- **Resources**: Read access (for node filters)
- **System**: Read access (for health metrics)

### 🛡️ Security Best Practices

- ✅ Store API tokens securely
- ✅ Use environment variables
- ✅ Limit token permissions
- ✅ Use HTTPS connections
- ✅ Rotate tokens regularly
- ❌ Never commit tokens to version control

## 🐛 Troubleshooting

### 🔍 Quick Diagnostics

```bash
# Test configuration
python tests/test_server.py

# Debug job execution
python tests/debug_jobs.py

# Fix Claude configuration
python tests/fix_claude_config.py
```

### ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| 🚫 "Server not found" | Check Python paths in Claude config |
| 🔌 "Connection failed" | Verify Rundeck URL and API token |
| 🔒 "Permission denied" | Check API token permissions |
| ⚙️ Environment variables | Ensure `.env` file is configured |

## 🤝 Contributing

We welcome contributions to this experimental project!

```bash
# Development setup
make dev-install

# Run tests
make test

# Format code
make format

# Type checking
make type-check
```

## 📄 License

This project is licensed under the MIT License - see the [`LICENSE`](LICENSE) file for details.

---

### 🔬 **Remember: This is an Experimental Project**

**Built for learning and exploration • Not officially supported**

**Use responsibly and at your own risk**

---

**Made with ❤️ for the DevOps community**