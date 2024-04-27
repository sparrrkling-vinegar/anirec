import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TestSearchPage(unittest.TestCase):
    def setUp(self):
        # Initialize WebDriver for Firefox
        self.driver = webdriver.Firefox()
        self.driver.get('http://localhost:8080/search_page')

    def test_page_title(self):
        # Confirm that the page title is 'Search Page'
        self.assertIn('Search Page', self.driver.title)

    def test_search_functionality(self):
        # Ensure that search input and button are present
        search_input = self.driver.find_element(By.ID, "searchInput")
        search_button = self.driver.find_element(By.ID, "searchBtn")

        self.assertTrue(search_input.is_displayed())
        self.assertTrue(search_button.is_displayed())

        # Simulate typing into the search field
        search_input.send_keys("example")

        # Simulate clicking the search button
        search_button.click()

        output_div = self.driver.find_element(By.ID, "output")
        self.assertTrue(output_div.is_displayed())
        # Without a backend to process the post, we're limited to checking the display of the output div here.

    def test_navigation_links(self):
        # Basic tests to ensure that navigation links are correctly set up
        home_link = self.driver.find_element(By.LINK_TEXT, 'Home')
        self.assertEqual(home_link.get_attribute('href'), 'http://localhost:8080/internal')

        account_details_link = self.driver.find_element(By.LINK_TEXT, 'Account Details')
        self.assertEqual(account_details_link.get_attribute('href'), 'http://localhost:8080/account')

    def tearDown(self):
        # Close the browser after tests
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
