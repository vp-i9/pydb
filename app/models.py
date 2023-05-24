from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine

# from db import Base
from sqlalchemy.orm import sessionmaker

# from models import User, Post
from datetime import datetime

Base = declarative_base()


class Vendor(Base):
    """Vendor class which inludes ID, abbreviation, name, and list of products."""

    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True)
    abbrev = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    products = relationship("Product", back_populates="vendor")

    def __str__(self):
        return f"This is vendor information: {self.name}, listed as {self.abbrev}"


class Product(Base):
    """Product class which includes ID, reference number, expiry date, size, etc."""

    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    id_reference = Column(String, nullable=False, index=True)
    id_expiry_date = Column(String, nullable=False, index=True)
    ref_id_expiry_date = Column(String)
    name = Column(String, nullable=False)
    category = Column(String)
    size = Column(String)
    quantity_on_hand = Column(Integer, nullable=False, default=1)
    quantity_on_order = Column(Integer, nullable=False, default=0)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    vendor = relationship("Vendor", back_populates="products")

    # # Add unique constraint for reference_id and expiry_date
    # __table_args__ = (
    #     UniqueConstraint("id_reference", "id_expiry_date"),
    # )

    def __str__(self):
        return f"Product Reference Information: {self.name}, Quantity of product available: {self.quantity_on_hand}"


class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    vendor_abbrev = Column(String, ForeignKey("vendors.abbrev"))
    quantity = Column(Integer, nullable=False, default=1)
    date = Column(DateTime, nullable=False)
    product = relationship("Product", foreign_keys=[product_id])
    vendor = relationship("Vendor", foreign_keys=[vendor_abbrev])

    def __str__(self):
        return f"Purchase reference information: {self.vendor_abbrev}-{self.product_id}"
