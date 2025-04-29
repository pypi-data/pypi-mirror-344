# mcp_server_say_hello

MCP Protocol-compliant greeting service providing standardized greeting tool interfaces.

## Features

- Personalized greeting generation
- Compliant with MCP v1.2 protocol specifications
- Multi-environment deployment support (uvx/docker/pip)
- Complete tool registration specifications

## Tool Registration

### Tool List

1. `say_hello`
   - Description: Greeting tool for users
   - Input Parameters:
  
     ```json
     {
       "name": "username"
     }
     ```

   - Success Response:
  
     ```json
     {
       "type": "text",
       "text": "Hello {username}!"
     }
     ```

## API Reference

**endpoint**: POST /say_hello

request parameters:

```json
{
  "name": "username"
}
```

success response:

```json
{
  "message": "Hello {username}!"
}
```

## Integrated configuration

### VS Code configuration

```json
{
  "mcp": {
    "servers": {
      "say_hello": {
        "command": "uvx",
        "args": ["mcp_server_say_hello"]
      }
    }
  }
}
```

or locally (if you installed the package using `pip install` or `pip install -e .`):

```json
{
  "mcp": {
    "servers": {
      "say_hello": {
        "command": "/path/to/python",
        "args": ["-m", "mcp_server_say_hello"]
      }
    }
  }
}
```

### Claude Desktop or Trae CN Desktop configuration

use python

```json
{
  "mcpServers": {
    "say_hello": {
      "command": "python",
      "args": ["-m", "mcp_server_say_hello"]
    }
  }
}
```

or uvx

```json
{
  "mcpServers": {
    "say_hello": {
      "command": "uvx",
      "args": ["mcp_server_say_hello"]
    }
  }
}
```

## debug

Debug the service using the MCP protocol inspector:

```bash
npx @modelcontextprotocol/inspector uvx mcp_server_say_hello
```
