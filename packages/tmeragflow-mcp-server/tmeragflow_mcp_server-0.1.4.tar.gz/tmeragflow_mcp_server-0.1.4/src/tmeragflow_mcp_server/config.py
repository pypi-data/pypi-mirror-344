from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RAGFLOW_API_KEY: str

    # class Config:
    #     env_prefix = "RAGFLOW_"

settings = Settings()