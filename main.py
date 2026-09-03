import flask
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from pip._internal.utils import datetime
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped
import datetime


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)

    cart_items: Mapped[list["CartItem"]] = relationship()
    orders: Mapped[list["Order"]] = relationship()


class Product(db.Model):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=False)
    price: Mapped[float] = mapped_column(float, nullable=False)
    photo_url: Mapped[str] = mapped_column(String(300), nullable=False)

    cart_items: Mapped[list["CartItem"]] = relationship()
    order_items: Mapped[list["OrderItems"]] = relationship()


class CartItem(db.Model):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))
    product_id: Mapped[int] = mapped_column(db.ForeignKey('product.id'))

    user: Mapped["User"] = relationship()
    product: Mapped["Product"] = relationship()

class Order(db.Model):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total: Mapped[float] = mapped_column(float, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))

    user: Mapped["User"] = relationship()
    order_items: Mapped[list["OrderItems"]] = relationship()

class OrderItems(db.Model):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(float, nullable=False)

    product_id: Mapped[int] = mapped_column(db.ForeignKey('product.id'))
    order_id: Mapped[int] = mapped_column(db.ForeignKey('order.id'))

    product: Mapped["Product"] = relationship()
    order: Mapped["Order"] = relationship()