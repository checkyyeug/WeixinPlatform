from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.sql import func

from app.db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    openid = Column(String(128), unique=True, index=True, nullable=False)
    session_key = Column(String(128), nullable=False)
    unionid = Column(String(128), unique=True, index=True, nullable=True)
    nickname = Column(String(255), nullable=True)
    avatar_url = Column(String(512), nullable=True)
    gender = Column(TINYINT, default=0)
    mobile = Column(String(20), unique=True, index=True, nullable=True)
    last_login_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())