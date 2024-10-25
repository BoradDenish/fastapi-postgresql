from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, text, TIMESTAMP
from config.connection import Base
from sqlalchemy.orm import relationship



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

    session = relationship("Session", back_populates="user")


    
class Session(Base):
    __tablename__ = "user_session"

    session_id      = Column(Integer, primary_key=True, index=True)
    session_email   = Column(String(255))
    session_token   = Column(String(955))
    session_user    = Column(Integer, ForeignKey("users.user_id"))
    session_expiry  = Column(DateTime, default=datetime.now())
    session_status  = Column(Boolean, default=1)
    deleted_at      = Column(Boolean, default=0)
    created_at      = Column(DateTime, default=datetime.now(), nullable=True)
    updated_at      = Column(DateTime, nullable=True)

    user            = relationship("User", back_populates="session")
