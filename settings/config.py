from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DEEPL_API_KEY: str = ''

    CHAT_GPT_API_KEY: str = ''
    OPENAI_ORG_ID: str = ''
    PROJECT_ID: str = ''

    class Config:
        env_file = Path(BASE_DIR, 'settings', 'env')


settings = Settings()
