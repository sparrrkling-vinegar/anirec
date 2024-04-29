import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


class TestInternalPage(unittest.TestCase):
    def setUp(self):
        # Set up Firefox WebDriver
        self.driver = webdriver.Firefox()
        self.driver.get('http://localhost:8080/internal')

    def test_page_title(self):
        # Confirm that the internal page title is correct
        self.assertIn('Internal Page', self.driver.title)

    def test_welcome_message(self):
        # Ensure that the welcome message is displayed correctly
        welcome_message = self.driver.find_element(
            By.XPATH,
            "//h2[contains(text(),"
            " 'Welcome to Internal Page!')]"
        )
        self.assertTrue(welcome_message.is_displayed())

    def test_navigation_links(self):
        # Check that navigation links (from the base template) are present and correctly linked
        links = {
            "Search": "/search_page",
            "Generate": "/recommendation",
            "Home": "/internal",
            "Logout": "/logout",
            "Account Details": "/account"
        }

        for link_text, url_extension in links.items():
            link = self.driver.find_element(By.LINK_TEXT, link_text)
            self.assertIn(url_extension, link.get_attribute('href'))

    def tearDown(self):
        # Close browser window
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
