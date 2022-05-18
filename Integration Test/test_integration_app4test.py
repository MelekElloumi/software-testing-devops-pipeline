import sqlite3
import pytest
import os
from app4test import create_app
from databaseInit import create_db


#to run the test:
#coverage run -m unittest UnitTest\test_integration_app4test.py


@pytest.fixture(scope="session", autouse=True)
def create_test_database(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("tmp")
    database_filename = tmp_dir / "test_database.db"
    create_db(database_filename)

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(__name__,test=True)
    flask_app.secret_key = 'secret123'
    testing_client = flask_app.test_client(use_cookies=False)
    context = flask_app.app_context()
    context.push()
    yield testing_client
    context.pop()

# def test_register_user(test_client):
#     # Given
#     request_payload = {
#         "username": "foulen",
#         "fullname": "Foulen Ben Foulen"
#     }
#
#     expected_body = {
#         "username": "foulen",
#         "full_name": "Foulen Ben Foulen"
#     }
#     expected_status_code = 200
#
#     expected_body_keys = ["user_id", "username", "full_name"]
#
#     # When
#     response = test_client.post('/users', json=request_payload)
#
#     # Then
#     assert expected_status_code == response.status_code
#     assert response.json | expected_body == response.json
#     assert set(expected_body_keys) == response.json.keys()
#     assert int == type(response.json["user_id"])

def test_login_user(test_client):
    # Given
    expected_status_code = 200
    # When
    response = test_client.get('/login')
    # Then
    assert expected_status_code == response.status_code
    assert b"<h1>Login</h1>" in response.data


