from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
import sqlite3
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

from loginModule import loginMenu
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

    return app


# print("-------App4Test-------")
# username,password=loginMenu()
# productMenu()
# print("App4Test done, goodbye ^_^")


if __name__ == '__main__':
    create_db('database.db')
    app = create_app(__name__)
    app.run()