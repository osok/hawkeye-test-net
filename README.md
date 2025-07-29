# MCP Container Test Environment

A comprehensive Docker-based test environment for MCP (Model Context Protocol) servers. This environment demonstrates **both native HTTP MCP servers and stdio-to-HTTP proxy wrappers** using real MCP server implementations across 4 different server types with supporting gateway services.

## ⚠️ CRITICAL: REAL MCP SERVERS ONLY ⚠️

**This environment uses ONLY official, pre-built, real MCP server implementations - NO demo, fake, mock, or custom servers.**

## Architecture Overview

### Mixed Transport Method Demonstration
This environment showcases **both approaches** to MCP server deployment:
1. **✅ Native HTTP**: Servers with built-in streamableHttp support
2. **🔄 Proxied stdio**: Community servers wrapped with proxy tools to provide HTTP APIs

### Network Configuration
- **CIDR**: 192.168.100.0/27 (30 usable IPs)
- **Gateway**: 192.168.100.1  
- **Container Range**: 192.168.100.2 - 192.168.100.30

### MCP Servers (Mixed Transport Methods)
| Service | Port | IP Address | Transport Method | Capabilities |
|---------|------|------------|------------------|--------------|
| Everything MCP | 3000 | 192.168.100.2 | ✅ Native HTTP | Reference implementation, all MCP features |
| Filesystem MCP | 3001 | 192.168.100.3 | 🔄 Python Proxy | File operations via stdio→HTTP wrapper |
| Git MCP | 3002 | 192.168.100.4 | 🔄 Python Proxy | Version control via stdio→HTTP wrapper |
| Memory MCP | 3003 | 192.168.100.5 | 🔄 Node.js Proxy | Knowledge graph via stdio→HTTP wrapper |

### Gateway & Management
| Service | Ports | IP Address | Purpose |
|---------|-------|------------|---------|
| MCP Gateway | 8000, 8080 | 192.168.100.10 | Service discovery, routing, health checks |

## Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose V2 (plugin)
- 2GB+ available RAM
- 5GB+ available disk space

### 1. Deploy Environment

```bash
# Using Docker Compose directly
docker compose up -d

# Check service status
docker ps
```

### 2. Verify Deployment

```bash
# Test individual MCP endpoints
curl http://localhost:3000/        # Everything MCP (Native HTTP)
curl http://localhost:3001/mcp     # Filesystem MCP (Proxied)
curl http://localhost:3002/mcp     # Git MCP (Proxied)
curl http://localhost:3003/mcp     # Memory MCP (Proxied)

# Test gateway endpoints
curl http://localhost:8000/health     # Health check
curl http://localhost:8000/services   # Service discovery
curl http://localhost:8080/health     # Gateway health check
```

## MCP Server Details

### 🎯 Everything MCP (Port 3000) - ✅ Native HTTP
- **Package**: @modelcontextprotocol/server-everything
- **Transport**: ✅ Native streamableHttp (built-in HTTP support)
- **Capabilities**: Reference implementation with prompts, resources, and tools
- **Use Case**: Comprehensive testing with all MCP protocol features
- **Endpoint**: http://localhost:3000/

