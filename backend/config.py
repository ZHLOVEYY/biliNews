from pydantic_settings import BaseSettings
from pydantic_settings import BaseSettings, Field
import os

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = Field(default=os.getenv("OPENROUTER_API_KEY", ""))
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'

settings = Settings()

# 验证关键配置
if not settings.OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY 未设置，请确保在系统环境变量中设置")