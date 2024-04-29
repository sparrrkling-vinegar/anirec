import unittest

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.mark.e2e
class TestAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @pytest.mark.order(0)
    def test_signup_weak_password(self):
        response = self.client.post("/signup", data={"username": "user", "password": "WeakPassword"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Weak password.", response.text)

    @pytest.mark.order(1)
    def test_signup_success(self):
        response = self.client.post("/signup", data={"username": "user", "password": "StrongPassword123!"})
        self.assertEqual(response.status_code, 200)

    @pytest.mark.order(2)
    def test_signup_failure_user_exists(self):
        response = self.client.post("/signup", data={"username": "user", "password": "StrongPassword123!"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username already exists", response.text)

    @pytest.mark.order(2)
    def test_login_with_non_existing_user(self):
        response = self.client.post("/signin", data={
            "username": "non-existing-user",
            "password": "StrongPassword123!"
        })
        self.assertIn("User does not exist.", response.text)

    @pytest.mark.order(2)
    def test_login_with_incorrect_password(self):
        response = self.client.post("/signin", data={"username": "user", "password": "1WrongPassword!"})
        self.assertIn("Incorrect password.", response.text)

    @pytest.mark.order(2)
    def test_login_success(self):
        response = self.client.post("/signin", data={"username": "user", "password": "StrongPassword123!"})
        self.assertEqual(response.status_code, 200)

