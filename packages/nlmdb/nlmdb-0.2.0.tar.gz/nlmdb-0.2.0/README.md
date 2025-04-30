# Model Context Protocol (MCP) Library

A Python library for connecting to and querying databases using the OpenAI API and LangChain agents. This library implements the Model Context Protocol (MCP) approach, providing AI models with structured context about database schemas for more accurate database-related responses.

## Features

- Connect to SQLite databases (extensible to other database types)
- Generate structured database context for LLMs
- Create LangChain agents for database interaction
- Execute SQL queries and get results
- Direct querying of LLMs with database context

## Installation

```bash
pip install mcp-lib
```

## Quick Start

```python
from nlmdb import Config, DatabaseHandler, DatabaseTools, MCPHandler, create_database_agent
from openai import OpenAI

# Set up configuration
config = Config(openai_api_key="your-api-key", db_path="your-database.db")

# Initialize database handler
db_handler = DatabaseHandler(config.db_path)

# Initialize database tools
db_tools = DatabaseTools(db_handler)
tools = db_tools.get_tools()

# Initialize OpenAI client
client = OpenAI(api_key=config.openai_api_key)

# Initialize MCP handler
mcp_handler = MCPHandler(client, db_handler)

# Create agent executor
agent_executor = create_database_agent(
    openai_api_key=config.openai_api_key,
    tools=tools,
    mcp_handler=mcp_handler
)

# Run a query
response = agent_executor.invoke({"input": "What tables are in the database?"})
print(response["output"])
```

## Library Structure

```
mcp_lib/
├── __init__.py
├── config.py
├── database/
│   ├── __init__.py
│   ├── handler.py
│   └── tools.py
├── mcp/
│   ├── __init__.py
│   └── handler.py
├── agents/
│   ├── __init__.py
│   └── agent_factory.py
└── examples/
    ├── __init__.py
    └── example_queries.py
```

## Examples

The library includes several example functions demonstrating its usage:

```python
from mcp_lib.examples import run_examples

# Run all examples
run_examples(api_key="your-api-key", db_path="your-database.db")
```

## Requirements

- Python 3.8+
- openai>=1.0.0
- langchain>=0.1.0
- langchain-core>=0.1.0
- langchain-experimental>=0.0.0
- langchain-community>=0.0.0

## License

MIT

## Acknowledgements

This library is based on the Model Context Protocol (MCP) approach for providing AI models with structured context about database schemas.
