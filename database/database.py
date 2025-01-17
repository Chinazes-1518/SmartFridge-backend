from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import ForeignKey, Integer, String, JSON, DateTime
from datetime import datetime
from typing import Optional


class MyBase(DeclarativeBase):
    pass


class ProductCategories(MyBase):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)


class ProductTypes(MyBase):
    __tablename__ = "product_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey(ProductCategories.id, ondelete="CASCADE"))
    amount: Mapped[float]
    units: Mapped[str]  # например, г, мл
    nutritional: Mapped[int]  # в ккал
    measure_type: Mapped[str]  # например, штуки, вес
    allergens: Mapped[Optional[str]]


class Products(MyBase):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey(ProductTypes.id, ondelete="CASCADE"))
    production_date: Mapped[datetime]
    expiry_date: Mapped[datetime]


class Users(MyBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    password_hash: Mapped[str]


class ActiveTokens(MyBase):
    __tablename__ = "active_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id, ondelete="CASCADE"))
    token: Mapped[str] = mapped_column(unique=True)


class BuyList(MyBase):
    __tablename__ = "buylist"

    id: Mapped[int] = mapped_column(primary_key=True)
    prod_type_id: Mapped[int] = mapped_column(ForeignKey(ProductTypes.id, ondelete="CASCADE"))
    amount: Mapped[int]


class Analytics(MyBase):
    __tablename__ = "analytics"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, unique=True)
    data: Mapped[dict] = mapped_column(JSON)  # словарь {айди типа товара: колво проданных}
