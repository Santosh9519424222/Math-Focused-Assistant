# Model Context Protocol (MCP) Server - Math Agent

## Overview

This MCP server exposes the Math Agent's knowledge base through the Model Context Protocol, allowing AI assistants like Claude to search and retrieve math problems and solutions.

## What is MCP?

Model Context Protocol (MCP) is an open standard that enables AI applications to connect to external data sources and tools. Think of it as a USB-C port for AI - a standardized way to plug AI agents into various systems.

## Features

Our MCP server provides 3 tools:

### 1. `search_math_problems`
Search for similar math problems using semantic search.

**Parameters:**
- `query` (string, required): The math question to search for
- `top_k` (int, optional): Number of results (1-10, default: 3)
- `score_threshold` (float, optional): Minimum similarity (0.0-1.0, default: 0.5)
- `topic` (string, optional): Filter by topic (e.g., "Calculus", "Algebra")

**Example:**
```
Search for problems about integration by parts
```

### 2. `get_problem_details`
Get complete details including step-by-step solution for a specific problem.

**Parameters:**
- `problem_id` (string, required): Problem identifier (e.g., "calc_001")

**Example:**
```
Get details for calc_001
```

### 3. `list_topics`
List all available topics with problem counts.

**Parameters:** None

**Example:**
```
Show all available topics
```

## Installation

The MCP server is already set up in this project. Dependencies are installed via:

```bash
pip install "mcp[cli]"
```

## Running the Server

### Standalone Testing
```bash
cd backend
python mcp_server.py
```

### With Claude Desktop

1. **Locate your Claude Desktop config file:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **Add this configuration:**
```json
{
  "mcpServers": {
    "math-agent": {
      "command": "python",
      "args": [
        "C:/Users/Lenovo/OneDrive/Desktop/new chatbot/backend/mcp_server.py"
      ]
    }
  }
}
```

3. **Restart Claude Desktop**

4. **Look for the 🔧 tools icon** in Claude Desktop to see available MCP tools

## Testing with Claude Desktop

Try these prompts in Claude:

1. **Search for problems:**
   ```
   Use the search_math_problems tool to find problems about derivatives
   ```

2. **Get problem details:**
   ```
   Get details for problem calc_001
   ```

3. **List topics:**
   ```
   Show me all available math topics
   ```

## Architecture

```
┌─────────────────────────────────────────┐
│         Claude Desktop / AI Client      │
│                                         │
└─────────────────┬───────────────────────┘
                  │
                  │ MCP Protocol (JSON-RPC)
                  │
┌─────────────────▼───────────────────────┐
│          MCP Server (FastMCP)           │
│  ┌─────────────────────────────────┐   │
│  │  Tools:                          │   │
│  │  - search_math_problems()        │   │
│  │  - get_problem_details()         │   │
│  │  - list_topics()                 │   │
│  └─────────────────────────────────┘   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Math Knowledge Base (Qdrant)       │
│                                         │
│  - Vector embeddings (384-dim)         │
│  - Semantic search                      │
│  - 5 math problems (expandable)        │
└─────────────────────────────────────────┘
```

## Knowledge Base

Currently contains 5 JEE-level math problems:

| Problem ID | Topic       | Question Type             | Difficulty    |
|-----------|-------------|---------------------------|---------------|
| calc_001  | Calculus    | Integration by parts      | JEE_Advanced  |
| alg_001   | Algebra     | Cubic equations           | JEE_Main      |
| calc_004  | Calculus    | Logarithmic differentiation| JEE_Advanced |
| prob_001  | Probability | Combinations              | JEE_Main      |
| trig_001  | Calculus    | Maclaurin series          | JEE_Advanced  |

## Technical Details

- **Framework:** FastMCP (Python MCP SDK)
- **Transport:** STDIO (standard input/output)
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB:** Qdrant (in-memory)
- **Search:** Semantic similarity (COSINE distance)

## Logging

The MCP server logs to **stderr** (not stdout) to avoid corrupting the JSON-RPC protocol:

```python
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr  # IMPORTANT for MCP
)
```

## Error Handling

All tools return formatted error messages if:
- Knowledge base is not initialized
- Invalid parameters provided
- Search fails
- Problem not found

## Extending the Server

To add more tools, use the `@mcp.tool()` decorator:

```python
@mcp.tool()
async def your_new_tool(param: str) -> str:
    """
    Tool description here.
    
    Args:
        param: Parameter description
    
    Returns:
        Result description
    """
    # Implementation
    return result
```

## Troubleshooting

### Server not showing in Claude Desktop
- Check config file path is correct
- Ensure absolute paths are used
- Restart Claude Desktop after config changes
- Check logs in stderr

### Tool calls failing
- Verify knowledge base initialized (check logs)
- Check parameter types match expected format
- Look for error messages in stderr logs

### Connection issues
- Make sure Python is in PATH
- Try running server standalone first
- Check firewall settings

## Benefits of MCP Integration

1. **Standardized Interface:** Any MCP-compatible client can use our knowledge base
2. **Tool Discovery:** Clients automatically discover available tools
3. **Type Safety:** Parameter validation via Python type hints
4. **Scalability:** Easy to add new tools without changing client code
5. **Security:** Runs in isolated process with controlled access

## Future Enhancements

- [ ] Add resource endpoints for direct problem access
- [ ] Implement prompt templates for common queries
- [ ] Add filtering by difficulty level
- [ ] Support batch problem retrieval
- [ ] Add problem submission tool
- [ ] Implement caching for faster responses

## References

- [MCP Documentation](https://modelcontextprotocol.io)
- [FastMCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://modelcontextprotocol.io/specification)
