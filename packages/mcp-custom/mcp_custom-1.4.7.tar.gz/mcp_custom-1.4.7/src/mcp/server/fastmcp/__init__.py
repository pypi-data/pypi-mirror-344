"""FastMCP - A more ergonomic interface for MCP servers."""

from importlib.metadata import version, PackageNotFoundError
from .server import Context, FastMCP
from .utilities.types import Image

try:
    __version__ = version("mcp-custom") 
    __all__ = ["FastMCP", "Context", "Image"]
except PackageNotFoundError:
    __version__ = "1.4.7"
    __all__ = ["FastMCP", "Context", "Image"]
