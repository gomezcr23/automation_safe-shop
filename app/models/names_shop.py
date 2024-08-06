from app.config.database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, TIMESTAMP


class namesShop(Base):
    __tablename__ = 'names_shop'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    path_img = Column(String, unique=True)
    created_at = Column(TIMESTAMP(timezone=True),
                    nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                    default=None, onupdate=func.now())