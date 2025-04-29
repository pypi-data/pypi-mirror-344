from sqlalchemy import Column, Integer, String, Float, Date
from .db import Base

class Device(Base):
    """
    ORM model representing a device entry in the PostgreSQL database.

    Example Record:
        Office Printer Pro, 299.99, MP-2000, HP, SN001, 2024-01-15, 50.0359, 19.1784

    Attributes:
        id (int): (e.g., 1).
        device_name (str): (e.g., "Office Printer Pro").
        price (float): (e.g., 299.99).
        model (str): (e.g., "MP-2000").
        brand (str): (e.g., "HP").
        serial_number (str): (e.g., "SN001").
        date (date): (e.g., 2024-01-15).
        brand_code (str): (e.g., "50.0359").
        product_number (str): (e.g., "19.1784").
    """
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    model = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    serial_number = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    brand_code = Column(String, nullable=False)
    product_number = Column(String, nullable=False)
