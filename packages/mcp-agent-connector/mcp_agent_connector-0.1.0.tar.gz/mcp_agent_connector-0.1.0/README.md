# mcp-agent_connector

Enables any MCP-compliant agentic platform (Claude, Grok, TypingMind, Cursor, etc.) to auto-discover generated MCP servers and sync capabilities from build metadata.

## Features

- Auto-publish MCP server manifest (tools/resources)
- Supports mcp-agent and Lutra agents
- Metadata broadcast over local network (optional)
- Claude agent mapping via Claude Desktop config
- Real-time sync with client environment

## Installation

```bash
pip install mcp-agent_connector
```

## Usage

```python
from mcp_agent_connector import Mcp_agent_connector

# Initialize the library
mcp_agent_connector_instance = Mcp_agent_connector()

# Use the library functions
# Example usage will be added in future versions
```

## License

MIT
