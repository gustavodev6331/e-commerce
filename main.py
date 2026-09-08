import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Numeric, DateTime
from datetime import datetime
from decimal import Decimal


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///shop.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


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
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
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
    total: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))

    user: Mapped["User"] = relationship()
    order_items: Mapped[list["OrderItems"]] = relationship()

class OrderItems(db.Model):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)

    product_id: Mapped[int] = mapped_column(db.ForeignKey('product.id'))
    order_id: Mapped[int] = mapped_column(db.ForeignKey('order.id'))

    product: Mapped["Product"] = relationship()
    order: Mapped["Order"] = relationship()

with app.app_context():
    db.create_all()