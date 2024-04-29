import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

API_URL = "http://anirec.ddns.net"
username = "testuser_internal"
password = "Secure!123Password"


class TestSearchPage(unittest.TestCase):
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

        self.driver.implicitly_wait(30)
        self.driver.get(f'{API_URL}/search_page')

    def test_page_title(self):
        # Confirm that the page title is 'Search Page'
        self.assertIn('Search Page', self.driver.title)

    def test_search_functionality(self):
        # Ensure that search input and button are present
        search_input = self.driver.find_element(By.ID, "searchInput")
        search_button = self.driver.find_element(By.ID, "searchBtn")

        self.assertTrue(search_input.is_displayed(), "Search input is not displayed")
        self.assertTrue(search_button.is_displayed(), "Search button is not displayed")

        # Simulate typing into the search field
        search_input.send_keys("example")

        # Simulate clicking the search button
        search_button.click()

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "output"))
        )

        output_div = self.driver.find_element(By.ID, "output")  # Find the output div
        self.assertTrue(output_div.is_displayed(), "Output div is not displayed.")

    def test_navigation_links(self):
        # Basic tests to ensure that navigation links are correctly set up
        home_link = self.driver.find_element(By.LINK_TEXT, 'Home')
        self.assertEqual(home_link.get_attribute('href'), f'{API_URL}/internal')

        account_details_link = self.driver.find_element(By.LINK_TEXT, 'Account Details')
        self.assertEqual(account_details_link.get_attribute('href'), f'{API_URL}/account')

    def tearDown(self):
        # Close the browser after tests
        self.driver.close()

