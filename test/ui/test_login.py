import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

API_URL = "http://anirec.ddns.net"
username = "testuser_internal"
password = "Secure!123Password"


class TestLoginPage(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def test_title(self):
        # Test to check if the title of the login page is correct
        self.driver.get(f'{API_URL}/signin')
        self.assertIn('Welcome to AniRec!', self.driver.title)

    def test_form_inputs(self):
        # Test to ensure username and password inputs are correctly labeled and exist
        self.driver.get(f'{API_URL}/signin')
        username_input = self.driver.find_element(By.ID, "form2Example1")
        password_input = self.driver.find_element(By.ID, "form2Example2")

        # Check for input existence and proper labeling
        self.assertEqual(username_input.get_attribute('name'), 'username')
        self.assertEqual(password_input.get_attribute('name'), 'password')

        # Labels
        username_label = self.driver.find_element(By.XPATH, "//label[@for='form2Example1']")
        password_label = self.driver.find_element(By.XPATH, "//label[@for='form2Example2']")

        self.assertEqual(username_label.text, 'Username')
        self.assertEqual(password_label.text, 'Password')

    def test_login_action(self):
        # Test to simulate login action
        self.driver.get(f'{API_URL}/signin')
        self.driver.find_element(By.ID, "form2Example1").send_keys("testuser")
        self.driver.find_element(By.ID, "form2Example2").send_keys("password")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Redirect and login response handling could be tested here, depending on the setup

    def tearDown(self):
        # close the browser window
        self.driver.close()
