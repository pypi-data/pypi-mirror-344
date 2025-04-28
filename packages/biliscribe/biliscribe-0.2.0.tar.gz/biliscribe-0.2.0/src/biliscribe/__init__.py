import asyncio

from . import server

__version__ = "0.2.0"

def main():
    asyncio.run(server.main())

__all__ = [
    "__version__",
    "main",
    "server",
]