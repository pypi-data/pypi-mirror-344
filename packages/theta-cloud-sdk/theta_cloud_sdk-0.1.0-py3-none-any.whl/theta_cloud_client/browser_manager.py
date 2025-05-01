import asyncio
from theta_cloud_client import Client
from theta_cloud_client.models import CreateRequest, BrowserResponse
from theta_cloud_client.api.default import (
    create_browser_v1_browsers_post,
    get_browser_v1_browsers_sandbox_id_get,
    delete_browser_v1_browsers_sandbox_id_delete,
)


class BrowserManager:
    """
    Helper for managing browser sandboxes via the theta-cloud SDK.
    """
    def __init__(self, base_url: str, api_key: str):
        """Initialize the async client with base URL and API key."""
        self.client = Client(base_url=base_url)
        self.api_key = api_key

    async def create_one(self, headless: bool = False) -> str:
        """Creates one sandbox and returns its ID."""
        resp = await create_browser_v1_browsers_post.asyncio(
            client=self.client,
            body=CreateRequest(headless=headless),
            x_api_key=self.api_key,
        )
        return resp.id

    async def get_info(self, sandbox_id: str) -> BrowserResponse:
        """Fetches BrowserResponse for a single sandbox."""
        detailed = await get_browser_v1_browsers_sandbox_id_get.asyncio_detailed(
            sandbox_id=sandbox_id,
            client=self.client,
            x_api_key=self.api_key,
        )
        return detailed.parsed

    async def delete(self, sandbox_id: str) -> None:
        """Deletes one sandbox."""
        await delete_browser_v1_browsers_sandbox_id_delete.asyncio(
            sandbox_id=sandbox_id,
            client=self.client,
            x_api_key=self.api_key,
        )

    async def fleet_create(self, n: int, parallel: bool = True) -> list[str]:
        """Spin up a fleet of n sandboxes; returns list of sandbox IDs."""
        if parallel:
            return await asyncio.gather(*[self.create_one() for _ in range(n)])
        return [await self.create_one() for _ in range(n)]

    async def fleet_info(self, ids: list[str], parallel: bool = True) -> list[BrowserResponse]:
        """Fetch info for a fleet of sandboxes."""
        if parallel:
            return await asyncio.gather(*[self.get_info(s) for s in ids])
        return [await self.get_info(s) for s in ids]

    async def fleet_delete(self, ids: list[str], parallel: bool = True) -> None:
        """Tear down a fleet of sandboxes."""
        if parallel:
            await asyncio.gather(*[self.delete(s) for s in ids])
        else:
            for s in ids:
                await self.delete(s)
