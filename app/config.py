from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

env = load_dotenv()

class SMTPConfig(BaseSettings):
    host: str
    port: int
    username: str = ""
    password: str = ""
    use_tls: bool = True

    model_config = SettingsConfigDict(
        env_prefix="SMTP_",
        case_sensitive=False,
    )

    
smtp_settings = SMTPConfig()
