# MCP Container Test Environment

A comprehensive Docker-based test environment for MCP (Model Context Protocol) servers. This environment deploys 14 containers across 8 different MCP server types with supporting services for comprehensive scanner testing.

## Architecture Overview

### Network Configuration
- **CIDR**: 172.20.0.0/27 (29 usable IPs)
- **Gateway**: 172.20.0.1  
- **Container Range**: 172.20.0.2 - 172.20.0.15

### MCP Servers (Primary Test Targets)
| Service | Port | IP Address | Capabilities |
|---------|------|------------|--------------|
| GitHub MCP | 3000 | 172.20.0.2 | Filesystem access, repository management |
| PostgreSQL MCP | 3001 | 172.20.0.3 | Database connectivity, SQL operations |
| MySQL MCP | 3002 | 172.20.0.4 | Database operations, MySQL dialect |
| Playwright MCP | 3003 | 172.20.0.5 | Browser automation, environment detection |
| Elasticsearch MCP | 3004 | 172.20.0.6 | Search operations, cluster information |  
| MongoDB MCP | 3005 | 172.20.0.7 | Document database, NoSQL operations |
| DuckDuckGo MCP | 3006 | 172.20.0.8 | Web search, content fetching |
| Grafana MCP | 3007 | 172.20.0.9 | Monitoring dashboards, metrics access |

### Supporting Services
| Service | IP Address | Purpose |
|---------|------------|---------|
| PostgreSQL DB | 172.20.0.10 | Backend for PostgreSQL MCP |
| MySQL DB | 172.20.0.11 | Backend for MySQL MCP |
| Elasticsearch | 172.20.0.12 | Backend for Elasticsearch MCP |
| MongoDB | 172.20.0.13 | Backend for MongoDB MCP |
| Grafana | 172.20.0.14 | Backend for Grafana MCP |

### Gateway & Management
| Service | Ports | IP Address | Purpose |
|---------|-------|------------|---------|
| Nginx Gateway | 8000, 8080 | 172.20.0.15 | Service discovery, routing, management |

## Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose V2 (plugin)
- 4GB+ available RAM
- 10GB+ available disk space

### 1. Setup Environment Variables

```bash
# Copy the template and edit with your credentials
cp .env.template .env
# Edit .env with your actual tokens and passwords
```

Required environment variables:
- `GITHUB_TOKEN`: Your GitHub personal access token
- `POSTGRES_PASSWORD`: Secure PostgreSQL password  
- `MYSQL_ROOT_PASSWORD`: Secure MySQL root password
- `GRAFANA_ADMIN_PASSWORD`: Secure Grafana admin password
- `GRAFANA_TOKEN`: Grafana service account token (optional)

### 2. Deploy Environment

```bash
# Using the deployment script (recommended)
chmod +x deploy.sh
./deploy.sh deploy

# Or using Docker Compose directly
docker compose up -d
```

### 3. Verify Deployment

```bash
# Check service status
./deploy.sh status

# Test individual MCP endpoints
curl http://localhost:3000/mcp  # GitHub MCP
curl http://localhost:3001/mcp  # PostgreSQL MCP
curl http://localhost:3002/mcp  # MySQL MCP
curl http://localhost:3003/mcp  # Playwright MCP
curl http://localhost:3004/mcp  # Elasticsearch MCP
curl http://localhost:3005/mcp  # MongoDB MCP
curl http://localhost:3006/mcp  # DuckDuckGo MCP
curl http://localhost:3007/mcp  # Grafana MCP

# Test gateway endpoints
curl http://localhost:8000/health     # Health check
curl http://localhost:8000/discover   # Service discovery
```

## Management & Monitoring

### Management Interface
Access the web-based management interface at: http://localhost:8080

### Gateway Endpoints
- **Health Check**: `http://localhost:8000/health`
- **Service Discovery**: `http://localhost:8000/discover`  
- **Service Routing**: `http://localhost:8000/{service}/`

### Deployment Script Commands

```bash
./deploy.sh deploy    # Deploy the complete environment
./deploy.sh status    # Check service status and connectivity
./deploy.sh stop      # Stop all containers
./deploy.sh cleanup   # Stop containers and remove volumes  
./deploy.sh logs      # Show logs for all services
./deploy.sh logs github-mcp  # Show logs for specific service
```

## Scanner Testing

### MCP Endpoint Discovery
Your scanner should be able to discover all 8 MCP servers by testing ports 3000-3007:

```bash
for port in {3000..3007}; do
  echo "Testing port $port..."
  curl -f "http://localhost:$port/mcp" && echo " - MCP server found on port $port"
done
```

### Service Discovery via Gateway
Test service discovery capabilities:

```bash
# Get list of all available MCP servers
curl http://localhost:8000/discover | jq '.'

# Access services via gateway routing
curl http://localhost:8000/github/mcp
curl http://localhost:8000/postgres/mcp
```

### Protocol Testing
All MCP servers are configured for:
- **Transport**: Streamable HTTP (SSE)
- **Host Binding**: 0.0.0.0 (external access)
- **Standard Endpoint**: `/mcp`

## Troubleshooting

### Common Issues

**Containers not starting:**
```bash
# Check logs for specific service
./deploy.sh logs github-mcp

# Check Docker resources  
docker system df
docker system prune  # Clean up if needed
```

**MCP endpoints not responding:**
```bash
# Restart specific service
docker compose restart github-mcp

# Check service health
docker compose ps
```

**Network connectivity issues:**
```bash
# Verify network configuration
docker network ls
docker network inspect mcp-docker-test-node_mcp-network
```

### Resource Requirements
- **Minimum RAM**: 4GB
- **Recommended RAM**: 8GB+  
- **Disk Space**: 10GB+ for container images and volumes
- **Network**: All containers use 172.20.0.0/27 subnet

### Port Conflicts
If you have port conflicts, update the port mappings in `docker-compose.yml`:

```yaml
services:
  github-mcp:
    ports:
      - "3010:3000"  # Changed from 3000:3000
```

## Development & Customization

### Adding New MCP Servers
1. Add service definition to `docker-compose.yml`
2. Assign static IP in 172.20.0.0/27 range
3. Update `nginx.conf` with routing rules
4. Update documentation and management interface

### Environment Customization  
- Modify `.env.template` for new environment variables
- Update `docker-compose.yml` for service configurations
- Customize `nginx.conf` for routing changes

## Security Considerations

- Private network range (172.20.0.0/27) prevents external access
- Environment variables for sensitive credentials
- Volume persistence for database data
- Restart policies for service availability
- Resource limits to prevent resource exhaustion

## License

This project is designed for testing and development purposes. Please ensure you comply with the licenses of the individual MCP servers and supporting services used. 