from fastmcp import FastMCP
from open_data_mcp.core.config import settings

mcp = FastMCP(
    name=settings.name,
    version=settings.version,
    instructions=settings.description,
)
