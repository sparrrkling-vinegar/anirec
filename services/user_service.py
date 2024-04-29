import re

from repositories import schemas
from typing import List
from repositories.user_repository import UserRepository


class UserAlreadyExists(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class WrongPassword(Exception):
    pass


class WeakPassword(Exception):
    pass


def check_password(password: str) -> bool:
    # Password should at least be 8 characters long,
    # have a number, an uppercase and a lowercase letter,
    # and a special character
    # TODO: for debugging only!
    # return True
    return all([
        len(password) >= 8,
        re.search(r'\d', password) is not None,
        re.search(r'[A-Z]', password) is not None,
        re.search(r'[a-z]', password) is not None,
        re.search(r'\W', password) is not None
    ])


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def register(self, user: schemas.CreateUser) -> None:
        if self.__user_repository.get(user.username) is not None:
            raise UserAlreadyExists()
        if not check_password(user.password):
            raise WeakPassword()
        self.__user_repository.create(user)

    def login(self, username: str, password: str) -> schemas.User:
        user = self.__user_repository.get(username)
        if user is None:
            raise UserDoesNotExist()
        if user.password != password:
            raise WrongPassword()
        return user

    def get(self, username: str) -> schemas.User:
        user = self.__user_repository.get(username)
        # TODO: perform image decoding
        if user is None:
            raise UserDoesNotExist()
        return user

    def update(self, username: str, user_info: schemas.EditUser) -> schemas.User:
        user = self.__user_repository.get(username)
        if user is None:
            raise UserDoesNotExist()
        if user_info.password is not None and not check_password(user_info.password):
            raise WeakPassword()
        self.__user_repository.edit(username, user_info)

        return self.__user_repository.get(
            username if user_info.username is None else user_info.username
        )

    def list(self, limit=1000) -> List[schemas.User]:
        return self.__user_repository.list(limit=limit)
