from unittest import TestCase
from unittest.mock import patch
from productModule import average
from productModule import price_average
from productModule import fetch_by_name
from loginModule import verifyUser
from Product import Product

#to run the test:
#Python -m unittest UnitTest\test_app4test.py


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
        product1=Product(1,'Test1',1.0,1)
        product2=Product(2,'Test2',3.0,1)
        mocked_object.return_value = [product1,product2]
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

class TestVerifyUser(TestCase):
    def test_verifyUser_exists(self):
        #Given
        username='melek'
        password='elloumi'
        expected_result=True
        #When
        result = verifyUser(username,password)
        #Then
        self.assertEqual(expected_result,result)

    def test_verifyUser_unregistered(self):
        #Given
        username='wassime'
        password='kallel'
        expected_result=False
        #When
        result = verifyUser(username,password)
        #Then
        self.assertEqual(expected_result,result)

    def test_verifyUser_wrongPassword(self):
        #Given
        username='melek'
        password='kallel'
        expected_result=False
        #When
        result = verifyUser(username,password)
        #Then
        self.assertEqual(expected_result,result)

class TestFetchByName(TestCase):
    @patch("productModule.sqlite3")
    def test_fetchByName_exists(self, mocked_object):
        # Given
        mocked_object.connect().execute().fetchone.return_value = [1,'CD',4.5,5]
        expected_bool = True
        expected_product = Product(1,'CD',4.5,5)
        # When
        result_bool, result_product = fetch_by_name('CD')
        # Then
        self.assertEqual(expected_bool, result_bool)
        self.assertEqual(expected_product, result_product)

    @patch("productModule.sqlite3")
    def test_fetchByName_unexistant(self, mocked_object):
        # Given
        mocked_object.connect().execute().fetchone.return_value = None
        expected_bool = False
        expected_product = None
        # When
        result_bool, result_product = fetch_by_name('Testing')
        # Then
        self.assertEqual(expected_bool, result_bool)
        self.assertEqual(expected_product, result_product)



