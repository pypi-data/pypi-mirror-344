"""
Natural Language Model Database (NLMDB) package.

This package provides a way to query databases using natural language
through the Model Context Protocol (MCP) approach.
"""

from .config import Config
from .database.handler import DatabaseHandler
from .database.tools import DatabaseTools
from .mcp.handler import MCPHandler
from .agents.agent_factory import create_database_agent

# Import the simplified API
from ._api import dbagent
from ._private_api import dbagent_private

__version__ = "0.1.0"
__all__ = [
    "Config",
    "DatabaseHandler",
    "DatabaseTools",
    "MCPHandler", 
    "create_database_agent",
    "dbagent",
    "dbagent_private"
]