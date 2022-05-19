import pytest
import os
from app4test import create_app
from databaseInit import create_db

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
    testing_client = flask_app.test_client(use_cookies=True)
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
    expected_status_code = 200
    expected_page_alert = b"Registered successfully"
    data_to_register={
                                        "username":"super",
                                        "password":"mario",
                                        "confirm":"mario"
                    }
    # When
    response = test_client.post('/register',data=data_to_register,follow_redirects=True )
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data


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
    expected_status_code = 200
    expected_page_alert = b"Logged in successfully"
    data_to_login={
                                        "username":"melek",
                                        "password":"elloumi"
                }
    # When
    response = test_client.post('/login', data=data_to_login,follow_redirects=True)
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data

def test_login_post_failure_user(test_client):
    # Given
    expected_status_code = 200
    expected_page_alert = b"User not registered in database"
    data_to_login ={
                                        "username":"elloumi",
                                        "password":"melek"
                                            }
    # When
    response = test_client.post('/login', data=data_to_login)
    print(response.data)
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data

def test_login_post_failure_password(test_client):
    # Given
    expected_status_code = 200
    expected_page_alert = b"Wrong password"
    data_to_login = {
                                        "username":"melek",
                                        "password":"melek"
                    }
    # When
    response = test_client.post('/login', data=data_to_login)
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data

def test_logout_get(test_client):
    # Given
    expected_status_code = 200
    expected_page_alert = b'Logged out successfully'
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    # When
    response = test_client.get('/logout',follow_redirects=True)
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data

def test_productapp_success(test_client):
    # Given
    expected_status_code = 200
    expected_page_title = b'<h1>ProductApp'
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    # When
    response = test_client.get('/productapp')
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_title in response.data

def test_productapp_average(test_client):
    # Given
    expected_status_code = 200
    expected_page_element = b'Average: 6.375'
    average_data=6.375
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    # When
    response = test_client.get(f'/productapp/{average_data}')
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_element in response.data

def test_productapp_failure(test_client):
    # Given
    expected_status_code = 200
    expected_page_alert = b'No products Found'
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    test_client.post('/delete_product/1')
    test_client.post('/delete_product/2')
    test_client.post('/delete_product/3')
    test_client.post('/delete_product/4')
    # When
    response = test_client.get('/productapp')
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data

def test_unautherized(test_client):
    # Given
    expected_status_code = 200
    expected_page_alert = b"Unauthorized, Please login"
    with test_client.session_transaction() as session:
        del session['logged_in']
    # When
    response = test_client.get('/productapp',follow_redirects=True)
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data

def test_addproduct_get(test_client):
    # Given
    expected_status_code = 200
    expected_page_title = b"<h1>Add Product</h1>"
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    # When
    response = test_client.get('/add_product')
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_title in response.data

def test_addproduct_post(test_client):
    # Given
    expected_status_code = 200
    expected_page_alert = b"Product Created"
    expected_product_name = b"TEST"
    expected_product_price = b"1337"
    data_to_add={
                                        "name":"TEST",
                                        "price":"1337",
                                        "quantity":"69"
                                            }
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    # When
    response = test_client.post('/add_product',data=data_to_add,follow_redirects=True )
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data
    assert expected_product_name in response.data
    assert expected_product_price in response.data

def test_updateproduct_get(test_client):
    # Given
    expected_status_code = 200
    expected_page_title = b"<h1>Edit Product</h1>"
    id_to_update=1
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    # When
    response = test_client.get(f'/edit_product/{id_to_update}')
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_title in response.data

def test_updateproduct_post(test_client):
    # Given
    expected_status_code = 200
    expected_page_alert = b"Product updated successfully"
    expected_product_name = b"RULE"
    expected_product_price = b"34"
    id_to_update=1
    data_to_update = {
        "name":"RULE",
        "price":"34",
        "quantity":"5"
    }
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    # When
    response = test_client.post(f'/edit_product/{id_to_update}',data=data_to_update,follow_redirects=True )
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data
    assert expected_product_name in response.data
    assert expected_product_price in response.data

def test_deleteproduct_post(test_client):
    # Given
    expected_status_code = 200
    expected_page_alert = b"Product Deleted"
    expected_product_name = b"RULE"
    id_to_delete = 1
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    # When
    response = test_client.post(f'/delete_product/{id_to_delete}',follow_redirects=True )
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data
    assert expected_product_name not in response.data

def test_averageproduct_get(test_client):
    # Given
    expected_status_code = 200
    expected_page_element = b'Average: 5.2'
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    test_client.post('/add_product', data={
        "name": "Pen",
        "price": "5.2",
        "quantity": "1"
    }, follow_redirects=True)
    # When
    response = test_client.get('/average_product',follow_redirects=True)
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_element in response.data

def test_buyproduct_post_success(test_client):
    # Given
    expected_status_code = 200
    expected_page_alert = b"Product bought successfully"
    id_to_buy = 1
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    # When
    response = test_client.post(f'/buy_product/{id_to_buy}',follow_redirects=True )
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data

def test_buyproduct_post_failure(test_client):
    # Given
    expected_status_code = 200
    expected_page_alert = b"Product Stock depleted"
    id_to_buy = 1
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "melek"
    # When
    response = test_client.post(f'/buy_product/{id_to_buy}',follow_redirects=True )
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_alert in response.data