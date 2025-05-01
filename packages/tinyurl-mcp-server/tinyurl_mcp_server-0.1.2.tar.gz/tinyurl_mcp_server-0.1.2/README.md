# TinyURL MCP Server

A simple MCP server for generating short links using TinyURL API.

## Configuration

```json
{
    "mcpServers": {
        "tinyurl": {
            "command": "uvx",
            "args": ["tinyurl-mcp-server"],
            "env": {
                "TINYURL_API_KEY": "your_tinyurl_api_key"
            }
        }
    }
}
```