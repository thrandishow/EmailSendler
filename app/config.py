import os
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


smtp_config = SMTPConfig()
