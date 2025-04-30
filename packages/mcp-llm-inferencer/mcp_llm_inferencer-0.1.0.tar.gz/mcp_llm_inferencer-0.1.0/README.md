# mcp-llm_inferencer

Uses Claude or OpenAI API to convert prompt-mapped input into concrete MCP server components such as tools, resource templates, and prompt handlers.

## Features

- LLM call engine with retry and fallback logic
- Supports Claude and OpenAI interchangeably
- Streaming support for Claude Desktop
- Tool and resource response validation
- Structured output bundling per component

## Installation

```bash
pip install mcp-llm_inferencer
```

## Usage

```python
from mcp_llm_inferencer import Mcp_llm_inferencer

# Initialize the library
mcp_llm_inferencer_instance = Mcp_llm_inferencer()

# Use the library functions
# Example usage will be added in future versions
```

## License

MIT
