import random
from math import ceil

import flask_security
from flask import render_template, request, session, redirect, url_for, Blueprint, flash
from flask_login import login_required

from forms import CheckoutForm
from query.query_functions import get_user_by_username, get_products, get_product, post_shipping_address, \
    get_shipping_address, post_order, get_order, post_order_consoles, get_shipping_address_by_user, \
    update_shipping_address

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    products = get_products()
    selected_products = []
    if products:
        selected_products = random.sample(products, 8)
    username = session.get('username')
    return render_template("index.html", products=selected_products, username=username)


@main_bp.route('/all_products', methods=['GET'])
def all_products():
    if request.method == 'GET':
        products = get_products()
        page = int(request.args.get('page', 1))
        selected_manufacturers = request.args.getlist('manufacturers')
        items_per_page = 9
        manufacturers = set([product.manufacturer for product in products])
        if len(selected_manufacturers) != 0:
            products = [product for product in products if product.manufacturer in selected_manufacturers]
        max_page = ceil(len(products) / items_per_page)

        if page > max_page or page < 1:
            return redirect(url_for("main.all_products", page=1))

        start_index = (page - 1) * items_per_page
        end_index = page * items_per_page
        sliced_products = products[start_index:end_index]

        return render_template("allproducts.html", products=sliced_products, page=page, max_page=max_page,
                               manufacturers=manufacturers, selected_manufacturers=selected_manufacturers)


@main_bp.route('/add_to_cart/<id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = [id]
    else:
        if id not in session['cart']:
            session['cart'].append(id)
            session.modified = True
            flash('Added product to cart.', 'success')
        else:
            flash('This product is already in cart.', 'warning')

    return redirect(request.referrer)


@main_bp.route('/remove_from_cart/<id>', methods=['POST'])
def remove_from_cart(id):
    if request.method == 'POST':
        session['cart'].remove(id)
        session.modified = True
        return redirect(request.referrer)


@main_bp.route('/profile')
@login_required
def profile():
    user_id = get_user_by_username(flask_security.current_user.username).user_id
    orders = get_order(user_id)
    return render_template("profile.html", orders=orders)


@main_bp.route('/view_cart')
def view_cart():
    products = []
    if 'cart' in session:
        for product in session['cart']:
            products.append(get_product(product))
    return render_template("cart.html", products=products)


@main_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        if len(session['cart']) != 0:
            form = CheckoutForm()

            products = [get_product(product) for product in session['cart']]

            if flask_security.current_user.is_authenticated:
                user_id = get_user_by_username(flask_security.current_user.username).user_id
                address = get_shipping_address_by_user(user_id)
                return render_template("checkout.html", products=products, address=address, form=form)

            return render_template("checkout.html", products=products, form=form)

        else:
            return redirect(url_for('main.view_cart'))

    if request.method == 'POST':
        form = CheckoutForm(request.form)

        if form.validate_on_submit():
            first_name = form.fname.data
            last_name = form.lname.data
            email = form.email.data
            address = form.address.data
            city = form.city.data
            country = form.country.data
            state = form.state.data
            zip = form.zip.data

            address_check = None

            if not flask_security.current_user.is_authenticated or (
                    flask_security.current_user.is_authenticated and not form.save_info.data):
                user_id = None
            else:
                user_id = get_user_by_username(flask_security.current_user.username).user_id
                address_check = get_shipping_address_by_user(user_id)

            if address_check is not None:
                update_shipping_address(first_name, last_name, address, city, state, zip, email, country,
                                        user_id)
            else:
                post_shipping_address(first_name, last_name, address, city, state, zip, email, country,
                                      user_id)

            address_id = get_shipping_address(first_name, last_name, address, city, state, zip, email, country,
                                              user_id).address_id

            total_amount = sum([float(get_product(product).price) for product in session['cart']])
            consoles_id = [product for product in session['cart']]

            if flask_security.current_user.is_authenticated:
                user_id = get_user_by_username(flask_security.current_user.username).user_id

            order_id = post_order(address_id, user_id, total_amount)

            for console_id in consoles_id:
                post_order_consoles(order_id, console_id)
                session['cart'].remove(console_id)
                session.modified = True

            flash('Successfully ordered products.', 'success')
            return redirect(url_for('main.home'))

        # If the form is not valid, re-render the checkout page with the form and error messages
    products = [get_product(product) for product in session['cart']]
    return render_template("checkout.html", products=products, form=form)


@main_bp.route('/p/<id>')
def product_page(id):
    product_info = get_product(id)
    products = get_products()
    selected_products = random.sample(products, 4)
    return render_template("product.html", product=product_info, products=selected_products)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@main_bp.route('/logout')
def logout():
    return redirect(url_for('main.home'))


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@main_bp.route('/change', methods=['GET', 'POST'])
@login_required
def change_password():
    return render_template('change_password.html')
