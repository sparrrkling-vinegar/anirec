import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ENDPOINT = "http://localhost:8000"


class TestRecommendationPage(unittest.TestCase):
    def setUp(self):
        # Initialize WebDriver for Firefox
        self.driver = webdriver.Firefox()

        self.driver.get(f"{ENDPOINT}/signin")
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

        username_input.send_keys("testuser_internal" + Keys.RETURN)
        password_input.send_keys("Secure!123Password" + Keys.RETURN)
        submit_button.click()

        self.driver.implicitly_wait(3)
        self.driver.get(f"{ENDPOINT}/recommendation")

    def test_page_title(self):
        # Confirm that the web page title is as expected
        self.assertIn("Recommendation Page", self.driver.title)

    def test_generate_button_functionality(self):
        # Verify the presence of the Generate button
        generate_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "generateBtn"))
        )
        self.assertTrue(generate_btn.is_displayed(), "Generate button is not displayed")

        # Click the Generate button
        generate_btn.click()

        # Check that the output container is available and could potentially display results

        # In testing environments, actual data/results are not retrieved, this checks UI responsiveness.
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "output"))
        )

        output_div = self.driver.find_element(By.ID, "output")
        self.assertTrue(output_div.is_displayed(), "Recommendation is not displayed")

    def test_navigation_links(self):
        # Example of testing navigation links for its presence and correct destination href:
        search_link = self.driver.find_element(By.LINK_TEXT, 'Search')
        self.assertIn("/search_page", search_link.get_attribute('href'))

        home_link = self.driver.find_element(By.LINK_TEXT, 'Home')
        self.assertIn("/internal", home_link.get_attribute('href'))

    def tearDown(self):
        # Close the browser after tests
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
