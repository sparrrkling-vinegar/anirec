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

        self.driver.implicitly_wait(3)
        self.driver.get(f'{API_URL}/internal')

    def test_page_title(self):
        # Confirm that the internal page title is correct
        self.assertIn('Internal Page', self.driver.title)

    def test_welcome_message(self):
        # Ensure that the welcome message is displayed correctly
        welcome_message = self.driver.find_element(
            By.XPATH,
            "//h2[contains(text(), 'Welcome to Internal Page!')]"
        )
        self.assertTrue(welcome_message.is_displayed())

    def test_navigation_links(self):
        # Check that navigation links (from the base template) are present and correctly linked
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

        self.driver.implicitly_wait(3)
        self.driver.get(f"{API_URL}/recommendation")

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

        self.driver.implicitly_wait(3)
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

        WebDriverWait(self.driver, 10).until(
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


class TestSignupPage(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

        self.driver.get(f'{API_URL}/signup')

    def test_title(self):
        # Check if the page title is correct
        self.assertIn('New user', self.driver.title)

    def test_username_password_inputs(self):
        # Check for existence and proper labeling of username and password inputs
        username_input = self.driver.find_element(By.ID, "form2Example1")
        password_input = self.driver.find_element(By.ID, "form2Example2")

        # Input 'name' attributes should match expected names
        self.assertEqual(username_input.get_attribute('name'), 'username')
        self.assertEqual(password_input.get_attribute('name'), 'password')

        # Input labeling
        username_label = self.driver.find_element(By.XPATH, "//label[@for='form2Example1']")
        password_label = self.driver.find_element(By.XPATH, "//label[@for='form2Example2']")

        self.assertEqual(username_label.text, 'Username')
        self.assertEqual(password_label.text, 'Password')

    def test_signup_action(self):
        # Simulate user input and submit action for the signup form
        self.driver.find_element(By.ID, "form2Example1").send_keys("new_user")
        self.driver.find_element(By.ID, "form2Example2").send_keys("new_password123")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    def tearDown(self):
        # Close the browser window on test completion
        self.driver.close()
