# OpenAPI LLM Tools

Generate function tools from OpenAPI server that can be used with LLM AI agents.

## Project Checklist

- ✅ Generate python functions from OpenAPI server endpoints
- Generate function tools for OpenAPI Agent SDK
- Generate function tools for Google ADK
- Integrate pydantic for better typings
- Support for endpoints with multiple path parameters

## Installation

```bash
pip install openapi-llm-tools
```

## Usage

```python
from agent_tools import generate_tools

spec = load_spec('https://api.example.com/openapi.json')

generate_tools(spec)
```

## License

MIT
