from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    RAGFLOW_API_KEY: str

    # class Config:
    #     env_prefix = "RAGFLOW_"
    model_config = SettingsConfigDict()

settings = Settings()