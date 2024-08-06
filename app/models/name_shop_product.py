from app.config.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, TIMESTAMP


class nameShopProduct(Base):
    __tablename__ = 'name_shop_product'

    id = Column(Integer, primary_key=True, index=True)
    id_name_shop = Column(String, ForeignKey('names_shop.id'))
    id_product = Column(String, ForeignKey('products.id'))
    max_invoice = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                    nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                    default=None, onupdate=func.now())