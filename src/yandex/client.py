import asyncio
import aiohttp
from typing import Any, Dict, List


def is_ok(response: aiohttp.ClientResponse) -> bool:
    return True if response.status == 200 else False


async def fetch(
        session: aiohttp.ClientSession,
        url: str,
        params: Dict[str, Any]
) -> Dict[str, Any]:
    async with session.get(
        url=url,
        params=params
    ) as response:
        return await response.json()


async def fetch_all(
        loop: asyncio.AbstractEventLoop,
        urls: List[str],
        params_list: List[Dict[str, Any]]
) -> ...:
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [
            fetch(session, url, params)
            for url, params in zip(urls, params_list)
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses
