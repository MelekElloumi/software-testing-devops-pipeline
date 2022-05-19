import time
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

#to run the test:
#coverage run -m unittest "e2e Test\test_e2e_app4test.py"

class TestApp4Test(TestCase):

    @classmethod
    def setUp(inst):
        inst.driver = webdriver.Chrome('chromedriver.exe')
        #inst.driver.implicitly_wait(1)
        print("Visiting home page")
        inst.driver.maximize_window()
        inst.driver.get('http://localhost:5000/')
        inst.driver.save_screenshot('./e2e Test/Screenshots/homepage.png')

    def test_register(self):
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
        self.driver.save_screenshot('./e2e Test/Screenshots/registerpage.png')

        print("Submitting register form")
        register_button = self.driver.find_element(by=By.ID, value='Submit')
        register_button.click()

        message = self.driver.find_element(by=By.ID, value='message0').text
        expected_message = "Registered successfully"
        self.assertIn(expected_message, message)

    @classmethod
    def tearDownClass(inst):
        inst.driver.quit()



# driver = webdriver.Chrome('../chromedriver.exe')
#
# print("Visiting home page")
# driver.get('http://localhost:5000/')
# driver.maximize_window()
# driver.save_screenshot('./Screenshots/homepage.png')
# #time.sleep(2)
#
#
# driver.quit()
