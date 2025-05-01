from .config import Config
from .database.handler import DatabaseHandler
from .database.tools import DatabaseTools
from .mcp.handler import MCPHandler
from .agents.agent_factory import create_database_agent

# Import the simplified API
from ._api import dbagent
from ._private_api import dbagent_private

# Import the SQL-only mode
from ._sql_agent import sql_agent, sql_agent_private

__version__ = "1.3.4"  # Update version number
__all__ = [
    "Config",
    "DatabaseHandler",
    "DatabaseTools",
    "MCPHandler", 
    "create_database_agent",
    "dbagent",
    "dbagent_private",
    "sql_agent",
    "sql_agent_private"
]