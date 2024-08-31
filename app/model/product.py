from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.model.base import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'product'
    prdno: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    prdname: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[str] = mapped_column(String(20), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    description: Mapped[str] = mapped_column(String(100))
    regdate: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=True)

    # carts = relationship("Cart", back_populates="product")
    attachs = relationship('Prdattach', back_populates='product')

class PrdAttach(Base):
    __tablename__ = 'prdattach'
    prdatno: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    prdno: Mapped[int] = mapped_column(Integer, ForeignKey('product.prdno'))
    img1 = Column(String(50), nullable=False)
    img2 = Column(String(50), nullable=False)
    img3 = Column(String(50), nullable=False)
    img4 = Column(String(50), nullable=False)
    product = relationship('Product', back_populates='attachs')


# class Cart(Base):
#     __tablename__ = 'cart'
#     cno: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     mno: Mapped[int] = mapped_column(Integer, ForeignKey('member.mno'), nullable=False)
#     prdno: Mapped[int] = mapped_column(Integer, ForeignKey('product.prdno'), nullable=False)
#     qty: Mapped[int] = mapped_column(Integer, nullable=False)
#     price: Mapped[int] = mapped_column(Integer, nullable=False)
#
#     product = relationship("Product", back_populates="carts")