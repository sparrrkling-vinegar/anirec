import unittest
from unittest.mock import Mock

from repositories.anime_repository import AnimeRepository
from repositories.user_repository import UserRepository
from services.enroll_service import EnrollService


class TestEnrollService(unittest.TestCase):

    def setUp(self):
        self.user_repo = Mock(spec=UserRepository)
        self.anime_repo = Mock(spec=AnimeRepository)
        self.enroll_service = EnrollService(self.user_repo, self.anime_repo)

    def test_connect_associates_user_to_anime(self):
        # Given
        username = 'name'
        mal_id = 1
        # When
        self.enroll_service.connect(username, mal_id)
        # Then
        self.user_repo.add_anime.assert_called_once_with(username, mal_id)

    def test_disconnect_dissociates_user_from_anime(self):
        # Given
        username = 'name'
        mal_id = 1
        # When
        self.enroll_service.disconnect(username, mal_id)
        # Then
        self.user_repo.delete_anime.assert_called_once_with(username, mal_id)
