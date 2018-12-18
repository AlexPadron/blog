import os

from grift import BaseConfig, ConfigProperty, EnvLoader, JsonFileLoader
from schematics.types import StringType, BooleanType, IntType


class AppConfig(BaseConfig):
    FLASK_HOST = ConfigProperty(property_type=StringType(), default='127.0.0.1')
    FLASK_PORT = ConfigProperty(property_type=IntType(), default=8000)
    FLASK_DEBUG = ConfigProperty(property_type=BooleanType(), default=True)


loaders = [EnvLoader()]
settings_path = os.environ.get('SETTINGS_PATH')

if settings_path is not None:
    loaders.append(JsonFileLoader(settings_path))

app_config = AppConfig(loaders)
