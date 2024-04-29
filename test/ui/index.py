import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By

ENDPOINT = "http://localhost:8000"

class TestHomePage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_home_page_loaded(self):
        self.driver.get(ENDPOINT)
        self.assertIn('Index Page', self.driver.title)

    def test_home_page_navigation(self):
        self.driver.get(ENDPOINT)
        home_link = self.driver.find_element(By.LINK_TEXT, 'Home')
        self.assertEqual(home_link.get_attribute('href'), f'{ENDPOINT}/')

    def test_login_link(self):
        self.driver.get(ENDPOINT)
        login_link = self.driver.find_element(By.LINK_TEXT, 'Login')
        self.assertEqual(login_link.get_attribute('href'), f'{ENDPOINT}/signin')

    def test_signup_link(self):
        self.driver.get(ENDPOINT)
        signup_link = self.driver.find_element(By.LINK_TEXT, 'Sign Up')
        self.assertEqual(signup_link.get_attribute('href'), f'{ENDPOINT}/signup')

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
