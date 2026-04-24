"""
Cognee - Knowledge graph and memory layer for AI applications.

This package provides tools for building, managing, and querying
knowledge graphs powered by LLMs.
"""

from cognee.api.v1.cognify import cognify
from cognee.api.v1.add import add
from cognee.api.v1.search import search
from cognee.api.v1.prune import prune
from cognee.config import Config

__version__ = "0.1.0"
__author__ = "Cognee Contributors"

__all__ = [
    "cognify",
    "add",
    "search",
    "prune",
    "Config",
    "__version__",
]
