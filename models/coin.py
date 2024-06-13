from sqlalchemy import  Column, String, Float
from config.config_base import Base


class Price(Base):
    __tablename__ = "prices"
    currency = Column(String, primary_key=True, index=True)
    value = Column(Float, index=True)
