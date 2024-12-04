import aiohttp
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from src.yandex.schemas import GeopointsSchema
from src.config import config


@dataclass
class YandexGeocoder:
    api_key: str = config.yandex_api.key
    geocoder_url: str = config.yandex_api.base_url

    @staticmethod
    def _is_ok(response: aiohttp.ClientResponse) -> bool:
        return True if response.status == 200 else False

    async def address_to_geopoint(self, address: str) -> List[float] | None:
        params: Dict[str, Any] = {
            'apikey': self.api_key,
            'geocode': address,
            'format': 'json'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.geocoder_url,
                params=params
            ) as response:
                if self._is_ok(response=response):
                    data = await response.json()
        geopoint: List[dict] = data['response']['GeoObjectCollection']['featureMember']
        if len(geopoint) == 0:
            return
        lat, lon = geopoint[0]['GeoObject']['Point']['pos'].split(' ')
        return self._to_datalens_response(lon, lat)

    @staticmethod
    def _to_datalens_format(lon: str, lat: str) -> str:
        return f"[{lon}, {lat}]"

    @staticmethod
    def _to_datalens_response(*args, **kwargs) -> Optional[GeopointsSchema]:
        if len(args) == 2 and all(isinstance(arg, str) for arg in args):
            return GeopointsSchema.from_str_points(*args)
        elif kwargs and set(kwargs.keys()).issubset({'lon', 'lat'}):
            return GeopointsSchema(**kwargs)
