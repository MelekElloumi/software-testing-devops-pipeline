import sqlite3
from unittest import TestCase
from unittest.mock import patch
from productModule import average, price_average, fetch_by_id,fetch_all,add_product,update_product,delete_product,buy_product
from loginModule import verifyUser, addUser
import os

#to run the test:
#coverage run -m unittest UnitTest\test_unit_app4test.py
os.environ['DATABASE_FILENAME'] = 'database.db'

class TestAddUser(TestCase):
    @patch("loginModule.sqlite3", spec=sqlite3)
    def test_addUser(self, mocked_object):
        # Given
        mock_execute= (mocked_object.connect.return_value.cursor.return_value.execute)
        # When
        addUser('test', 'test')
        # Then
        mock_execute.assert_called_once()

class TestVerifyUser(TestCase):
    def test_verifyUser_exists(self):
        #Given
        username='melek'
        password='elloumi'
        expected_result=True
        #When
        result,msg = verifyUser(username,password)
        #Then
        self.assertEqual(expected_result,result)

    def test_verifyUser_unregistered(self):
        #Given
        username='wassime'
        password='kallel'
        expected_result=False
        #When
        result,msg = verifyUser(username,password)
        #Then
        self.assertEqual(expected_result,result)

    def test_verifyUser_wrongPassword(self):
        #Given
        username='melek'
        password='kallel'
        expected_result=False
        #When
        result,msg = verifyUser(username,password)
        #Then
        self.assertEqual(expected_result,result)

class TestFetchById(TestCase):
    @patch("productModule.sqlite3")
    def test_fetchById_exists(self, mocked_object):
        # Given
        mocked_object.connect().cursor().execute().fetchone.return_value = (1,'CD',4.5,5)
        expected_product = (1,'CD',4.5,5)
        # When
        result_product = fetch_by_id(1)
        # Then
        self.assertEqual(expected_product, result_product)

    @patch("productModule.sqlite3")
    def test_fetchById_unexistant(self, mocked_object):
        # Given
        mocked_object.connect().cursor().execute().fetchone.return_value = None
        expected_product = None
        # When
        result_product = fetch_by_id(1)
        # Then
        self.assertEqual(expected_product, result_product)

class TestFetchAll(TestCase):
    @patch("productModule.sqlite3")
    def test_fetchAll_exists(self, mocked_object):
        # Given
        mocked_object.connect().cursor().execute().fetchall.return_value = [(1,'CD',4.5,5),(2,'DVD',2,1)]
        expected_product = [(1,'CD',4.5,5),(2,'DVD',2,1)]
        # When
        result_product = fetch_all()
        # Then
        self.assertEqual(expected_product, result_product)

    @patch("productModule.sqlite3")
    def test_fetchAll_unexistant(self, mocked_object):
        # Given
        mocked_object.connect().cursor().execute().fetchall.return_value = None
        expected_product = None
        # When
        result_product = fetch_all()
        # Then
        self.assertEqual(expected_product, result_product)

class TestAverage(TestCase):
    def test_average_notempty(self):
        # Given
        list = [3,2,1,10]
        expected_result = 4.0
        # When
        result = average(list)
        # Then
        self.assertEqual(expected_result, result)

    def test_average_emptylist(self):
        # Given
        list = []
        # Then
        self.assertRaises(ValueError, average, list)

class TestPriceAverage(TestCase):
    @patch("productModule.fetch_all")
    def test_priceAverage_notempty(self, mocked_object):
        # Given
        mocked_object.return_value = [(1, 'Test1', 1.0, 1), (2, 'Test2', 3.0, 1)]
        expected_result = 2.0
        # When
        result = price_average()
        # Then
        self.assertEqual(expected_result, result)

    @patch("productModule.fetch_all")
    def test_priceAverage_emptylist(self, mocked_object):
        # Given
        mocked_object.return_value = []
        # Then
        self.assertRaises(ValueError, price_average)

class TestAddProduct(TestCase):
    @patch("productModule.sqlite3", spec=sqlite3)
    def test_addProduct(self, mocked_object):
        # Given
        mock_execute=(mocked_object.connect.return_value.execute)
        # When
        add_product('test', 0,0)
        # Then
        mock_execute.assert_called_once()

class TestUpdateProduct(TestCase):
    @patch("productModule.sqlite3", spec=sqlite3)
    def test_updateProduct(self, mocked_object):
        # Given
        mock_execute=(mocked_object.connect.return_value.execute)
        # When
        update_product(0,'test', 0,0)
        # Then
        mock_execute.assert_called_once()

class TestDeleteProduct(TestCase):
    @patch("productModule.sqlite3", spec=sqlite3)
    def test_deleteProduct(self, mocked_object):
        # Given
        mock_execute=(mocked_object.connect.return_value.execute)
        # When
        delete_product(0)
        # Then
        mock_execute.assert_called_once()

class TestBuyProduct(TestCase):
    @patch("productModule.sqlite3")
    def test_buyProduct_exists(self, mocked_object):
        # Given
        mocked_object.connect().cursor().rowcount = 1
        expected_result=True
        # When
        result=buy_product(0)
        # Then
        self.assertEqual(expected_result, result)

    @patch("productModule.sqlite3")
    def test_buyProduct_unexistant(self, mocked_object):
        # Given
        mocked_object.connect().cursor().rowcount = 0
        expected_result = False
        # When
        result = buy_product(0)
        # Then
        self.assertEqual(expected_result, result)


