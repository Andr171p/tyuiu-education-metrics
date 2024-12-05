import asyncio
import aiohttp
from typing import Any, Dict, List


class HTTPClient:
    @staticmethod
    def is_ok(response: aiohttp.ClientResponse) -> bool:
        return True if response.status == 200 else False

    async def fetch_one(
            self,
            session: aiohttp.ClientSession,
            url: str,
            params: Dict[str, Any]
    ) -> Dict[str, Any]:
        async with session.get(
                url=url,
                params=params
        ) as response:
            if self.is_ok(response):
                return await response.json()

    async def fetch_all(
            self,
            urls: List[str],
            params_list: List[Dict[str, Any]]
    ) -> tuple:
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_one(session, url, params)
                for url, params in zip(urls, params_list)
            ]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            return responses
