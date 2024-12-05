import asyncio
import aiohttp
import logging
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass

from src.yandex.schemas import GeopointsSchema
from src.yandex.client import HTTPClient
from src.config import config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dataclass
class YandexGeocoder(HTTPClient):
    api_key: str = config.yandex_api.key
    geocoder_url: str = config.yandex_api.base_url

    async def address_to_geopoint(self, address: str) -> List[float] | None:
        params: Dict[str, Any] = {
            'apikey': self.api_key,
            'geocode': address,
            'format': 'json'
        }
        async with aiohttp.ClientSession() as session:
            data = await self.fetch(
                session=session,
                url=config.yandex_api.base_url,
                params=params
            )
            print(data)
        lat, lon = self._get_position(data)
        logger.info(f"[{address}]: {lon}:{lat}")
        return self._to_datalens_response(lon, lat)

    async def addresses_to_geopoints(
            self,
            addresses: List[str]
    ) -> List[List[float]]:
        geopoints: List[List[float]] = []
        async with aiohttp.ClientSession():
            tasks = [
                self.address_to_geopoint(address)
                if address is not None else ''
                for address in addresses
            ]
            responses = await asyncio.gather(*tasks)
            for response in responses:
                geopoints.append(response)
        return geopoints

    @staticmethod
    def _get_position(data: Dict[str, Any]) -> Tuple[str, str] | None:
        geopoint: List[dict] = data['response']['GeoObjectCollection']['featureMember']
        if len(geopoint) == 0:
            return
        lat, lon = geopoint[0]['GeoObject']['Point']['pos'].split(' ')
        return lat, lon

    @staticmethod
    def _to_datalens_response(*args, **kwargs) -> Optional[GeopointsSchema]:
        if len(args) == 2 and all(isinstance(arg, str) for arg in args):
            return GeopointsSchema.from_str_points(*args)
        elif kwargs and set(kwargs.keys()).issubset({'lon', 'lat'}):
            return GeopointsSchema(**kwargs)


print(asyncio.run(YandexGeocoder().address_to_geopoint('')))
'''from src.etl.processor import UserEducation

if __name__ == "__main__":
    import asyncio
    addresses = UserEducation().get_users_educations()
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(addresses_to_geopoints(addresses))
    print(results)'''
