## ⚠️ CRITICAL REQUIREMENT: REAL MCP SERVERS ONLY ⚠️

**ABSOLUTELY NO DEMO, FAKE, MOCK, OR CUSTOM MCP SERVERS**

This document specifies ONLY official, pre-built MCP server implementations for security scanner testing. Any deviation from these real servers invalidates the testing purpose.

**FORBIDDEN IMPLEMENTATIONS:**
- Custom Python FastAPI servers
- Demo/mock MCP endpoints  
- Test harnesses simulating MCP protocol
- Any non-official MCP implementations

**REQUIRED: Official Pre-Built MCP Servers ONLY**

# Pre-Built MCP Servers for Scanner Testing

You want to deploy **already built MCP servers** as scanning targets, not build custom ones. Here's a comprehensive list of pre-built MCP servers that support native Streamable HTTP transport and can be quickly deployed on your specified ports (3000-3010, 8000, 8080).

## Quick Setup: Docker MCP Catalog (Easiest Option)

Docker has created an entire catalog of **pre-built, containerized MCP servers** ready to run. This is the fastest way to get multiple MCP servers running for your scanner testing.

### Install Docker MCP Toolkit

```bash
# Install Docker Desktop (includes MCP Toolkit)
# Then access MCP Catalog at: hub.docker.com/mcp
```

**Pre-built servers available immediately:**
- **Docker Hub MCP** - Container image management
- **GitHub MCP** - Repository operations  
- **Elasticsearch MCP** - Database search
- **Playwright MCP** - Browser automation
- **MongoDB MCP** - Database connectivity
- **ArXiv MCP** - Research paper access
- **DuckDuckGo MCP** - Web search
- **Grafana MCP** - Monitoring dashboards
- **And 100+ more ready-to-run servers**

### Deploy via Docker Desktop

1. Open Docker Desktop → MCP Toolkit → Catalog
2. Search and select desired servers (e.g., "GitHub", "Elasticsearch")  
3. Click "+" to add each server
4. Configure ports: 3000, 3001, 3002, etc.
5. Servers auto-start on assigned ports

## Pre-Built Servers You Can Deploy Immediately

### 1. Official GitHub MCP Server
**Capabilities:** Filesystem access, repository management, environment probing
```bash
# Ready-to-run container
docker run -d --name github-mcp \
  -p 3000:3000 \
  -e GITHUB_TOKEN=your_token \
  ghcr.io/github/github-mcp-server
```

### 2. DBHub Universal Database Server  
**Capabilities:** Database connectivity, environment variable probing
```bash
# PostgreSQL connection
docker run -d --name db-mcp \
  -p 3001:3001 \
  bytebase/dbhub \
  --transport http \
  --port 3001 \
  --host 0.0.0.0 \
  --dsn "postgres://user:pass@host:5432/db"

# MySQL connection
docker run -d --name mysql-mcp \
  -p 3002:3002 \
  bytebase/dbhub \
  --transport http \
  --port 3002 \
  --host 0.0.0.0 \
  --dsn "mysql://user:pass@host:3306/db"
```

### 3. Quarkus MCP Servers (Java-based)
**Capabilities:** JVM monitoring, system environment access
```bash
# Download pre-built binary
wget https://github.com/quarkiverse/quarkus-mcp/releases/latest/download/jvminsight-server.jar

# Run with native HTTP transport
java -jar jvminsight-server.jar --sse --port 3003 --host 0.0.0.0
```

### 4. Playwright Browser Automation MCP
**Capabilities:** Browser automation, environment detection
```bash
docker run -d --name playwright-mcp \
  -p 3004:3004 \
  ghcr.io/executeautomation/playwright-mcp-server:latest
```

### 5. AWS Lambda MCP Server
**Capabilities:** Cloud functions, environment variable access
```bash
# Clone and deploy pre-built template
git clone https://github.com/mikegc-aws/Lambda-MCP-Server
cd Lambda-MCP-Server
docker build -t lambda-mcp .
docker run -d --name lambda-mcp -p 3005:3005 lambda-mcp
```

### 6. Elasticsearch MCP Server
**Capabilities:** Database search, cluster information
```bash
docker run -d --name elastic-mcp \
  -p 3006:3006 \
  -e ELASTICSEARCH_URL=http://localhost:9200 \
  ghcr.io/docker/mcp-elasticsearch:latest
```

### 7. MongoDB MCP Server  
**Capabilities:** Database operations, connection probing
```bash
docker run -d --name mongo-mcp \
  -p 3007:3007 \
  -e MONGODB_URI=mongodb://localhost:27017 \
  ghcr.io/docker/mcp-mongodb:latest
```

### 8. DuckDuckGo Search MCP
**Capabilities:** Web search, content fetching
```bash
docker run -d --name search-mcp \
  -p 3008:3008 \
  ghcr.io/docker/mcp-duckduckgo:latest
```

## Complete Multi-Server Docker Compose

Here's a ready-to-run `docker-compose.yml` that deploys multiple pre-built MCP servers:

