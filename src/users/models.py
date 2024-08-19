from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from datetime import datetime
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from database import Base

if TYPE_CHECKING:
    from converter.models import User



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    operations = relationship("Operation", back_populates="user")


