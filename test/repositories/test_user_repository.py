import unittest
from repositories import schemas
from database import get_db
from repositories.anime_repository import AnimeRepository
from repositories.user_repository import UserRepository


class TestUserRepository(unittest.TestCase):
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

    test_anime = schemas.Anime(
        mal_id=1,
        title="Death Note",
        main_picture="None",
        popularity=100,
        synopsis="Note and death",
        rating="BS21",
        genre_list=["Drama", "Thriller"],
        episodes=10,
        duration=123
    )

    def setUp(self):
        self.db = get_db("sqlite:///:memory:")
        self.repository = UserRepository(self.db)
        self.anime_repository = AnimeRepository(self.db)

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

        for user in users:
            self.assertIn(user, self.repository.list())

        for user in users_to_create:
            self.repository.delete(user.username)

    def test_add_anime_user_not_found(self):
        result = self.repository.add_anime('non-existent-user', 1)
        self.assertEqual(result, False)

    def test_add_anime_already_added(self):
        self.repository.create(self.create_user)
        self.repository.add_anime(self.create_user.username, 1)
        result = self.repository.add_anime(self.create_user.username, 1)
        self.assertEqual(result, False)
        self.repository.delete(self.create_user.username)

    def test_add_anime(self):
        self.repository.create(self.create_user)
        self.anime_repository.create(self.test_anime)
        result = self.repository.add_anime(self.create_user.username, 1)
        self.assertEqual(result, True)
        user = self.repository.get(self.create_user.username)
        self.assertEqual(user.anime[0].mal_id, 1)
        self.anime_repository.delete(self.test_anime.mal_id)
        self.repository.delete(self.create_user.username)

    def test_delete_anime_user_not_found(self):
        result = self.repository.delete_anime(self.create_user.username, 1)
        self.assertEqual(result, False)

    def test_delete_anime_not_associated(self):
        self.repository.create(self.create_user)
        result = self.repository.delete_anime(self.create_user.username, 1)
        self.assertEqual(result, False)

    def test_delete_anime(self):
        self.repository.create(self.create_user)
        self.anime_repository.create(self.test_anime)
        self.repository.add_anime(self.create_user.username, self.test_anime.mal_id)
        result = self.repository.delete_anime(self.create_user.username, self.test_anime.mal_id)
        self.assertEqual(result, True)
