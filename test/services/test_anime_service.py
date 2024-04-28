import unittest
from unittest.mock import Mock

from repositories import schemas
from repositories.anime_repository import AnimeRepository
from services.anime_service import AnimeService, AnimeAlreadyExists, AnimeDoesNotExist


class AnimeServiceTests(unittest.TestCase):
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
        self.repo = Mock(spec=AnimeRepository)
        self.service = AnimeService(self.repo)

    def test_add_anime_successfully(self):
        # Given
        self.repo.get.return_value = None
        # When
        self.service.add(self.test_anime)
        # Then
        self.repo.create.assert_called_once_with(self.test_anime)

    def test_add_anime_raises_exception(self):
        # Given
        self.repo.get.return_value = self.test_anime
        # Then
        with self.assertRaises(AnimeAlreadyExists):
            # When
            self.service.add(self.test_anime)

    def test_get_existing_anime(self):
        # Given
        mal_id = self.test_anime.mal_id
        self.repo.get.return_value = self.test_anime
        # When
        result = self.service.get(mal_id)
        # Then
        self.assertEqual(result, self.test_anime)

    def test_get_nonexistent_anime_raises_exception(self):
        # Given
        mal_id = self.test_anime.mal_id
        self.repo.get.return_value = None
        # Then
        with self.assertRaises(AnimeDoesNotExist):
            # When
            self.service.get(mal_id)

    def test_delete_existing_anime(self):
        # Given
        mal_id = self.test_anime.mal_id
        self.repo.get.return_value = self.test_anime
        # When
        self.service.delete(mal_id)
        # Then
        self.repo.delete.assert_called_once_with(mal_id)

    def test_delete_nonexistent_anime_raises_exception(self):
        # Given
        mal_id = self.test_anime.mal_id
        self.repo.get.return_value = None
        # Then
        with self.assertRaises(AnimeDoesNotExist):
            # When
            self.service.delete(mal_id)
