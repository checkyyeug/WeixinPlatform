import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据库配置
    # 格式: "mysql+pymysql://user:password@host:port/dbname"
    DATABASE_URL: str = "mysql+pymysql://root:password@127.0.0.1:3306/mydatabase"

    # 微信小程序配置
    WECHAT_APP_ID: str = "your_wechat_app_id"
    WECHAT_APP_SECRET: str = "your_wechat_app_secret"

    # JWT (Token) 配置
    SECRET_KEY: str = "a_very_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        # 如果存在 .env 文件，则从中读取配置
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()