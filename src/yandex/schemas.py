from pydantic import BaseModel, field_validator


class GeopointsSchema(BaseModel):
    lon: float
    lat: float

    @field_validator(*['lon', 'lat'])
    @classmethod
    def validate_lon(cls, value: str) -> float:
        return float(value)

    @classmethod
    def from_str_points(cls, lon: str, lat: str) -> "GeopointsSchema":
        return cls(lon=lon, lat=lat)
