# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TITLE: str = "TRADE WITH CHUN"

    JWT_SECRET_KEY: str = "JWT_SECRET_KEY"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_IN_MINUTES: int = 10080  # 7 days
    REFRESH_TOKEN_EXPIRE_IN_DAYS: int = 28
    PAYSTACK_KEY: str = "sk_test_f1057904457b921cbb56b0a8b62a53ee5c4fd739"
    DATABASE_URL: str = "postgresql://chun:chunpass@45.33.77.191/chunbase"


settings = Settings()
