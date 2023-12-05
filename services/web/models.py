from flask_security import RoleMixin, UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from database import db


class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(50), nullable=False, unique=True)
    manufacturer = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    orders = relationship('OrderProduct', back_populates='product')


class OrderProduct(db.Model):
    __tablename__ = 'order_products'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True)

    order = relationship('Order', back_populates='products')
    product = relationship('Product', back_populates='orders')


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True, default=None)
    address_id = db.Column(db.Integer, db.ForeignKey('shippingaddresses.address_id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

    user = relationship('User', back_populates='orders')
    address = relationship('ShippingAddress', back_populates='orders')
    products = relationship('OrderProduct', back_populates='order')


class ShippingAddress(db.Model, RoleMixin):
    __tablename__ = 'shippingaddresses'
    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True, default=None)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)

    user = relationship('User', back_populates='shipping_address')
    orders = relationship('Order', back_populates='address')


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), default=None, unique=True, nullable=False)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    tf_totp_secret = db.Column(db.String(255), nullable=True)
    tf_primary_method = db.Column(db.String(64), nullable=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    roles = relationship(
        "Role", secondary="roles_users", backref=backref("users", lazy="dynamic")
    )

    orders = relationship('Order', back_populates='user')
    shipping_address = relationship('ShippingAddress', back_populates='user')


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, ForeignKey("users.user_id"))
    role_id = db.Column("role_id", db.Integer, ForeignKey("roles.role_id"))


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
