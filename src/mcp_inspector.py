#!/usr/bin/env python3
"""
MCP Filesystem Server Inspector
Inspects and tests an MCP server running at a given HTTP endpoint
"""

import json
import requests
import uuid
from typing import Dict, Any, Optional
import sys

class MCPInspector:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.mcp_endpoint = f"{self.base_url}/mcp"
        self.session_id = None
        self.server_capabilities = None
        
    def _make_request(self, method: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a JSON-RPC request to the MCP server"""
        request_id = str(uuid.uuid4())
        
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method
        }
        
        if params:
            payload["params"] = params
            
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        # Include session ID if we have one
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
            
        try:
            print(f"📤 Sending {method} request to {self.mcp_endpoint}")
            response = requests.post(self.mcp_endpoint, 
                                   json=payload, 
                                   headers=headers,
                                   timeout=10)
            
            # Check for session ID in response headers
            if "Mcp-Session-Id" in response.headers:
                self.session_id = response.headers["Mcp-Session-Id"]
                print(f"🔑 Session ID received: {self.session_id}")
            
            print(f"📥 Response status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                return {"error": f"HTTP {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
            return {"error": str(e)}
    
    def test_connectivity(self) -> bool:
        """Test basic connectivity to the server"""
        print(f"\n🔍 Testing connectivity to {self.base_url}")
        
        try:
            # First try a simple GET to the base URL
            response = requests.get(self.base_url, timeout=5)
            print(f"✅ Base URL accessible (HTTP {response.status_code})")
            
            # Try GET to MCP endpoint (for SSE detection)
            response = requests.get(self.mcp_endpoint, timeout=5)
            print(f"✅ MCP endpoint accessible (HTTP {response.status_code})")
            
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Connectivity test failed: {str(e)}")
            return False
    
    def initialize_session(self) -> bool:
        """Initialize MCP session"""
        print(f"\n🚀 Initializing MCP session")
        
        params = {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {"listChanged": True},
                "sampling": {}
            },
            "clientInfo": {
                "name": "mcp-inspector",
                "version": "1.0.0"
            }
        }
        
        result = self._make_request("initialize", params)
        
        if "result" in result:
            self.server_capabilities = result["result"]
            print("✅ Session initialized successfully")
            print(f"📋 Server info: {result['result'].get('serverInfo', {})}")
            print(f"🔧 Server capabilities: {result['result'].get('capabilities', {})}")
            return True
        else:
            print(f"❌ Initialization failed: {result}")
            return False
    
    def list_tools(self) -> Optional[Dict]:
        """List available tools"""
        print(f"\n🛠️  Listing available tools")
        
        result = self._make_request("tools/list")
        
        if "result" in result:
            tools = result["result"].get("tools", [])
            print(f"✅ Found {len(tools)} tools:")
            
            for tool in tools:
                print(f"  📌 {tool['name']}: {tool.get('description', 'No description')}")
                if 'inputSchema' in tool:
                    properties = tool['inputSchema'].get('properties', {})
                    if properties:
                        print(f"     Parameters: {list(properties.keys())}")
            
            return result["result"]
        else:
            print(f"❌ Failed to list tools: {result}")
            return None
    
    def list_resources(self) -> Optional[Dict]:
        """List available resources"""
        print(f"\n📁 Listing available resources")
        
        result = self._make_request("resources/list")
        
        if "result" in result:
            resources = result["result"].get("resources", [])
            print(f"✅ Found {len(resources)} resources:")
            
            for resource in resources:
                print(f"  📄 {resource['uri']}: {resource.get('name', 'No name')}")
                if 'description' in resource:
                    print(f"     {resource['description']}")
            
            return result["result"]
        else:
            print(f"❌ Failed to list resources: {result}")
            return None
    
    def test_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict]:
        """Test calling a specific tool"""
        print(f"\n🔧 Testing tool call: {tool_name}")
        
        params = {
            "name": tool_name,
            "arguments": arguments
        }
        
        result = self._make_request("tools/call", params)
        
        if "result" in result:
            print(f"✅ Tool call successful")
            content = result["result"].get("content", [])
            for item in content:
                if item.get("type") == "text":
                    print(f"📄 Output: {item.get('text', '')[:200]}...")
            return result["result"]
        else:
            print(f"❌ Tool call failed: {result}")
            return None
    
    def run_filesystem_tests(self):
        """Run filesystem-specific tests"""
        print(f"\n🗂️  Running filesystem-specific tests")
        
        # First, check what directories are allowed
        print("\n--- Testing list_allowed_directories ---")
        self.test_tool_call("list_allowed_directories", {})
        
        # Test list_directory on /projects (our mounted demo project)
        print("\n--- Testing list_directory on /projects ---")
        self.test_tool_call("list_directory", {"path": "/projects"})
        
        # Test get_file_info on the demo project directory
        print("\n--- Testing get_file_info on /projects ---")
        self.test_tool_call("get_file_info", {"path": "/projects"})
        
        # Test reading the HTML file
        print("\n--- Testing read_text_file on index.html ---")
        self.test_tool_call("read_text_file", {"path": "/projects/index.html"})
        
        # Test reading the config file
        print("\n--- Testing read_text_file on config.json ---")
        self.test_tool_call("read_text_file", {"path": "/projects/config.json"})
        
        # Test search_files for HTML files
        print("\n--- Testing search_files for *.html ---")
        self.test_tool_call("search_files", {
            "path": "/projects",
            "pattern": "*.html",
            "max_results": 5
        })
        
        # Test search_files for environment files
        print("\n--- Testing search_files for .env ---")
        self.test_tool_call("search_files", {
            "path": "/projects", 
            "pattern": ".env",
            "max_results": 5
        })
        
        # Test directory tree view
        print("\n--- Testing directory_tree ---")
        self.test_tool_call("directory_tree", {"path": "/projects"})
    
    def comprehensive_inspect(self):
        """Run comprehensive inspection"""
        print("=" * 60)
        print("🔍 MCP FILESYSTEM SERVER INSPECTOR")
        print("=" * 60)
        
        # Test connectivity
        if not self.test_connectivity():
            print("❌ Cannot connect to server. Exiting.")
            return False
        
        # Initialize session
        if not self.initialize_session():
            print("❌ Cannot initialize MCP session. Exiting.")
            return False
        
        # List tools
        tools_result = self.list_tools()
        
        # List resources
        resources_result = self.list_resources()
        
        # Run filesystem tests if tools are available
        if tools_result and tools_result.get("tools"):
            self.run_filesystem_tests()
        
        print("\n" + "=" * 60)
        print("✅ INSPECTION COMPLETE")
        print("=" * 60)
        
        return True

def main():
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    else:
        server_url = "http://192.168.100.3:3001"
    
    print(f"🎯 Target server: {server_url}")
    
    inspector = MCPInspector(server_url)
    inspector.comprehensive_inspect()

if __name__ == "__main__":
    main()