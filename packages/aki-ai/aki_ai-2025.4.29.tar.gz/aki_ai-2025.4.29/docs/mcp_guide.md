# Project migrated to AMZN_AKI
# Check docs under https://code.amazon.com/packages/AMZN_AKI/blobs/mainline/--/docs/ for the latest version

# Model Context Protocol (MCP) Guide

This guide explains how MCP works in Aki and how to develop your own MCP servers.

## Overview

Model Context Protocol (MCP) is a standardized protocol that enables Aki to communicate with external tools and services via JSON-RPC. It allows you to extend Aki's capabilities by adding new servers that provide specialized functionality.

## Key Components

### 1. Server Configuration
MCP servers are configured in `~/.aki/mcp_settings.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npm",
      "args": ["--prefix", "${aki_home}/mcp_servers/my-server", "start"],
      "disabled": false,
      "env": {},
      "check_install_script": {
        "command": "npm",
        "args": ["list", "--prefix", "${aki_home}/mcp_servers/my-server"],
        "expected_output": "my-mcp-server@1.0.0"
      },
      "install_scripts": [
        {
          "command": "npm",
          "args": ["install"],
          "cwd": "${aki_home}/mcp_servers/my-server"
        }
      ]
    }
  }
}
```

Configuration fields:
- `command`: Command to start the server
- `args`: Command line arguments
- `disabled`: Whether the server is disabled
- `env`: Environment variables
- `check_install_script`: Script to verify installation
- `install_scripts`: Scripts to install the server

### 2. Server Installation
Aki automatically manages MCP server installation:

1. **Installation Check**:
   - Runs `check_install_script` to verify installation
   - Checks for expected output

2. **Installation Process**:
   - If not installed, runs `install_scripts` in sequence
   - Handles environment setup
   - Verifies successful installation

3. **Health Check**:
   - Tests server connection
   - Verifies tool availability
   - Updates server state

## Developing MCP Servers

### 1. Project Structure
```
my-mcp-server/
├── src/
│   └── index.ts    # Server implementation
├── package.json    # Dependencies
└── tsconfig.json   # TypeScript config
```

### 2. Server Implementation

Basic TypeScript implementation:
```typescript
import { Server, ListToolsRequestSchema, CallToolRequestSchema } from '@modelcontextprotocol/sdk';

// Create server
const server = new Server('my-server', '1.0.0');

// Register tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'my_tool',
        description: 'What my tool does',
        inputSchema: {
          type: 'object',
          properties: {
            param1: { type: 'string' }
          }
        }
      }
    ]
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { tool, arguments: args } = request;
  
  // Tool implementation
  const result = await myToolLogic(args);
  
  return {
    content: [
      {
        type: 'text',
        text: result
      }
    ]
  };
});

// Start server
server.listen();
```

### 3. Tool Response Format
```typescript
{
  content: [
    {
      type: 'text',
      text: 'Result text'
    },
    {
      type: 'error',
      text: 'Error message'
    }
  ]
}
```

## Using MCP Tools in Profiles

### 1. Enable MCP Servers
In your profile JSON:
```json
{
  "name": "My Agent",
  "description": "Uses MCP tools",
  "enabled_mcp_servers": ["my-server"],  // or "__ALL__"
  "tools": ["my_tool"]
}
```

### 2. Access MCP Tools
In system prompts:
```text
<capabilities>
Use my_tool for specialized tasks:
- Parameter: param1 (string)
- Returns: text result
</capabilities>
```

## Best Practices

### 1. Server Development
- Implement proper error handling
- Provide clear tool descriptions
- Follow JSON-RPC 2.0 spec

### 2. Tool Design
- Keep tools focused and single-purpose
- Validate all inputs
- Return structured responses
- Handle errors gracefully

### 3. Security
- Validate all inputs
- Sanitize file paths
- Implement rate limiting if needed

## Troubleshooting

### 1. Installation Issues
Check server state:
```bash
cat ~/.aki/mcp_server_state.json
```

Manual installation test:
```bash
cd ~/.aki/mcp_servers/my-server
npm install
npm start
```

### 2. Communication Issues
Test server directly:
```bash
echo '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}' | node dist/index.js
```

## Example Servers

1. **AmazonInternalMCPServer** (built-in):
   - Access internal Amazon websites
   - Search internal documentation
   - Query code repositories

2. **Memory Server** (external):
   - Knowledge graph storage
   - Entity relationship tracking
   - Persistent memory across sessions

Add below config to ~/.aki/mcp_settings.json:
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

For more MCP servers, visit: https://github.com/punkpeye/awesome-mcp-servers