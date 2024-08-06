from app.config.database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Double, TIMESTAMP


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    price = Column(Double)
    descr = Column(String)
    descr_long = Column(String)
    type = Column(String)
    path_img = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                    nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                    default=None, onupdate=func.now())