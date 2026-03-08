from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    CLICKHOUSE_HOST: str = "localhost"
    CLICKHOUSE_PORT: int = 8123
    CLICKHOUSE_USER: str = "default"
    CLICKHOUSE_PASSWORD: str = "REstart@789"
    CLICKHOUSE_DB: str = "business_ops"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()