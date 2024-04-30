import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

API_URL = "http://anirec.ddns.net"
username = "testuser_internal"
password = "Secure!123Password"


class TestSignupPage(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

        self.driver.implicitly_wait(15)

    def test_title(self):
        self.driver.get(f'{API_URL}/signup')

        # Check if the page title is correct
        self.assertIn('New user', self.driver.title)

    def test_username_password_inputs(self):
        self.driver.get(f'{API_URL}/signup')

        # Check for existence and proper labeling of username and password inputs
        username_input = self.driver.find_element(By.ID, "form2Example1")
        password_input = self.driver.find_element(By.ID, "form2Example2")

        # Input 'name' attributes should match expected names
        self.assertEqual(username_input.get_attribute('name'), 'username')
        self.assertEqual(password_input.get_attribute('name'), 'password')

        # Input labeling
        username_label = self.driver.find_element(By.XPATH, "//label[@for='form2Example1']")
        password_label = self.driver.find_element(By.XPATH, "//label[@for='form2Example2']")

        self.assertEqual(username_label.text, 'Username')
        self.assertEqual(password_label.text, 'Password')

    def test_signup_action(self):
        self.driver.get(f'{API_URL}/signup')

        # Simulate user input and submit action for the signup form
        self.driver.find_element(By.ID, "form2Example1").send_keys("new_user")
        self.driver.find_element(By.ID, "form2Example2").send_keys("new_password123")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    def tearDown(self):
        # Close the browser window on test completion
        self.driver.close()
