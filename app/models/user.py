from app.config.database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, TIMESTAMP


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    name = Column(String)
    lastname = Column(String)
    type_document = Column(String)
    num_document = Column(Integer, unique=True)
    phone_number = Column(Integer, unique=True)
    type_person = Column(String)
    country = Column(String)
    state = Column(String)
    city = Column(String)
    position = Column(String, nullable=True)
    address = Column(String, unique=True)
    postal_code = Column(String)
    hashed_password = Column(String)
    token_payment = Column(String, nullable=True, unique=True)
    type_payment = Column(String, nullable=True)
    id_source_payment = Column(Integer, nullable=True, unique=True)
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())