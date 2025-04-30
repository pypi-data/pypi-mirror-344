from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ragflow_api_key: str = ""

    class Config:
        env_prefix = "RAGFLOW_"

settings = Settings()