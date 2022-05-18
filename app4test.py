from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
import sqlite3
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

from loginModule import verifyUser,addUser
from productModule import productMenu
from databaseInit import create_db


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
    @is_logged_in
    def productapp():
        return render_template('productapp.html')

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
