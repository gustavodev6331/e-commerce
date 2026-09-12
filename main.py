import os
from urllib import request

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Numeric, DateTime
from datetime import datetime
from decimal import Decimal
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

import os
from dotenv import load_dotenv


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

#creatin login-manager
login_manager = LoginManager()
login_manager.init_app(app)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///shop.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(UserMixin ,db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)

    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="user")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")


class Product(db.Model):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(300), nullable=False)

    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="product")
    order_items: Mapped[list["OrderItems"]] = relationship(back_populates="product")


class CartItem(db.Model):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))
    product_id: Mapped[int] = mapped_column(db.ForeignKey('product.id'))

    user: Mapped["User"] = relationship(back_populates="cart_items")
    product: Mapped["Product"] = relationship(back_populates="cart_items")

class Order(db.Model):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))

    user: Mapped["User"] = relationship(back_populates="orders")
    order_items: Mapped[list["OrderItems"]] = relationship(back_populates="order")

class OrderItems(db.Model):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)

    product_id: Mapped[int] = mapped_column(db.ForeignKey('product.id'))
    order_id: Mapped[int] = mapped_column(db.ForeignKey('order.id'))

    product: Mapped["Product"] = relationship(back_populates="order_items")
    order: Mapped["Order"] = relationship(back_populates="order_items")

with app.app_context():
    db.create_all()


    # products = Product(
    #     name="Developer T-shirt",
    #     description="A T-shirt made for developers",
    #     price=29.99,
    #     photo_url="https://shirt.com",
    # )
    # db.session.add(products)
    # products_2 = Product(
    #     name="Gamer Keyboard",
    #     description="The perfect keyboard for who love gaming",
    #     price=49.99,
    #     photo_url="https://keyboard.com",
    # )
    # db.session.add(products_2)
    # products_3 = Product(
    #     name="Developer chair",
    #     description="The most comfortable chair for developers who have to work hours a day.",
    #     price=89.99,
    #     photo_url="https://developerchair.com",
    # )
    # db.session.add(products_3)
    #
    # db.session.commit()

def get_user_by_email(email):
    result= db.session.execute(db.select(User).where(User.email == email))
    return result.scalars()

@app.route('/')
def home():
    result = db.session.execute(db.select(Product))
    products = result.scalars().all()

    return render_template('index.html', products=products, logged_in=current_user.is_authenticated)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)
        )
        user = get_user_by_email(new_user.email)
        if user:
            flash("Email already registered, please login.")
            return redirect(url_for('login'))
        else:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))

    return render_template('register.html', logged_in=current_user.is_authenticated)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)

        if user is None:
            flash("Email does not exist, please login.")
            return redirect(url_for('login'))
        if check_password_hash(user.password, password=password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid password. Please try again.")
            return redirect(url_for('login'))

    return render_template('login.html', logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):



if __name__ == '__main__':
    app.run(debug=True)
