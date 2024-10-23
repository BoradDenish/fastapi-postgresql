from sqlalchemy import Column, Integer, String, Boolean, text, TIMESTAMP
from config.connection import Base



class User(Base):
    __tablename__ = "users"

    user_id         = Column(Integer,primary_key=True,nullable=False)
    user_name       = Column(String,nullable=False)
    user_email      = Column(String,nullable=False)
    user_password   = Column(String,nullable=False)
    simple_password = Column(String,nullable=False)
    user_status     = Column(Boolean, server_default='TRUE')
    created_at      = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at      = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at      = Column(TIMESTAMP(timezone=True), nullable=True)