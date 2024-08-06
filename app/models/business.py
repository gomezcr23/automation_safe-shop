from app.config.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, TIMESTAMP


class Business(Base):
    __tablename__ = 'business'

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    name = Column(String, unique=True)
    type_document = Column(String)
    num_document = Column(String)
    phone_number = Column(Integer, unique=True)
    country = Column(String)
    state = Column(String)
    city = Column(String)
    address = Column(String)
    postal_code = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())