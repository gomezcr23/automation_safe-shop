from app.config.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, TIMESTAMP

class Subscriptions(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    id_product = Column(Integer, ForeignKey('products.id'))
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    status_renovation = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())