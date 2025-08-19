from urllib.parse import quote_plus
from pydantic.config import BaseSettings
from pydantic import Field


class SMTPConfig(BaseSettings):
    host: str = Field(..., description="SMTP server host")
    port: int = Field(..., description="SMTP server port")
    username: str = Field(..., description="SMTP server username")
    password: str = Field(..., description="SMTP server password")
    from_email: str = Field(
        ..., description="Email отправителя (например: noreply@domain.com)"
    )
    use_tls: bool = Field(True, description="Использовать TLS шифрование")
    timeout: int = Field(10, description="Таймаут подключения в секундах")

    class Config:
        env_prefix = "SMTP_"
        secrets_dir = "/run/secrets"


class PostgreSQLConfig(BaseSettings):
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: str = Field(..., env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def DATABASE_URL(self) -> str:
        password = quote_plus(self.DB_PASSWORD)
        return f"postgresql+asyncpg://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


smtp_config = SMTPConfig()
postgres_config = PostgreSQLConfig()

if not all(
    [
        postgres_config.DB_USER,
        postgres_config.DB_PASSWORD,
        postgres_config.DB_HOST,
        postgres_config.DB_PORT,
        postgres_config.DB_NAME,
    ]
):
    raise RuntimeError(
        "Отсутствуют необходимые переменные окружения для подключения к БД"
    )
