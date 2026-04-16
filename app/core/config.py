from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    USUARIO_DATABASE_URL: str = Field(..., env="USUARIO_DATABASE_URL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALG: str = Field(default="HS256", env="JWT_ALG")
    JWT_EXPIRES_MIN: int = Field(default=60*24, env="JWT_EXPIRES_MIN")
    PROJECT_NAME: str = "SVIP"
    ENVIRONMENT: str = Field(..., env="ENVIRONMENT")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()