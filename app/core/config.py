from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    APP_ENV: str = 'local'
    PROJECT_NAME: str = 'argowf-api-local'
    API_V1_STR: str = '/api/v1'

# os.environ["APP_ENV"] = 'dev'

settings = Settings(_env_file=f'conf/{os.getenv("APP_ENV")}.env')