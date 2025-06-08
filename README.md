██████╗ ██╗   ██╗███╗   ██╗██████╗ ███████╗ ██████╗██╗  ██╗    ███╗   ███╗ ██████╗██████╗ 
██╔══██╗██║   ██║████╗  ██║██╔══██╗██╔════╝██╔════╝██║ ██╔╝    ████╗ ████║██╔════╝██╔══██╗
██████╔╝██║   ██║██╔██╗ ██║██║  ██║█████╗  ██║     █████╔╝     ██╔████╔██║██║     ██████╔╝
██╔══██╗██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██║     ██╔═██╗     ██║╚██╔╝██║██║     ██╔═══╝ 
██║  ██║╚██████╔╝██║ ╚████║██████╔╝███████╗╚██████╗██║  ██╗    ██║ ╚═╝ ██║╚██████╗██║     
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝    ╚═╝     ╚═╝ ╚═════╝╚═╝     
                                                                                           
███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗                                          
██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗                                         
███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝                                         
╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗                                         
███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║                                         
╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝                                         
```

<div align="center">

# 🚀 Rundeck MCP Server

**A Model Context Protocol (MCP) server for Rundeck automation**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Experimental](https://img.shields.io/badge/Status-Experimental-orange.svg)](https://github.com/your-username/rundeck-mcp-server)

---

### ⚠️ **EXPERIMENTAL PROJECT** ⚠️
**This is an experimental project built for learning and exploration purposes.**  
**Not officially supported by PagerDuty or Rundeck.**

---

</div>

## 🌟 Overview

Transform your Rundeck automation with AI-powered job management! This MCP server bridges the gap between Claude AI and your Rundeck infrastructure, enabling intelligent automation workflows, comprehensive analytics, and ROI analysis.

> 🔬 **Built as an Experiment**: This project was created to explore the possibilities of integrating AI with DevOps automation tools. While functional, it's designed for experimentation and learning.

## ✨ Features

<details>
<summary>🎯 <strong>Core Job Management</strong></summary>

- **🏗️ Project Management**: List and explore all Rundeck projects
- **⚙️ Job Discovery**: Find jobs with intelligent filtering
- **📋 Job Definitions**: Get detailed job configurations and workflows
- **🚀 Job Execution**: Run jobs with custom parameters and node filters
- **📊 Execution Monitoring**: Track job status and retrieve output logs

</details>

<details>
<summary>📈 <strong>Advanced Analytics & Monitoring</strong></summary>

- **📊 Execution Analytics**: Comprehensive success rates and performance metrics
- **🔍 Smart Filtering**: Advanced execution queries with pagination
- **🏥 System Health**: Monitor Rundeck system status and resources
- **📋 Project Statistics**: Detailed project insights and job counts
- **⏱️ Real-time Monitoring**: Live job execution tracking

</details>

<details>
<summary>💰 <strong>ROI & Cost Analysis</strong></summary>

- **💵 Cost Calculation**: Analyze automation costs vs manual work
- **📈 ROI Metrics**: Calculate return on automation investment
- **🎯 Value Assessment**: Quantify time and resource savings
- **📊 Business Intelligence**: Transform data into actionable insights

</details>

<details>
<summary>🔧 <strong>Enhanced Capabilities</strong></summary>

- **🔄 Multi-Server Support**: Manage multiple Rundeck environments
- **⚡ Bulk Operations**: Efficient batch status checking
- **🎛️ Customizable Prompts**: Externalized tool descriptions
- **🔐 Secure Configuration**: Environment-based credential management

</details>

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

## 🛠️ Quick Start

### 📋 Prerequisites

- 🐍 Python 3.8 or higher
- 🏗️ Rundeck server with API access
- 🔑 Valid Rundeck API token
- 🖥️ Linux environment (recommended)

### ⚡ Installation

Choose your preferred installation method:

<details>
<summary>🚀 <strong>Quick Setup (Recommended)</strong></summary>

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

</details>

<details>
<summary>🔧 <strong>Manual Installation</strong></summary>

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

</details>

<details>
<summary>📦 <strong>Package Installation</strong></summary>

```bash
# Development installation
git clone https://github.com/your-username/rundeck-mcp-server.git
cd rundeck-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

</details>

<details>
<summary>🛠️ <strong>Using Make</strong></summary>

```bash
# Quick development setup
make dev-setup

# Or individual commands
make install          # Basic installation
make dev-install      # Development installation
make test            # Run tests
make configure-claude # Setup Claude Desktop
```

</details>

### 🔧 Configuration

<details>
<summary>🏢 <strong>Single Server Setup</strong></summary>

```bash
# Edit your .env file
RUNDECK_URL=https://your-rundeck-server.com
RUNDECK_API_TOKEN=your-api-token-here
RUNDECK_API_VERSION=47
RUNDECK_NAME=production
```

</details>

<details>
<summary>🌐 <strong>Multi-Server Setup</strong></summary>

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

</details>

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

<details>
<summary>🏗️ <strong>Project & Job Management</strong></summary>

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

</details>

<details>
<summary>🚀 <strong>Job Execution</strong></summary>

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

</details>

<details>
<summary>📊 <strong>Analytics & Reporting</strong></summary>

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

</details>

## 📚 Documentation

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

```
✅ Store API tokens securely
✅ Use environment variables
✅ Limit token permissions
✅ Use HTTPS connections
✅ Rotate tokens regularly
❌ Never commit tokens to version control
```

## 🐛 Troubleshooting

<details>
<summary>🔍 <strong>Quick Diagnostics</strong></summary>

```bash
# Test configuration
python tests/test_server.py

# Debug job execution
python tests/debug_jobs.py

# Fix Claude configuration
python tests/fix_claude_config.py
```

</details>

<details>
<summary>⚠️ <strong>Common Issues</strong></summary>

| Issue | Solution |
|-------|----------|
| 🚫 "Server not found" | Check Python paths in Claude config |
| 🔌 "Connection failed" | Verify Rundeck URL and API token |
| 🔒 "Permission denied" | Check API token permissions |
| ⚙️ Environment variables | Ensure `.env` file is configured |

</details>

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

<div align="center">

### 🔬 **Remember: This is an Experimental Project**

**Built for learning and exploration • Not officially supported**

**Use responsibly and at your own risk**

---

**Made with ❤️ for the DevOps community**

</div>