import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

API_URL = "http://anirec.ddns.net"
username = "testuser_internal"
password = "Secure!123Password"


class TestInternalPage(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

        self.driver.get(f"{API_URL}/signin")
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

        username_input.send_keys(username + Keys.RETURN)
        password_input.send_keys(password + Keys.RETURN)
        submit_button.click()

        self.driver.implicitly_wait(15)


    def test_page_title(self):
        # Confirm that the internal page title is correct
        self.driver.get(f'{API_URL}/internal')
        self.assertIn('Internal Page', self.driver.title)

    def test_welcome_message(self):
        # Ensure that the welcome message is displayed correctly
        self.driver.get(f'{API_URL}/internal')

        welcome_message = self.driver.find_element(
            By.XPATH,
            "//h2[contains(text(), 'Welcome to Internal Page!')]"
        )
        self.assertTrue(welcome_message.is_displayed())

    def test_navigation_links(self):
        # Check that navigation links (from the base template) are present and correctly linked
        self.driver.get(f'{API_URL}/internal')

        links = {
            "Search": "/search_page",
            "Home": "/internal",
            "Generate": "/recommendation",
            "Logout": "/logout",
            "Account Details": "/account"
        }

        for link_text, url_extension in links.items():
            link = self.driver.find_element(By.LINK_TEXT, link_text)
            self.assertIn(url_extension, link.get_attribute('href'))

    def tearDown(self):
        # Close browser window
        self.driver.close()
