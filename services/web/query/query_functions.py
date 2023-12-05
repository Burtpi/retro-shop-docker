from datetime import datetime
from config import db
from models import User, Product, ShippingAddress, Order, OrderProduct


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_products():
    return Product.query.all()


def get_product(id):
    return Product.query.get(id)


def post_shipping_address(first_name, last_name, shipping_address, city, state, zip_code, email, country, user_id):
    address = get_shipping_address(first_name, last_name, shipping_address, city, state, zip_code, email, country,
                                   user_id)
    if address:
        return
    else:
        new_address = ShippingAddress(first_name=first_name, last_name=last_name, shipping_address=shipping_address,
                                      city=city, state=state, zip_code=zip_code, email=email, country=country,
                                      user_id=user_id)
        db.session.add(new_address)
        db.session.commit()


def update_shipping_address(first_name, last_name, shipping_address, city, state, zip_code, email, country, user_id):
    address = get_shipping_address_by_user(user_id)

    if address:
        address.first_name = first_name
        address.last_name = last_name
        address.shipping_address = shipping_address
        address.city = city
        address.state = state
        address.zip_code = zip_code
        address.email = email
        address.country = country
        db.session.commit()
    else:
        post_shipping_address(first_name, last_name, address, city, state, zip_code, email, country, user_id)


def get_shipping_address(first_name, last_name, shipping_address, city, state, zip_code, email, country, user_id):
    if user_id is None:
        return ShippingAddress.query.filter_by(
            first_name=first_name, last_name=last_name, shipping_address=shipping_address,
            city=city, state=state, zip_code=zip_code, email=email, country=country).first()
    else:
        return ShippingAddress.query.filter_by(
            first_name=first_name, last_name=last_name, shipping_address=shipping_address,
            city=city, state=state, zip_code=zip_code, email=email, country=country, user_id=user_id).first()


def get_shipping_address_by_user(user_id):
    return ShippingAddress.query.filter_by(user_id=user_id).first()


def post_order(address_id, user_id, total_amount):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_order = Order(address_id=address_id, user_id=user_id, order_date=time_now, total_amount=total_amount)
    db.session.add(new_order)
    db.session.commit()
    return new_order.order_id


def get_order_id(address_id, user_id, time, total_amount):
    print(time)
    if user_id is None:
        return Order.query.filter_by(address_id=address_id, order_date=time,
                                     total_amount=round(total_amount, 2)).first()
    else:
        return Order.query.filter_by(address_id=address_id, user_id=user_id, order_date=time,
                                     total_amount=round(total_amount, 2)).first()


def get_order(user_id):
    return Order.query.filter_by(user_id=user_id).all()


def post_order_consoles(order_id, console_id):
    new_order_console = OrderProduct(order_id=order_id, product_id=console_id)
    db.session.add(new_order_console)
    db.session.commit()
