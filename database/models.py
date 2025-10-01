from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import BigInteger, Column, String, Float, DateTime, func, Integer, ForeignKey, Boolean

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String(32), nullable=True)
    full_name = Column(String(255), nullable=False)
    balance = Column(Float, default=100.0)

    created_at = Column(DateTime, default=func.now())

    cart_items = relationship("Cart", back_populates="user")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)

    is_active = Column(Boolean, default=True)

class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="cart_items")