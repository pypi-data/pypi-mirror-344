"""
Browser Use MCP - An unofficial Model Context Protocol server for automating browser tasks using Browser Use API.
This package is not provided or endorsed by Browser Use.
"""

__version__ = "0.1.0"

from . import server
import asyncio


def main():
    """Main entry point for the package."""
    asyncio.run(server.main())


# Optionally expose other important items at package level
__all__ = ["main", "server"]