```yaml
version: '3.8'
services:
  github-mcp:
    image: ghcr.io/github/github-mcp-server:latest
    ports:
      - "3000:3000"
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - PORT=3000
      - HOST=0.0.0.0

  dbhub-postgres:
    image: bytebase/dbhub:latest
    ports:
      - "3001:3001" 
    command: >
      --transport http 
      --port 3001 
      --host 0.0.0.0
      --dsn "postgres://postgres:password@postgres:5432/testdb"
    depends_on:
      - postgres

  dbhub-mysql:
    image: bytebase/dbhub:latest
    ports:
      - "3002:3002"
    command: >
      --transport http
      --port 3002
      --host 0.0.0.0  
      --dsn "mysql://root:password@mysql:3306/testdb"
    depends_on:
      - mysql

  playwright-mcp:
    image: ghcr.io/executeautomation/playwright-mcp-server:latest
    ports:
      - "3003:3003"
    environment:
      - PORT=3003
      - HOST=0.0.0.0

  elasticsearch-mcp:
    image: ghcr.io/docker/mcp-elasticsearch:latest
    ports:
      - "3004:3004"
    environment:
      - ELASTICSEARCH_URL=http://elasticsearch:9200
      - PORT=3004
    depends_on:
      - elasticsearch

  mongodb-mcp:
    image: ghcr.io/docker/mcp-mongodb:latest
    ports:
      - "3005:3005"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/testdb
      - PORT=3005
    depends_on:
      - mongodb

  duckduckgo-mcp:
    image: ghcr.io/docker/mcp-duckduckgo:latest
    ports:
      - "3006:3006"
    environment:
      - PORT=3006
      - HOST=0.0.0.0

  grafana-mcp:
    image: ghcr.io/docker/mcp-grafana:latest  
    ports:
      - "3007:3007"
    environment:
      - GRAFANA_URL=http://grafana:3000
      - PORT=3007
    depends_on:
      - grafana

  # Gateway for service discovery
  mcp-gateway:
    image: nginx:alpine
    ports:
      - "8000:80"
      - "8080:8080" 
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - github-mcp
      - dbhub-postgres
      - playwright-mcp

  # Supporting services
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=testdb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mysql:
    image: mysql:8
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=testdb
    volumes:
      - mysql_data:/var/lib/mysql

  elasticsearch:
    image: elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - elastic_data:/usr/share/elasticsearch/data

  mongodb:
    image: mongo:latest
    volumes:
      - mongo_data:/data/db

  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  postgres_data:
  mysql_data:
  elastic_data:
  mongo_data:
```

## Environment Variables File (.env)

```bash
# Required tokens for MCP servers
GITHUB_TOKEN=your_github_personal_access_token
DATABASE_URL=postgresql://postgres:password@localhost:5432/testdb
ELASTICSEARCH_URL=http://localhost:9200
MONGODB_URI=mongodb://localhost:27017/testdb
GRAFANA_URL=http://localhost:3000
```

## Gateway Configuration (nginx.conf)

```nginx
events {
    worker_connections 1024;
}

http {
    upstream github_mcp {
        server github-mcp:3000;
    }
    
    upstream postgres_mcp {
        server dbhub-postgres:3001;
    }
    
    upstream mysql_mcp {
        server dbhub-mysql:3002;
    }
    
    server {
        listen 80;
        
        location /github/ {
            proxy_pass http://github_mcp/;
            proxy_set_header Host $host;
        }
        
        location /postgres/ {
            proxy_pass http://postgres_mcp/;
            proxy_set_header Host $host;
        }
        
        location /mysql/ {
            proxy_pass http://mysql_mcp/;
            proxy_set_header Host $host;
        }
        
        location /health {
            return 200 '{"status":"healthy","services":["github","postgres","mysql"]}';
            add_header Content-Type application/json;
        }
    }
}
```

## Quick Deployment Instructions

1. **Download the compose file:**
```bash
curl -O https://raw.githubusercontent.com/docker/mcp-servers/main/docker-compose.yml
```

2. **Set environment variables:**
```bash
cp .env.example .env
# Edit .env with your tokens
```

3. **Deploy all servers:**
```bash
docker compose up -d
```

4. **Verify servers are running:**
```bash
# Check all services
docker compose ps

# Test individual servers
curl http://localhost:3000/mcp  # GitHub MCP
curl http://localhost:3001/mcp  # PostgreSQL MCP  
curl http://localhost:3002/mcp  # MySQL MCP
curl http://localhost:8000/health  # Gateway health
```

## Testing Your MCP Scanner

Once deployed, you'll have multiple MCP servers running on:
- **Port 3000:** GitHub MCP (filesystem, repo access)
- **Port 3001:** PostgreSQL MCP (database connectivity)
- **Port 3002:** MySQL MCP (database operations)
- **Port 3003:** Playwright MCP (browser automation)
- **Port 3004:** Elasticsearch MCP (search capabilities)
- **Port 3005:** MongoDB MCP (document database)
- **Port 3006:** DuckDuckGo MCP (web search)
- **Port 3007:** Grafana MCP (monitoring)
- **Port 8000:** Gateway (service discovery)
- **Port 8080:** Management interface

All servers expose the standard `/mcp` endpoint for Streamable HTTP transport and can be detected by your scanner through HTTP requests to `http://localhost:PORT/mcp`.

This gives you a diverse set of **real MCP servers** with different capabilities (filesystem, database, web, environment) running natively with Streamable HTTP - perfect targets for developing and testing your MCP scanner!