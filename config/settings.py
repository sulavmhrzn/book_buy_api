from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 8000
    DEBUG: bool = True
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
