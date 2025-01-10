from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Open Configurator API"
    admin_email: str
    env = SettingsConfigDict(env_file=".env")


settings = Settings()
