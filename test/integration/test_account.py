import unittest
from unittest.mock import patch

import pytest
from starlette.testclient import TestClient

from main import app
from repositories import schemas


@pytest.mark.e2e
class TestAccount(unittest.TestCase):
    username = "username"
    password = "StrongPassword123!"
    user = schemas.User(
        username=username,
        password=password,
        anime=[]
    )

    @patch('main.get_current_user')
    def setUp(self, get_current_user):
        self.client = TestClient(app)
        self.client.post("/signup", data={
            "username": self.username,
            "password": self.password
        })
        get_current_user.return_value = self.user

    def test_update_password(self):
        response = self.client.post("/update_account", data={
            "password": "NewStrongPassword123!",
        })
        self.assertEqual(response.status_code, 200)
