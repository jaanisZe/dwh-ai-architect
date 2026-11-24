from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "dwh_mart"
    db_user: str = "ai_reader"
    db_password: str
    query_timeout_seconds: int = 10
    semantic_layer_path: str = "config/semantic_layer.yaml"
    llm_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def db_uri(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
