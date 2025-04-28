from typing import List
from .client import MimirClient
from .types import Repository


class RepositoriesAPI:
    """API methods for working with repositories."""

    def __init__(self, client: MimirClient):
        self._client = client

    async def list(self) -> List[Repository]:
        """List repositories for a user."""
        return await self._client.request(
            method="GET",
            endpoint="/repositories/"
        )
