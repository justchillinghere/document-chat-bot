from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.Collection import Collection
from models.base import Base

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	telegram_id = Column(Integer, nullable=False, unique=True)
	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
	collections = relationship("Collection", back_populates="user", cascade="all, delete-orphan",)
