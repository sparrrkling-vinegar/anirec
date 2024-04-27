import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TestSignupPage(unittest.TestCase):
    def setUp(self):
        # Set up the Firefox WebDriver
        self.driver = webdriver.Firefox()
        self.driver.get('http://localhost:8080/signup')

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

        # Further actions to check for successful signup could be added here, e.g., redirection, success message,
        # or checking error elements if validations fail or display an error message.

    def tearDown(self):
        # Close the browser window on test completion
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
