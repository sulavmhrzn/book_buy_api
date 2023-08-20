from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 8000
    DEBUG: bool = True
    MONGO_URI: str
    MONGO_DB: str
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_PORT: int
    SMTP_HOST: str
    JWT_SECRET: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
