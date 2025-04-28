"""
Mimir API: Python client library for the Mimir AI platform.

This library provides programmatic access to Mimir's repository analysis 
and code intelligence tools through a simple API client.

Website: https://trymimir.ai
Author: Justin Garofolo (justin@trymimir.ai)
Copyright (c) 2025 Mimir AI
"""

from .client import MimirClient, MimirConfig, load_config
from .repositories import RepositoriesAPI
from .tools import ToolsAPI

__author__ = "Justin Garofolo"
__email__ = "justin@trymimir.ai"
__website__ = "https://trymimir.ai"

__all__ = [
    "MimirClient",
    "MimirConfig",
    "load_config",
    "RepositoriesAPI",
    "ToolsAPI"
]
