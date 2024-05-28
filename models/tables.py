from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text
)
from sqlalchemy.orm import (
    relationship,
    DeclarativeBase,
    mapped_column,
    Mapped
)
from db import pg_engine


class Serializable():
    def to_dict(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}


class Base(DeclarativeBase, Serializable):
    pass


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True,
                                    unique=True)
    asin: Mapped[str] = mapped_column(String(10),
                                      unique=True)
    title: Mapped[str] = mapped_column(String(128))
    reviews = relationship('Review', back_populates='product')

    def __repr__(self):
        return f"Product(id={self.id}, asin={self.asin}, title={self.title})"


class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True,
                                    unique=True)
    asin: Mapped[str] = mapped_column(String(10),
                                      ForeignKey('products.asin'))
    title: Mapped[str] = mapped_column(String(128))
    review: Mapped[str] = mapped_column(Text)
    product = relationship('Product', back_populates='reviews')

    def __repr__(self):
        return f"Product(id={self.id}, asin={self.asin}, title={self.title},review={self.review})"


Base.metadata.create_all(pg_engine)
