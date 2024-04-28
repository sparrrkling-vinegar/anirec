import unittest
from unittest.mock import Mock, patch

from repositories.schemas import CreateUser, User, EditUser
from repositories.user_repository import UserRepository
from services.user_service import UserService, UserAlreadyExists, WeakPassword, UserDoesNotExist, WrongPassword


class TestUserService(unittest.TestCase):
    create_user = CreateUser(username="Username", password="Password", icon="123")
    user = User(username="Username", password="Password", icon="123", anime=[])
    edit_user = EditUser(username=None, password="new_password")

    def setUp(self):
        self.repo = Mock(spec=UserRepository)
        self.user_service = UserService(self.repo)

    def test_register_successfully(self):
        # Given
        self.repo.get.return_value = None
        with patch('services.user_service.check_password', return_value=True):
            # When
            self.user_service.register(self.create_user)
            # Then
            self.repo.create.assert_called_once_with(self.create_user)

    def test_register_user_already_exists(self):
        # Given
        self.repo.get.return_value = self.create_user
        # Then
        with self.assertRaises(UserAlreadyExists):
            # When
            self.user_service.register(self.create_user)

    def test_register_weak_password(self):
        # Given
        self.repo.get.return_value = None
        with patch('services.user_service.check_password', return_value=False):
            # Then
            with self.assertRaises(WeakPassword):
                # When
                self.user_service.register(self.create_user)

    def test_login_success(self):
        # Given
        username = self.user.username
        password = self.user.password
        self.repo.get.return_value = self.user
        # When
        result = self.user_service.login(username, password)
        # Then
        self.assertEqual(result, self.user)

    def test_login_user_does_not_exist(self):
        # Given
        username = self.user.username
        password = self.user.password
        self.repo.get.return_value = None
        # Then
        with self.assertRaises(UserDoesNotExist):
            # When
            self.user_service.login(username, password)

    def test_login_wrong_password(self):
        # Given
        username = self.user.username
        password = self.user.password + 'wrong password'
        self.repo.get.return_value = self.user
        # Then
        with self.assertRaises(WrongPassword):
            # When
            self.user_service.login(username, password)

    def test_update_user_password(self):
        # Given
        username = self.user.username
        current_user = self.user
        new_info = self.edit_user
        self.repo.get.return_value = current_user
        with patch('services.user_service.check_password', return_value=True) as mocked_check_password:
            # When
            self.user_service.update(username, new_info)
            # Then
            mocked_check_password.assert_called_once_with(new_info.password)
            self.repo.edit.assert_called_once_with(username, new_info)
            self.repo.get.assert_called_with(username)
