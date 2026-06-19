import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "StudySync Core Engine"
    VERSION: str = "4.0.0"
    ENVIRONMENT: str = "production"

    SECRET_KEY: str = "ae734fca4b1e948fa390de25000000000000000000000000000000000000000"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Verify this matches your local MongoDB instance connection port URI
    MONGODB_URL: str = "mongodb://127.0.0.1:27017"
    DATABASE_NAME: str = "studysync"

    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=os.path.abspath(os.path.join(os.path.dirname(__file__), ".env")),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
