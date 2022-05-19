import sqlite3
import pytest
import os
from app4test import create_app
from databaseInit import create_db
from flask import url_for, request, get_flashed_messages

#to run the test:
#coverage run -m pytest


@pytest.fixture(scope="session", autouse=True)
def create_test_database(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("tmp")
    database_filename = tmp_dir / "test_database.db"
    create_db(database_filename)
    os.environ['DATABASE_FILENAME'] = str(database_filename)

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(__name__,test=True)
    flask_app.secret_key = 'secret123'
    flask_app.config.update({"TESTING":True,})
    testing_client = flask_app.test_client(use_cookies=False)
    context = flask_app.app_context()
    context.push()
    yield testing_client
    context.pop()

def test_index(test_client):
    # Given
    expected_status_code = 200
    expected_page_title = b"<h1>Welcome To App4Test</h1>"
    # When
    response = test_client.get('/')
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_title in response.data

def test_register_get(test_client):
    # Given
    expected_status_code = 200
    expected_page_title = b"<h1>Register</h1>"
    # When
    response = test_client.get('/register')
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_title in response.data

def test_register_post(test_client):
    # Given
    expected_status_code = 302
    expected_page_url = b"/login"
    # When
    response = test_client.post('/register',data={
                                        "username":"super",
                                        "password":"mario",
                                        "confirm":"mario"
                                            } )
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_url in response.data


def test_login_get(test_client):
    # Given
    expected_status_code = 200
    expected_page_title = b"<h1>Login</h1>"
    # When
    response = test_client.get('/login',follow_redirects=True)
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_title in response.data

def test_login_post_success(test_client):
    # Given
    expected_status_code = 302
    expected_page_url = b"/productapp"
    # When
    response = test_client.post('/login', data={
                                        "username":"melek",
                                        "password":"elloumi"
                                            })
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_url in response.data

def test_login_post_failure(test_client):
    # Given
    expected_status_code = 200
    expected_page_title = b"<h1>Login</h1>"
    # When
    response = test_client.post('/login', data={
                                        "username":"elloumi",
                                        "password":"melek"
                                            })
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_title in response.data

def test_logout_get(test_client):
    # Given
    expected_status_code = 302
    expected_page_url = b"/login"
    # When
    response = test_client.get('/logout')
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_url in response.data

