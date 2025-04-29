"""FastMCP - A more ergonomic interface for MCP servers."""
 
from importlib.metadata import version
 
from .server import Context, FastMCP
from .utilities.types import Image
 
# __version__ = version("mcp")
__version__ = "1.4.0"  # or any dummy version string
 
__all__ = ["FastMCP", "Context", "Image"]
 