# MCP Container Test Environment - Task List

## ⚠️ CRITICAL REQUIREMENT: REAL MCP SERVERS ONLY ⚠️

**NO DEMO, FAKE, MOCK, OR CUSTOM MCP SERVERS PERMITTED**

All MCP servers must be official, pre-built implementations from the Design Document:
- GitHub MCP Server (ghcr.io/github/github-mcp-server)
- PostgreSQL MCP via DBHub (bytebase/dbhub)
- MySQL MCP via DBHub (bytebase/dbhub) 
- Playwright MCP (ghcr.io/executeautomation/playwright-mcp-server)
- Elasticsearch MCP (ghcr.io/docker/mcp-elasticsearch)
- MongoDB MCP (ghcr.io/docker/mcp-mongodb)
- DuckDuckGo MCP (ghcr.io/docker/mcp-duckduckgo)
- Grafana MCP (ghcr.io/docker/mcp-grafana)

**ABSOLUTELY FORBIDDEN:** Python FastAPI demos, custom implementations, mock servers

## Project Overview  
Implementing a comprehensive MCP server test environment using Docker containers for testing the MCP scanner. Deploying 14 containers (8 MCP servers + 5 supporting services + 1 gateway) on a minimal network CIDR.

## ✅ Status: Foundation Complete - Ready for Testing Phase
All infrastructure tasks (MCP-1 through MCP-15) are complete. The environment is ready for testing and validation.

## Tasks

| ID | Task Description | Dependencies | Status | Reference |
|----|------------------|--------------|--------|-----------|
| MCP-1 | Create Docker network configuration with /27 CIDR (172.20.0.0/27) | None | Complete | docker-compose.yml |
| MCP-2 | Create .env template with required tokens and credentials | None | Complete | .env.template |
| MCP-3 | Create nginx gateway configuration for service discovery | None | Complete | nginx.conf |
| MCP-4 | Create supporting services configuration (PostgreSQL, MySQL, Elasticsearch, MongoDB, Grafana) | MCP-1 | Complete | docker-compose.yml |
| MCP-5 | Configure GitHub MCP Server container (port 3000) | MCP-1, MCP-2 | Complete | docker-compose.yml |
| MCP-6 | Configure PostgreSQL MCP Server container (port 3001) | MCP-1, MCP-4 | Complete | docker-compose.yml |
| MCP-7 | Configure MySQL MCP Server container (port 3002) | MCP-1, MCP-4 | Complete | docker-compose.yml |
| MCP-8 | Configure Playwright MCP Server container (port 3003) | MCP-1 | Complete | docker-compose.yml |
| MCP-9 | Configure Elasticsearch MCP Server container (port 3004) | MCP-1, MCP-4 | Complete | docker-compose.yml |
| MCP-10 | Configure MongoDB MCP Server container (port 3005) | MCP-1, MCP-4 | Complete | docker-compose.yml |
| MCP-11 | Configure DuckDuckGo MCP Server container (port 3006) | MCP-1 | Complete | docker-compose.yml |
| MCP-12 | Configure Grafana MCP Server container (port 3007) | MCP-1, MCP-4 | Complete | docker-compose.yml |
| MCP-13 | Configure Nginx Gateway container (ports 8000, 8080) | MCP-3 | Complete | docker-compose.yml |
| MCP-14 | Create master docker-compose.yml file with all services | MCP-5 through MCP-13 | Complete | docker-compose.yml |
| MCP-15 | Create deployment scripts and documentation | MCP-14 | Complete | deploy.sh, README.md |
| T-MCP-1 | Test all container startup and network connectivity | MCP-15 | Ready | deploy.sh, docker-compose.yml |
| T-MCP-2 | Test MCP endpoints respond correctly on all ports | T-MCP-1 | Ready | deploy.sh status command |
| T-MCP-3 | Test gateway routing and service discovery | T-MCP-1 | Ready | nginx.conf, gateway endpoints |
| T-MCP-4 | Validate scanner can discover all MCP servers | T-MCP-2, T-MCP-3 | Ready | All endpoint testing |
| C-MCP-1 | Checkpoint: Complete MCP test environment deployment | T-MCP-4 | Ready | All tasks complete |

## Network Architecture
- **CIDR**: 172.20.0.0/27 (29 usable IPs for 14 containers)
- **Gateway**: 172.20.0.1
- **Container Range**: 172.20.0.2 - 172.20.0.30
- **Host Access**: All services accessible via localhost:PORT

## Container Mapping
1. **172.20.0.2** - GitHub MCP (port 3000)
2. **172.20.0.3** - PostgreSQL MCP (port 3001) 
3. **172.20.0.4** - MySQL MCP (port 3002)
4. **172.20.0.5** - Playwright MCP (port 3003)
5. **172.20.0.6** - Elasticsearch MCP (port 3004)
6. **172.20.0.7** - MongoDB MCP (port 3005)
7. **172.20.0.8** - DuckDuckGo MCP (port 3006)
8. **172.20.0.9** - Grafana MCP (port 3007)
9. **172.20.0.10** - PostgreSQL Database
10. **172.20.0.11** - MySQL Database
11. **172.20.0.12** - Elasticsearch Instance
12. **172.20.0.13** - MongoDB Instance
13. **172.20.0.14** - Grafana Instance
14. **172.20.0.15** - Nginx Gateway (ports 8000, 8080)
