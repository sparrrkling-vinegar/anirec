import unittest

from repositories import schemas
from database import get_db
from repositories.user_repository import UserRepository


class TestUserRepository(unittest.TestCase):
    repository = UserRepository(get_db("sqlite:///:memory:"))
    create_user = schemas.CreateUser(
        username="Anton",
        icon="None",
        password="<PASSWORD>"
    )

    user = schemas.User(
        username="Anton",
        icon="None",
        password="<PASSWORD>",
        anime=[]
    )

    def test_create_user(self):
        self.repository.create(self.create_user)
        self.assertEqual(self.user, self.repository.get(username="Anton"))
        self.repository.delete(self.create_user.username)

    def test_get_not_existing_user(self):
        self.assertEqual(self.repository.get(username="Pupa"), None)

    def test_delete_user(self):
        self.repository.create(self.create_user)
        self.repository.delete(self.create_user.username)
        self.assertEqual(self.repository.get(username=self.create_user.username), None)

    def test_full_edit_user(self):
        self.repository.create(self.create_user)
        self.repository.edit(
            self.create_user.username,
            schemas.EditUser(
                username="Pupa",
                icon="123",
                password="<NEWPASSWORD>"
            )
        )
        self.assertEqual(
            schemas.User(
                username="Pupa",
                icon="123",
                password="<NEWPASSWORD>",
                anime=[]
            ),
            self.repository.get(username="Pupa")
        )
        self.repository.delete("Pupa")

    def test_partial_edit_anime(self):
        self.repository.create(self.create_user)
        self.repository.edit(
            self.create_user.username,
            schemas.EditUser(
                icon="123",
                password="<NEWPASSWORD>"
            )
        )
        self.assertEqual(
            schemas.User(
                username="Anton",
                icon="123",
                password="<NEWPASSWORD>",
                anime=[]
            ),
            self.repository.get(username="Anton")
        )
        self.repository.delete("Anton")

    def test_list_user(self):
        users_to_create = [
            schemas.CreateUser(
                username="Anton",
                icon="None",
                password="<PASSWORD>"
            ),
            schemas.CreateUser(
                username="Anton1",
                icon="None",
                password="<PASSWORD>"
            ),
            schemas.CreateUser(
                username="Anton2",
                icon="None",
                password="<PASSWORD>"
            )
        ]

        users = [
            schemas.User(
                username="Anton",
                icon="None",
                password="<PASSWORD>",
                anime=[]
            ),
            schemas.User(
                username="Anton1",
                icon="None",
                password="<PASSWORD>",
                anime=[]
            ),
            schemas.User(
                username="Anton2",
                icon="None",
                password="<PASSWORD>",
                anime=[]
            )
        ]

        for user in users_to_create:
            self.repository.create(user)

        self.assertEqual(users, self.repository.list())

        for user in users_to_create:
            self.repository.delete(user.username)


if __name__ == '__main__':
    unittest.main()
