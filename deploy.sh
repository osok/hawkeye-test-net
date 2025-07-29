#!/bin/bash

# MCP Container Test Environment - Deployment Script
# This script helps deploy and manage the MCP test environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if .env file exists
check_env_file() {
    if [ ! -f ".env" ]; then
        print_warning ".env file not found!"
        print_status "Creating .env file from template..."
        
        if [ -f ".env.template" ]; then
            cp .env.template .env
            print_warning "Please edit .env file with your actual tokens and passwords before running:"
            print_warning "  - GITHUB_TOKEN: Your GitHub personal access token"
            print_warning "  - POSTGRES_PASSWORD: Secure PostgreSQL password"
            print_warning "  - MYSQL_ROOT_PASSWORD: Secure MySQL root password"
            print_warning "  - GRAFANA_ADMIN_PASSWORD: Secure Grafana admin password"
            print_warning "  - GRAFANA_TOKEN: Your Grafana service account token (optional)"
            echo ""
            read -p "Press Enter after updating .env file to continue..."
        else
            print_error ".env.template not found! Cannot create .env file."
            exit 1
        fi
    fi
}

# Function to check Docker requirements
check_docker() {
    print_status "Checking Docker installation..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if docker compose plugin is available
    if ! docker compose version &> /dev/null; then
        print_error "Docker Compose plugin is not available. Please install Docker Compose V2."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are available"
}

# Function to deploy the environment
deploy() {
    print_status "Deploying MCP Container Test Environment..."
    
    check_docker
    check_env_file
    
    print_status "Starting all containers..."
    docker compose up -d
    
    print_status "Waiting for services to start..."
    sleep 30
    
    print_success "Deployment complete!"
    print_status "Services should be available at:"
    echo "  - Everything MCP: http://localhost:3000/"
    echo "  - Filesystem MCP: http://localhost:3001/"
    echo "  - Git MCP: http://localhost:3002/"
    echo "  - PostgreSQL MCP: http://localhost:3003/"
    echo "  - Puppeteer MCP: http://localhost:3004/"
    echo "  - SQLite MCP: http://localhost:3005/"
    echo "  - Fetch MCP: http://localhost:3006/"
    echo "  - Memory MCP: http://localhost:3007/"
    echo "  - Gateway Health: http://localhost:8000/health"
    echo "  - Service Discovery: http://localhost:8000/discover"
    echo "  - Management UI: http://localhost:8080"
}

# Function to check service status
status() {
    print_status "Checking service status..."
    docker compose ps
    
    print_status "Testing MCP endpoint connectivity..."
    
    services=(
        "3000:Everything"
        "3001:Filesystem"
        "3002:Git" 
        "3003:PostgreSQL"
        "3004:Puppeteer"
        "3005:SQLite"
        "3006:Fetch"
        "3007:Memory"
    )
    
    for service in "${services[@]}"; do
        port="${service%%:*}"
        name="${service##*:}"
        
        if curl -f -s "http://localhost:$port/" > /dev/null 2>&1; then
            print_success "$name MCP (port $port): Online"
        else
            print_warning "$name MCP (port $port): Not responding"
        fi
    done
    
    # Test gateway endpoints
    if curl -f -s "http://localhost:8000/health" > /dev/null 2>&1; then
        print_success "Gateway Health Check: Online" 
    else
        print_warning "Gateway Health Check: Not responding"
    fi
}

# Function to stop the environment
stop() {
    print_status "Stopping MCP Container Test Environment..."
    docker compose down
    print_success "Environment stopped"
}

# Function to clean up the environment
cleanup() {
    print_status "Cleaning up MCP Container Test Environment..."
    docker compose down -v --remove-orphans
    print_success "Environment cleaned up (volumes removed)"
}

# Function to show logs
logs() {
    if [ $# -eq 0 ]; then
        docker compose logs -f
    else
        docker compose logs -f "$1"
    fi
}

# Function to show help
help() {
    echo "MCP Container Test Environment - Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy    Deploy the complete MCP test environment"
    echo "  status    Check status of all services and test connectivity" 
    echo "  stop      Stop all containers"
    echo "  cleanup   Stop containers and remove volumes"
    echo "  logs      Show logs for all services (or specify service name)"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy           # Deploy the environment"
    echo "  $0 status           # Check service status"
    echo "  $0 logs github-mcp  # Show logs for GitHub MCP service"
    echo "  $0 cleanup          # Clean up everything"
}

# Main script logic
case "${1:-help}" in
    deploy)
        deploy
        ;;
    status)
        status
        ;;
    stop)
        stop
        ;;
    cleanup)
        cleanup
        ;;
    logs)
        logs "${2:-}"
        ;;
    help|*)
        help
        ;;
esac 