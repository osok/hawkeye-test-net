# MCP Demo Project

This is a demonstration project showcasing the capabilities of the Model Context Protocol (MCP) filesystem server.

## 🎯 Purpose

- Test MCP filesystem server operations
- Demonstrate secure handling of environment variables
- Showcase file and directory management through MCP tools

## 📁 Project Structure

```
demo-project/
├── index.html          # Hello World web application
├── .env               # Environment variables (FAKE secrets for demo)
├── config.json        # Application configuration
└── README.md          # This file
```

## 🔐 Security Note

**IMPORTANT**: All credentials in the `.env` file are FAKE and for demonstration purposes only! Never commit real secrets to version control.

## 🚀 Features Demonstrated

- **File Operations**: Read, write, edit files through MCP
- **Directory Listing**: Browse project structure
- **Search Capabilities**: Find files matching patterns
- **Secure Access**: Environment variables in separate .env file
- **Metadata Access**: File information and permissions

## 🛠️ Available MCP Tools

The filesystem server provides 14+ tools for file operations:
- `read_text_file` - Read file contents
- `write_file` - Create/overwrite files
- `edit_file` - Make line-based edits
- `list_directory` - Browse directories
- `search_files` - Find files by pattern
- `get_file_info` - File metadata
- `create_directory` - Create directories
- `move_file` - Move/rename files
- And more...

## 🧪 Testing

Use the MCP inspector to test the server:

```bash
python src/mcp_inspector.py http://192.168.100.3:3001
```

## 📝 Notes

This project is mounted into the MCP filesystem server container, allowing secure access to project files while maintaining proper sandboxing. 