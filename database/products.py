from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import ForeignKey


class ProductCategories(DeclarativeBase):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class ProductTypes(DeclarativeBase):
    __tablename__ = "product_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey(ProductCategories.id, ondelete="CASCADE"))
    weight: Mapped[int]
    amount: Mapped[int]
    nutritional: Mapped[int]
    measure_type: Mapped[str]
    allergens: Mapped[str]

