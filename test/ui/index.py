import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestHomePage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_home_page_loaded(self):
        self.driver.get('http://localhost:8080')
        self.assertIn('Index Page', self.driver.title)

    def test_home_page_navigation(self):
        self.driver.get('http://localhost:8080')
        home_link = self.driver.find_element(By.LINK_TEXT, 'Home')
        self.assertEqual(home_link.get_attribute('href'), 'http://localhost:8080/')

    def test_login_link(self):
        self.driver.get('http://localhost:8080')
        login_link = self.driver.find_element(By.LINK_TEXT, 'Login')
        self.assertEqual(login_link.get_attribute('href'), 'http://localhost:8080/signin')

    def test_signup_link(self):
        self.driver.get('http://localhost:8080')
        signup_link = self.driver.find_element(By.LINK_TEXT, 'Sign Up')
        self.assertEqual(signup_link.get_attribute('href'), 'http://localhost:8080/signup')

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
