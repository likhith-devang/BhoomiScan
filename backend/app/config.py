from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://bhoomiscan:bhoomiscan@localhost:5432/bhoomiscan"
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440
    MAX_FILE_SIZE_MB: int = 10
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    STORAGE_DIR: Path = ROOT_DIR / "storage" / "documents"
    SARVAM_API_KEY: str = ""
    SARVAM_POLL_SECONDS: int = 3
    SARVAM_MAX_WAIT_SECONDS: int = 120
    # On startup, promote this username to SUPER_ADMIN if the account already exists.
    BOOTSTRAP_SUPER_ADMIN_USERNAME: str = ""

    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
