from flask import Flask, render_template, flash, redirect, url_for, session, request
import sqlite3
from wtforms import Form, StringField, FloatField, IntegerField, PasswordField, validators
from functools import wraps

from loginModule import verifyUser,addUser
import productModule
from databaseInit import create_db
from Product import Product


def create_app(name):
    app = Flask(name)
    db_connection = sqlite3.connect('database.db', check_same_thread=False)
    app.config.from_mapping(
        DATABASE_CON=db_connection
    )

    # Index
    @app.route('/')
    def index():
        return render_template('home.html')

    # Register Form Class
    class RegisterForm(Form):
        username = StringField('Username', [validators.Length(min=4, max=25)])
        password = PasswordField('Password', [
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords do not match')
        ])
        confirm = PasswordField('Confirm Password')

    # User Register
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            username = form.username.data
            password = str(form.password.data)

            addUser(username,password)

            flash('Registered successfully', 'success')

            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    # User login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # Get Form Fields
            username = request.form['username']
            password = request.form['password']

            result,error=verifyUser(username,password)

            if result:
                session['logged_in'] = True
                session['username'] = username

                flash('Logged in successfully', 'success')
                return redirect(url_for('productapp'))
            else:
                return render_template('login.html', error=error)
        return render_template('login.html')

    def is_logged_in(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:
                return f(*args, **kwargs)
            else:
                flash('Unauthorized, Please login', 'danger')
                return redirect(url_for('login'))

        return wrap

    # Logout
    @app.route('/logout')
    @is_logged_in
    def logout():
        session.clear()
        flash('Logged out successfully', 'success')
        return redirect(url_for('index'))

    # ProductApp
    @app.route('/productapp')
    @app.route('/productapp/<float:average>')
    @is_logged_in
    def productapp(average=None):
        products = productModule.fetch_all()
        if len(products) > 0:
            if average==None:
                return render_template('productapp.html', products=products)
            else:
                return render_template('productapp.html', products=products,average=average)
        else:
            msg = 'No products Found'
            return render_template('productapp.html', msg=msg)


    # Product Form Class
    class ProductForm(Form):
        name = StringField('Name', [validators.Length(min=1, max=200)])
        price = FloatField('Price')
        quantity = IntegerField('Quantity')

    # Add Product
    @app.route('/add_product', methods=['GET', 'POST'])
    @is_logged_in
    def add_product():
        form = ProductForm(request.form)
        if request.method == 'POST' and form.validate():
            name = form.name.data
            price = form.price.data
            quantity = form.quantity.data
            product=Product(0,name,price,quantity)

            productModule.add_product(product)

            flash('Product Created', 'success')

            return redirect(url_for('productapp'))

        return render_template('add_product.html', form=form)

    # Edit Article
    @app.route('/edit_product/<string:id>', methods=['GET', 'POST'])
    @is_logged_in
    def edit_product(id):
        # Create cursor
        product = productModule.fetch_by_id(id)
        # Get form
        form = ProductForm(request.form)

        # Populate article form fields
        form.name.data = product[1]
        form.price.data = product[2]
        form.quantity.data = product[3]

        if request.method == 'POST' and form.validate():
            name = request.form['name']
            price = request.form['price']
            quantity = request.form['quantity']

            product_up = Product(id, name, price, quantity)

            productModule.update_product(product_up)

            flash('Product updated successfully', 'success')

            return redirect(url_for('productapp'))

        return render_template('edit_product.html', form=form)

    # Delete Article
    @app.route('/delete_product/<string:id>', methods=['POST'])
    @is_logged_in
    def delete_product(id):

        productModule.delete_product(id)

        flash('Product Deleted', 'success')

        return redirect(url_for('productapp'))

    # Average Product
    @app.route('/average_product')
    @is_logged_in
    def average_product():
        average=productModule.price_average()
        return redirect(url_for('productapp',average=average))

    # Buy Product
    @app.route('/buy_product/<string:id>', methods=['POST'])
    @is_logged_in
    def buy_product(id):
        bought = productModule.buy_product(id)
        if bought:
            flash('Product bought successfully', 'success')
            return redirect(url_for('productapp'))
        else:
            return render_template('productapp.html', error="Product Stock depleted")



    return app


# print("-------App4Test-------")
# username,password=loginMenu()
# productMenu()
# print("App4Test done, goodbye ^_^")


if __name__ == '__main__':
    #create_db('database.db')
    app = create_app(__name__)
    app.secret_key = 'secret123'
    app.run()
