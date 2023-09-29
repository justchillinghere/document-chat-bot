from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Collection(Base):
	__tablename__ = 'collections'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship("User", back_populates="collections")
	collection_name = Column(String)
	created_at = Column(DateTime, default=datetime.utcnow)
	other_info = Column(String)
