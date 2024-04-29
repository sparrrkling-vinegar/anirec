import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

API_URL = "http://anirec.ddns.net"
username = "testuser_internal"
password = "Secure!123Password"

class TestHomePage(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def test_home_page_loaded(self):
        self.driver.get(API_URL)
        self.assertIn('Index Page', self.driver.title)

    def test_home_page_navigation(self):
        self.driver.get(API_URL)
        home_link = self.driver.find_element(By.LINK_TEXT, 'Home')
        self.assertEqual(home_link.get_attribute('href'), f'{API_URL}/')

    def test_login_link(self):
        self.driver.get(API_URL)
        login_link = self.driver.find_element(By.LINK_TEXT, 'Login')
        self.assertEqual(login_link.get_attribute('href'), f'{API_URL}/signin')

    def test_signup_link(self):
        self.driver.get(API_URL)
        signup_link = self.driver.find_element(By.LINK_TEXT, 'Sign Up')
        self.assertEqual(signup_link.get_attribute('href'), f'{API_URL}/signup')

    def tearDown(self):
        self.driver.close()
