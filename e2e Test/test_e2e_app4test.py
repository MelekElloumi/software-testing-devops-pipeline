from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3
import time
from app4test import main
import multiprocessing
import os

#to run the test:
#coverage run -m unittest "e2e Test\test_e2e_app4test.py"

def deleteUser():
    database_filename = 'database.db'
    connection = sqlite3.connect(database_filename)
    connection.execute(
        "DELETE FROM USER WHERE USERNAME LIKE ?;", ("selenium",))
    connection.commit()
    connection.close()

class TestApp4Test(TestCase):

    @classmethod
    def setUpClass(inst):
        inst.app4test_process=multiprocessing.Process(target=main,name="App4Test",args=('test_database.db',True,))
        inst.app4test_process.start()
        time.sleep(1)
        inst.start = time.time()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-gpu')
        #inst.driver = webdriver.Chrome('chromedriver.exe')
        inst.driver = webdriver.Chrome(options = chrome_options)

        #inst.driver.implicitly_wait(1)
        print("Visiting home page")
        inst.driver.get('http://localhost:5000/')
        inst.driver.save_screenshot('./e2e Test/Screenshots/01_homepage.png')

    def test_01_register(self):
        print("Visiting register page")
        register_button = self.driver.find_element(by=By.ID, value='Register')
        register_button.click()

        print("Filling register form")
        username_field = self.driver.find_element(by=By.ID, value='username')
        username_field.send_keys('selenium')
        password_field = self.driver.find_element(by=By.ID, value='password')
        password_field.send_keys('driver')
        confirm_field = self.driver.find_element(by=By.ID, value='confirm')
        confirm_field.send_keys('driver')
        self.driver.save_screenshot('./e2e Test/Screenshots/02_registerpage.png')

        print("Submitting register form")
        register_button = self.driver.find_element(by=By.ID, value='Submit')
        register_button.click()

        print("Redirecting to login page")
        message = self.driver.find_element(by=By.ID, value='message0').text
        expected_message = "Registered successfully"

        self.assertIn(expected_message, message)

    def test_02_login_success(self):
        print("Filling login form")
        username_field = self.driver.find_element(by=By.NAME, value='username')
        username_field.send_keys('selenium')
        password_field = self.driver.find_element(by=By.NAME, value='password')
        password_field.send_keys('driver')
        self.driver.save_screenshot('./e2e Test/Screenshots/03_loginpage.png')

        print("Submitting login form")
        register_button = self.driver.find_element(by=By.ID, value='Submit')
        register_button.click()

        print("Redirecting to productapp page")
        message = self.driver.find_element(by=By.ID, value='message0').text
        expected_message = "Logged in successfully"

        self.assertIn(expected_message, message)

    def test_03_productapp(self):
        print("Checking productapp page elements")
        self.driver.save_screenshot('./e2e Test/Screenshots/04_productapppage_beforeadd.png')
        table_id = self.driver.find_element(by=By.ID, value='maintable')
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        col = rows[1].find_elements(By.TAG_NAME, "td")
        cd_data={
            "id":col[0].text,
            "name": col[1].text,
            "price": col[2].text,
            "quantity": col[3].text
        }
        expected_cd_data = {
            "id": "1",
            "name": "CD",
            "price": "2.0",
            "quantity": "5"
        }

        self.assertEqual(expected_cd_data,cd_data)

    def test_04_addproduct(self):
        print("Visiting add product page")
        addproduct_button = self.driver.find_element(by=By.ID, value='addproduct')
        addproduct_button.click()

        print("Filling add product form")
        name_field = self.driver.find_element(by=By.ID, value='name')
        name_field.send_keys('server')
        price_field = self.driver.find_element(by=By.ID, value='price')
        price_field.send_keys('42.0')
        quantity_field = self.driver.find_element(by=By.ID, value='quantity')
        quantity_field.send_keys('2')
        self.driver.save_screenshot('./e2e Test/Screenshots/05_addproductpage.png')

        print("Submitting add product form")
        addproduct_button = self.driver.find_element(by=By.ID, value='Submit')
        addproduct_button.click()

        print("Redirecting to productapp page")
        message = self.driver.find_element(by=By.ID, value='message0').text
        expected_message = "Product Created"
        self.driver.save_screenshot('./e2e Test/Screenshots/06_productapppage_afteradd.png')

        table_id = self.driver.find_element(by=By.ID, value='maintable')
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        col = rows[5].find_elements(By.TAG_NAME, "td")
        server_data = {
            "id": col[0].text,
            "name": col[1].text,
            "price": col[2].text,
            "quantity": col[3].text
        }
        expected_server_data = {
            "id": "5",
            "name": "server",
            "price": "42.0",
            "quantity": "2"
        }

        self.assertIn(expected_message, message)
        self.assertEqual(expected_server_data, server_data)

    def test_05_editproduct(self):
        print("Visiting edit page for the product 'server'")
        editproduct_button = self.driver.find_element(by=By.ID, value='editproduct5')
        editproduct_button.click()

        print("Filling edit product form")
        price_field = self.driver.find_element(by=By.ID, value='price')
        price_field.clear()
        price_field.send_keys('20.0')
        self.driver.save_screenshot('./e2e Test/Screenshots/07_editproductpage.png')

        print("Submitting add product form")
        editproduct_button = self.driver.find_element(by=By.ID, value='Submit')
        editproduct_button.click()

        print("Redirecting to productapp page")
        message = self.driver.find_element(by=By.ID, value='message0').text
        expected_message = "Product updated successfully"
        self.driver.save_screenshot('./e2e Test/Screenshots/08_productapppage_afteredit.png')

        table_id = self.driver.find_element(by=By.ID, value='maintable')
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        col = rows[5].find_elements(By.TAG_NAME, "td")
        server_price = col[2].text
        expected_server_price = "20.0"

        self.assertIn(expected_message, message)
        self.assertEqual(expected_server_price, server_price)

    def test_06_buyproduct(self):
        print("Buying the product 'server'")
        buyproduct_button = self.driver.find_element(by=By.ID, value='buyproduct5')
        buyproduct_button.click()

        print("Redirecting to productapp page")
        message = self.driver.find_element(by=By.ID, value='message0').text
        expected_message = "Product bought successfully"
        self.driver.save_screenshot('./e2e Test/Screenshots/09_productapppage_afterbuy.png')

        table_id = self.driver.find_element(by=By.ID, value='maintable')
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        col = rows[5].find_elements(By.TAG_NAME, "td")
        server_price = col[3].text
        expected_server_price = "1"

        self.assertIn(expected_message, message)
        self.assertEqual(expected_server_price, server_price)

    def test_07_deleteproduct(self):
        print("Deleting the product 'server'")
        deleteproduct_button = self.driver.find_element(by=By.ID, value='deleteproduct5')
        deleteproduct_button.click()

        print("Redirecting to productapp page")
        message = self.driver.find_element(by=By.ID, value='message0').text
        expected_message = "Product Deleted"
        self.driver.save_screenshot('./e2e Test/Screenshots/10_productapppage_afterdelete.png')

        table_id = self.driver.find_element(by=By.ID, value='maintable')
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        rows_number=len(rows)
        expected_rows_number = 5

        self.assertIn(expected_message, message)
        self.assertEqual(expected_rows_number, rows_number)

    def test_08_averageprice(self):
        print("Checking the average price")
        averageprice_button = self.driver.find_element(by=By.ID, value='averageproduct')
        averageprice_button.click()

        print("Redirecting to productapp page")
        self.driver.save_screenshot('./e2e Test/Screenshots/11_productapppage_afteraverage.png')

        average_price = self.driver.find_element(by=By.ID, value='average').text
        expected_average_price = "Average: 4.125"

        self.assertEqual(expected_average_price, average_price)

    def test_09_logout(self):
        print("Logging out")
        logout_button = self.driver.find_element(by=By.ID, value='Logout')
        logout_button.click()

        print("Redirecting to productapp page")
        message = self.driver.find_element(by=By.ID, value='message0').text
        expected_message = "Logged out successfully"
        self.driver.save_screenshot('./e2e Test/Screenshots/12_loggedout.png')

        self.assertIn(expected_message, message)

    def test_10_login_failure(self):
        print("Visiting login page")
        register_button = self.driver.find_element(by=By.ID, value='Login')
        register_button.click()

        print("Filling login form")
        username_field = self.driver.find_element(by=By.NAME, value='username')
        username_field.send_keys('wrong')
        password_field = self.driver.find_element(by=By.NAME, value='password')
        password_field.send_keys('wrong')

        print("Submitting login form")
        register_button = self.driver.find_element(by=By.ID, value='Submit')
        register_button.click()

        print("Redirecting to login page")
        message = self.driver.find_element(by=By.ID, value='error').text
        expected_message = "User not registered in database"
        self.driver.save_screenshot('./e2e Test/Screenshots/13_loginfailed.png')

        self.assertIn(expected_message, message)

    @classmethod
    def tearDownClass(inst):
        inst.end = time.time()
        elapsedtime=inst.end-inst.start
        print("\n-------\nE2E test duration: ", "{:.2f}".format(elapsedtime), "seconds")
        inst.driver.quit()
        deleteUser()
        inst.app4test_process.terminate()
        os.remove('test_database.db')




