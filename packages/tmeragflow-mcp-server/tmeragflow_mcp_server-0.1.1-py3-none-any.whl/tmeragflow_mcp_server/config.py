from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    class Config:
        env_prefix = "RAGFLOW_"

settings = Settings()