### 📁 Filesystem MCP (Port 3001) - 🔄 Proxied HTTP
- **Package**: @modelcontextprotocol/server-filesystem
- **Proxy**: [mcp-streamablehttp-proxy](https://pypi.org/project/mcp-streamablehttp-proxy/) (Python)
- **Transport**: 🔄 stdio → HTTP via Python proxy
- **Capabilities**: Secure file operations with configurable access controls
- **Endpoint**: http://localhost:3001/mcp

### 🗂️ Git MCP (Port 3002) - 🔄 Proxied HTTP
- **Package**: mcp-server-git
- **Proxy**: [mcp-streamablehttp-proxy](https://pypi.org/project/mcp-streamablehttp-proxy/) (Python)
- **Transport**: 🔄 stdio → HTTP via Python proxy
- **Capabilities**: Git repository operations and version control
- **Endpoint**: http://localhost:3002/mcp

### 🧠 Memory MCP (Port 3003) - 🔄 Proxied HTTP
- **Package**: @modelcontextprotocol/server-memory
- **Proxy**: [mcp-proxy](https://www.npmjs.com/package/mcp-proxy) (Node.js)
- **Transport**: 🔄 stdio → HTTP via Node.js proxy
- **Capabilities**: Knowledge graph-based persistent memory system
- **Endpoint**: http://localhost:3003/mcp

## Management & Monitoring

### Gateway Access (Proxied Routing)
- **Everything MCP**: http://localhost:8000/everything/
- **Filesystem MCP**: http://localhost:8000/filesystem/
- **Git MCP**: http://localhost:8000/git/
- **Memory MCP**: http://localhost:8000/memory/

### Management Endpoints
- **Health Check**: http://localhost:8000/health
- **Service Discovery**: http://localhost:8000/services
- **Gateway Health**: http://localhost:8080/health

## Scanner Testing

### MCP Endpoint Discovery
Your scanner should be able to discover all 4 MCP servers by testing ports 3000-3003:

```bash
# Test all MCP endpoints
for port in {3000..3003}; do
  if [ $port -eq 3000 ]; then
    echo "Testing port $port (Native HTTP)..."
    curl -f "http://localhost:$port/" && echo " - Native HTTP MCP server found on port $port"
  else
    echo "Testing port $port (Proxied HTTP)..."
    curl -f "http://localhost:$port/mcp" && echo " - Proxied HTTP MCP server found on port $port"
  fi
done
```

### Service Discovery via Gateway
Test service discovery capabilities:

```bash
# Get list of all available MCP servers
curl http://localhost:8000/services | jq '.'

# Access services via gateway routing
curl http://localhost:8000/everything/
curl http://localhost:8000/filesystem/
curl http://localhost:8000/git/
curl http://localhost:8000/memory/
```

### Mixed Transport Testing
This environment demonstrates both transport methods:
- **Port 3000**: ✅ Native HTTP MCP server (direct streamableHttp support)
- **Ports 3001-3003**: 🔄 Proxied HTTP MCP servers (stdio wrapped as HTTP APIs)

## Proxy Tool Comparison

### 🐍 mcp-streamablehttp-proxy (Python)
- **Installation**: `pip install mcp-streamablehttp-proxy`
- **Usage**: `mcp-streamablehttp-proxy --host 0.0.0.0 --port 3001 npx @modelcontextprotocol/server-filesystem /tmp`
- **Features**: Production-ready, session management, configurable timeouts
- **Endpoint**: `/mcp` for streamableHttp transport
- **Best For**: Production deployments, stable environments

### 📇 mcp-proxy (Node.js/TypeScript)
- **Installation**: `npm install -g mcp-proxy`
- **Usage**: `mcp-proxy --port 3003 --server stream --endpoint /mcp -- npx @modelcontextprotocol/server-memory`
- **Features**: Dual transport (HTTP + SSE), TypeScript support, CORS enabled
- **Endpoints**: `/mcp` (HTTP) and `/sse` (Server-Sent Events)
- **Best For**: Development, flexible transport options

## Troubleshooting

### Common Issues

**Containers not starting:**
```bash
# Check logs for specific service
docker logs [container-name]

# Check Docker resources  
docker system df
docker system prune  # Clean up if needed
```

**MCP endpoints not responding:**
```bash
# Restart specific service
docker compose restart [service-name]

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
- **Minimum RAM**: 2GB
- **Recommended RAM**: 4GB+  
- **Disk Space**: 5GB+ for container images and volumes
- **Network**: All containers use 192.168.100.0/27 subnet

### Port Conflicts
If you have port conflicts, update the port mappings in `docker-compose.yml`:

```yaml
services:
  everything-mcp:
    ports:
      - "3010:3000"  # Changed from 3000:3000
```

## Development & Customization

### Adding New MCP Servers
1. Add service definition to `docker-compose.yml`
2. Assign static IP in 192.168.100.0/27 range
3. Update `nginx.conf` with routing rules
4. Use appropriate proxy wrapper for stdio servers

### Proxy Wrapper Selection
- **For Production**: Use `mcp-streamablehttp-proxy` (Python) - proven stable
- **For Development**: Use `mcp-proxy` (Node.js) - more features and flexibility

## Key Learnings & Breakthrough

### 🔄 Universal Solution
**Any stdio MCP server** from the community can now be deployed as an HTTP API using these proxy wrappers!

### Mixed Transport Demonstration
This environment proves that both approaches work:
1. **Native HTTP**: For servers with built-in streamableHttp support
2. **Proxied stdio**: For the majority of community servers that only support stdio

### Community Integration
All servers are sourced from the [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) list, demonstrating real-world compatibility.

## Security Considerations

- Private network range (192.168.100.0/27) prevents external access
- Only necessary ports exposed to host
- Service-to-service communication isolated within Docker network
- Real MCP server implementations (no mock/demo servers)
- Proxy wrappers provide secure stdio-to-HTTP bridging

## License

This project is designed for testing and development purposes. Please ensure you comply with the licenses of the individual MCP servers and proxy tools used.

---

**Environment Status**: ✅ **OPERATIONAL**  
**Real MCP Servers**: 4 different server types with mixed transport methods  
**Demo Servers**: 0 (NONE - All servers are real implementations)  
**Total Containers**: 5 (4 MCP servers + 1 gateway)  
**Breakthrough Achievement**: Solves the "stdio vs HTTP" limitation for MCP server deployment 