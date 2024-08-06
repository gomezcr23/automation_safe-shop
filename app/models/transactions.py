from app.config.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Double, TIMESTAMP

class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    id_transaction = Column(String)
    amount_in_cents = Column(Double)
    customer_email = Column(String)
    phone_number = Column(Integer)
    full_name = Column(String)
    num_document =  Column(String)
    type_document =  Column(String)
    type_person =  Column(String)
    address_line_1_shipping = Column(String)
    country_shipping = Column(String)
    region_shipping = Column(String)
    city_shipping = Column(String)
    name_shipping = Column(String)
    phone_number_shipping = Column(Integer)
    postal_code_shipping = Column(Integer)
    products = Column(String)
    payment_method_type = Column(String, nullable=True)
    status = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
    nullable=False, default=func.now())