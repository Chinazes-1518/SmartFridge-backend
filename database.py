from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import ForeignKey, Integer, String, JSON
from datetime import datetime


class ProductCategories(DeclarativeBase):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)


class ProductTypes(DeclarativeBase):
    __tablename__ = "product_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey(ProductCategories.id, ondelete="CASCADE"))
    weight: Mapped[int]
    amount: Mapped[int]
    nutritional: Mapped[int]
    measure_type: Mapped[str]
    allergens: Mapped[str]


class Products(DeclarativeBase):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey(ProductTypes.id, ondelete="CASCADE"))
    production_date: Mapped[datetime]
    expiry_date: Mapped[datetime]


class Organisations(DeclarativeBase):
    __tablename__ = "organisations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Users(DeclarativeBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey(Organisations.id, ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]


class BuyList(DeclarativeBase):
    __tablename__ = "buylist"

    id: Mapped[int] = mapped_column(primary_key=True)
    prod_type_id: Mapped[int] = mapped_column(ForeignKey(ProductTypes.id, ondelete="CASCADE"))
    amount: Mapped[int]


class Analytics(DeclarativeBase):
    __tablename__ = "analytics"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(datetime, unique=True)
    data: Mapped[dict] = mapped_column(JSON)  # словарь {айди типа товара: колво проданных}
