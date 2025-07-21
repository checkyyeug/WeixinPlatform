from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 创建数据库引擎
# connect_args 是特定于 SQLite 的，对于 MySQL/PostgreSQL，可以移除
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True,
    # connect_args={"check_same_thread": False} # 仅用于 SQLite
)

# 创建一个 SessionLocal 类
# 每个 SessionLocal 实例都将是一个数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)