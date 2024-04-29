import unittest

from repositories import schemas
from database import get_db
from repositories.anime_repository import AnimeRepository


class TestAnimeRepository(unittest.TestCase):
    repository = AnimeRepository(get_db("sqlite:///:memory:"))
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

    full_edit_anime = schemas.EditAnime(
        mal_id=1,
        title="JOJO!",
        main_picture="123",
        popularity=120,
        synopsis="Note and death !!!",
        rating="BS2112",
        genre_list=["Pupa"],
        episodes=100,
        duration=40
    )

    partial_edit_anime = schemas.EditAnime(
        mal_id=1,
        title="JOJO!",
        genre_list=["Pupa"],
        episodes=100,
        duration=40
    )

    def test_create_anime(self):
        self.repository.create(self.test_anime)
        self.assertEqual(self.test_anime, self.repository.get(mal_id=1))
        self.repository.delete(self.test_anime.mal_id)

    def test_get_existing_anime(self):
        self.repository.create(self.test_anime)
        self.assertEqual(self.repository.get(mal_id=1), self.test_anime)
        self.repository.delete(self.test_anime.mal_id)

    def test_get_not_existing_anime(self):
        self.assertEqual(self.repository.get(mal_id=322), None)

    def test_delete_anime(self):
        self.repository.create(self.test_anime)
        self.repository.delete(mal_id=1)
        self.assertEqual(self.repository.get(mal_id=1), None)

    def test_full_edit_anime(self):
        self.repository.create(self.test_anime)
        self.repository.edit(self.full_edit_anime)
        self.assertEqual(
            schemas.Anime(
                mal_id=1,
                title="JOJO!",
                main_picture="123",
                popularity=120,
                synopsis="Note and death !!!",
                rating="BS2112",
                genre_list=["Pupa"],
                episodes=100,
                duration=40
            ),
            self.repository.get(mal_id=1)
        )
        self.repository.delete(self.test_anime.mal_id)

    def test_partial_edit_anime(self):
        self.repository.create(self.test_anime)
        self.repository.edit(self.partial_edit_anime)
        self.assertEqual(
            schemas.Anime(
                mal_id=1,
                title="JOJO!",
                main_picture="None",
                popularity=100,
                synopsis="Note and death",
                rating="BS21",
                genre_list=["Pupa"],
                episodes=100,
                duration=40
            ),
            self.repository.get(mal_id=1)
        )
        self.repository.delete(self.test_anime.mal_id)

    def test_list_anime(self):
        anime = [
            schemas.Anime(
                mal_id=1,
                title="Death Note1",
                main_picture="None1",
                popularity=101,
                synopsis="Note and death1",
                rating="BS211",
                genre_list=["Drama", "Thriller1"],
                episodes=101,
                duration=1231
            ),
            schemas.Anime(
                mal_id=2,
                title="Death Note2",
                main_picture="None2",
                popularity=102,
                synopsis="Note and death2",
                rating="BS212",
                genre_list=["Drama", "Thriller2"],
                episodes=2,
                duration=2
            ),
            schemas.Anime(
                mal_id=3,
                title="Death Note3",
                main_picture="None3",
                popularity=103,
                synopsis="Note and death3",
                rating="BS213",
                genre_list=["Drama", "Thriller3"],
                episodes=103,
                duration=3
            )
        ]
        for anim in anime:
            self.repository.create(anim)

        self.assertEqual(anime, self.repository.list())

        for anim in anime:
            self.repository.delete(anim.mal_id)
