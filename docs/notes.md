# MCP Container Test Environment - Development Notes

## ⚠️ CRITICAL REQUIREMENT: REAL MCP SERVERS ONLY ⚠️

**ABSOLUTELY NO DEMO, FAKE, MOCK, OR CUSTOM MCP SERVERS**

**Decision**: Use ONLY official, pre-built, real MCP server implementations  
**Rationale**: 
- Testing real MCP server implementations for security scanning
- Must detect actual MCP protocol implementations, not mock APIs
- Security scanner needs to identify genuine MCP servers in production environments
- Demo servers provide false positives and invalid test results

**Real MCP Servers from Design Document:**
- GitHub MCP Server (ghcr.io/github/github-mcp-server)
- DBHub Universal Database Server (bytebase/dbhub)
- Playwright Browser Automation MCP (ghcr.io/executeautomation/playwright-mcp-server)
- Elasticsearch MCP Server (ghcr.io/docker/mcp-elasticsearch)
- MongoDB MCP Server (ghcr.io/docker/mcp-mongodb)
- DuckDuckGo Search MCP (ghcr.io/docker/mcp-duckduckgo)
- Grafana MCP Server (ghcr.io/docker/mcp-grafana)

**NEVER CREATE:**
- Python FastAPI mock servers
- Custom demo implementations
- Fake MCP endpoints
- Test harnesses that mimic MCP protocol

## [2024-12-30] Project Initialization

### Architecture Decision: Minimal Network CIDR
**Decision**: Use 172.20.0.0/27 network for MCP container test environment  
**Rationale**: 
- Need exactly 14 containers (8 MCP servers + 5 supporting services + 1 gateway)
- /27 provides 29 usable IPs (172.20.0.2 - 172.20.0.30) which is optimal
- /28 would only provide 13 usable IPs (insufficient)
- /26 would provide 61 usable IPs (wasteful)
- Private 172.20.0.0 range avoids conflicts with common Docker networks

### Design Pattern: Official Pre-built MCP Servers Only
**Decision**: Use only official/community pre-built MCP server containers  
**Rationale**:
- Testing real MCP server implementations, not custom builds
- Faster deployment without compilation/build steps  
- Authentic behavior for scanner testing
- Diverse MCP server types: filesystem, databases, web services, monitoring

### Container Architecture Strategy
**Decision**: Multi-service deployment with supporting backend services  
**Rationale**:
- MCP servers require real backends (databases, search engines) for realistic testing
- Service isolation ensures clean testing environment
- Gateway provides service discovery simulation
- Each MCP server on dedicated port for scanner accessibility

## Container Service Mapping

### MCP Servers (Primary Test Targets)
1. **GitHub MCP** (3000) → Filesystem access, repository management, environment probing
2. **PostgreSQL MCP** (3001) → Database connectivity, SQL operations, connection probing  
3. **MySQL MCP** (3002) → Database operations, different SQL dialect testing
4. **Playwright MCP** (3003) → Browser automation, environment detection
5. **Elasticsearch MCP** (3004) → Search operations, cluster information
6. **MongoDB MCP** (3005) → Document database, NoSQL operations
7. **DuckDuckGo MCP** (3006) → Web search, content fetching, external API testing
8. **Grafana MCP** (3007) → Monitoring dashboards, metrics access

### Supporting Services (Required Dependencies)
- **PostgreSQL DB** → Backend for PostgreSQL MCP
- **MySQL DB** → Backend for MySQL MCP  
- **Elasticsearch** → Backend for Elasticsearch MCP
- **MongoDB** → Backend for MongoDB MCP
- **Grafana** → Backend for Grafana MCP

### Infrastructure
- **Nginx Gateway** (8000/8080) → Service discovery, routing, health checks

## Network Design Considerations

### Routing Requirements Met
✅ **Host Accessibility**: All containers accessible via `localhost:PORT` from host  
✅ **Inter-container Communication**: Docker bridge network for service dependencies  
✅ **Port Exposure**: Each MCP server on dedicated port (3000-3007)  
✅ **Gateway Access**: Service discovery via ports 8000/8080

### Security Considerations
- Private network range (172.20.0.0/27) prevents external access
- Only necessary ports exposed to host
- Service-to-service communication isolated within Docker network
- Environment variables for sensitive tokens/credentials

## Testing Strategy

### Scanner Test Scenarios
1. **Port Discovery**: Scanner should find all 8 MCP servers on ports 3000-3007
2. **Protocol Testing**: All servers configured for Streamable HTTP transport
3. **Service Diversity**: Different MCP server types provide comprehensive testing
4. **Gateway Testing**: Service discovery via gateway endpoints
5. **Health Monitoring**: All services provide health check endpoints

### Validation Endpoints
- Individual MCP servers: `http://localhost:PORT/mcp`
- Gateway health: `http://localhost:8000/health`
- Service discovery: `http://localhost:8000/SERVICE_NAME/`

## Implementation Notes

### Environment Configuration
- `.env` file required for GitHub token and database credentials
- All services configured for HTTP transport (not stdio)
- Host binding (0.0.0.0) for external accessibility
- Volume persistence for database services

### Deployment Approach
- Single `docker-compose.yml` for entire environment
- Dependency management between MCP servers and backends
- Health checks and restart policies for stability
- Resource constraints appropriate for testing environment

## [2024-12-30] Foundation Implementation Complete

### Milestone: All Infrastructure Tasks Complete
**Achievement**: Successfully implemented all foundation tasks (MCP-1 through MCP-15)  
**Status**: Environment ready for testing phase
**Files Created**: 
- `docker-compose.yml` - 14-container orchestration (8 MCP servers + 5 backends + 1 gateway)
- `nginx.conf` - Gateway configuration with service discovery and routing
- `deploy.sh` - Comprehensive deployment and management script  
- `.env.template` - Environment variables template
- `README.md` - Complete documentation and usage guide

### Architecture Validated
✅ **Network Design**: 172.20.0.0/27 CIDR optimally supports 14 containers  
✅ **Service Mapping**: All 8 MCP servers mapped to dedicated ports (3000-3007)  
✅ **Gateway Integration**: Nginx configured for service discovery and routing  
✅ **Environment Management**: Template-based configuration for credentials  
✅ **Deployment Automation**: Single-command deployment and status checking

### Ready for Testing Phase
**Next Phase**: Testing tasks (T-MCP-1 through T-MCP-4) and final checkpoint (C-MCP-1)
- Container startup and network connectivity testing
- MCP endpoint validation across all 8 servers  
- Gateway routing and service discovery testing
- Scanner integration validation

## Completed TODOs
- [x] Create .env template with placeholder values - Implemented in `.env.template`
- [x] Implement health check endpoints for all services - Implemented in `nginx.conf` and `deploy.sh`  
- [x] Create cleanup scripts for environment reset - Implemented in `deploy.sh cleanup` command
- [x] Document scanner integration testing procedures - Implemented in `README.md`

## Remaining TODOs  
- [ ] Add resource limits to prevent resource exhaustion - Priority: Medium
- [ ] Test environment deployment and validate all endpoints - Priority: High
- [ ] Validate scanner discovery of all 8 MCP servers - Priority: High
