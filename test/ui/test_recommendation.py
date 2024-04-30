import unittest
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

API_URL = "http://anirec.ddns.net"
username = "testuser_internal"
password = "Secure!123Password"


def submit_signup_form(api_url, username, password):
    """
    Submit the signup form.
    :param api_url: Base URL of the API
    :param username: Username for signup
    :param password: Password for signup
    """
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(f"{api_url}/signup", data=data)
    if response.status_code == 303:  # Expecting a redirect on success
        return f"Signup successful, redirected to: {response.headers['Location']}"
    else:
        try:
            # Assuming error details are provided in response's HTML or text
            return response.text
        except Exception as e:
            return f"An error occurred: {str(e)}"


submit_signup_form(API_URL, username, password)


class TestRecommendationPage(unittest.TestCase):
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
        self.driver.get(f"{API_URL}/recommendation")

        # Confirm that the web page title is as expected
        self.assertIn("Recommendation Page", self.driver.title)

    def test_generate_button_functionality(self):
        self.driver.get(f"{API_URL}/recommendation")

        # Verify the presence of the Generate button
        generate_btn = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "generateBtn"))
        )
        self.assertTrue(generate_btn.is_displayed(), "Generate button is not displayed")

        # Click the Generate button
        generate_btn.click()

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "output"))
        )

        output_div = self.driver.find_element(By.ID, "output")
        self.assertTrue(output_div.is_displayed(), "Recommendation is not displayed")

    def test_navigation_links(self):
        self.driver.get(f"{API_URL}/recommendation")

        # Example of testing navigation links for its presence and correct destination href:
        search_link = self.driver.find_element(By.LINK_TEXT, 'Search')
        self.assertIn("/search_page", search_link.get_attribute('href'))

        home_link = self.driver.find_element(By.LINK_TEXT, 'Home')
        self.assertIn("/internal", home_link.get_attribute('href'))

    def tearDown(self):
        # Close the browser after tests
        self.driver.close()
