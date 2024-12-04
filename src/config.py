import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR: Path = Path(__file__).resolve().parent.parent

ENV_PATH: Path = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


class YandexAPIConfig(BaseSettings):
    key: str = os.getenv("YANDEX_API_KEY")
    base_url: str = os.getenv("YANDEX_BASE_URL")


class Config(BaseSettings):
    yandex_api: YandexAPIConfig = YandexAPIConfig()


config = Config()
