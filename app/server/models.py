# models here - db diagram : https://dbdiagram.io/d/6304c4b5f1a9b01b0fc7dc8a

from sqlalchemy import Column, String, DateTime, Integer, Boolean

from app.server.database import Base


# user class
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    reg_at = Column(DateTime)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
