# Mimir API

[![PyPI Version](https://img.shields.io/pypi/v/mimir-api?style=for-the-badge&color=%230094FF)](https://pypi.org/project/mimir-api/)

Python API client for the Mimir AI platform. This library provides programmatic access to Mimir's repository analysis and code intelligence tools.

## Installation

You can install the package directly from PyPI:

```bash
pip install mimir-api
```

Alternatively, you can clone the repository and install the package locally:

```bash
# Clone the repository
git clone https://github.com/trymimirai/mimir-api.git
cd mimir-api

# Install the package
pip install -e .
```

## Configuration

The client requires configuration for the API base URL and authentication key. These can be provided in three different ways:

1. **Environment Variables** (prioritized):

   - `MIMIR_API_URL`: The base URL for the API (optional, default: "https://dev.trymimir.ai/api")
   - `MIMIR_API_KEY`: Your API authentication key

2. **Configuration File** (used when environment variables are missing):
   Create a file at `~/.mimir/config.json` with the following structure:

   ```json
   {
     "api_url": "https://dev.trymimir.ai/api",
     "api_key": "your-api-key-here"
   }
   ```

3. **Manual Initialization**:
   Directly create a `MimirConfig` object in your code:

   ```python
   from mimir_api import MimirClient, MimirConfig

   # Create config manually
   config = MimirConfig(
       base_url="https://dev.trymimir.ai/api",
       api_key="your-api-key-here"
   )

   # Initialize the client with the config
   client = MimirClient(config)
   ```

## Getting Started

```python
import asyncio
from mimir_api import MimirClient, load_config, MimirConfig

async def main():
    # Option 1: Load from environment or config file
    config = load_config()
    client1 = MimirClient(config)

    # Option 2: Create config manually
    manual_config = MimirConfig(
        base_url="https://dev.trymimir.ai/api",
        api_key="your-api-key-here"
    )
    client2 = MimirClient(manual_config)

    # Example: List repositories
    repos = await client1.repositories.list()
    print(f"Found {len(repos)} repositories")

    # Example: Search for files in a repository
    if repos:
        repo = repos[0]
        results = await client1.tools.agentic_file_search(
            owner=repo["owner"],
            name=repo["name"],
            query="authentication implementation"
        )
        print(results)

asyncio.run(main())
```

## Available APIs

The client provides access to the following APIs:

### Repositories API

- `list()` - List repositories for the authenticated user

### Tools API

Code intelligence tools for analyzing repositories:

- `agentic_file_search()` - Find relevant files using natural language search
- `vector_search()` - Find code snippets with high similarity to a query
- `text_search()` - Search for text patterns across the codebase (like grep)
- `read_file()` - Read the contents of a specific file
- `list_directory()` - List files and directories in a specific path
