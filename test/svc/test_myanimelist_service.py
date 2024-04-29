import unittest
from unittest.mock import patch, MagicMock

from myanimelistpy.models.anime import Anime

from svc import schemas
from svc.myanimelist_service import BaseAnimeApiService


class TestBaseAnimeApiService(unittest.TestCase):
    def setUp(self):
        self.service = BaseAnimeApiService(client_id="test")

    @patch('myanimelistpy.myanimelist.MyAnimeList.getAnimeList')
    def test_get_anime_by_name(self, mock_getAnimeList):
        # Mock response for the method getAnimeListInDict
        mock_getAnimeList.return_value = [
            Anime(
                {
                    "title": "Naruto",
                    "id": 1,
                    "main_picture": {
                        'medium': 'https://image_url',
                        'large': 'https://image_url'
                    },
                    "synopsis": "A ninja adventure",
                    "popularity": 1234,
                    "num_episodes": 220,
                    "average_episode_duration": 1200,
                    "rating": "rx",
                    "genres": [{"id": "test", "name": "Adventure"}],
                },
                [
                    "synopsis",
                    "popularity",
                    "num_episodes",
                    "average_episode_duration",
                    "rating",
                    "genres"
                ]
            )
        ]

        # Using the MyAnimeList API Service to get anime by name
        result = self.service.get_anime_by_name("Naruto", limit=1)

        # Assertions to ensure method works correctly
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], schemas.Anime)
        self.assertEqual(result[0].title, "Naruto")

    @patch('requests.get')
    def test_get_random_anime(self, mock_get):
        mock_get.return_value.json.return_value = {
            "data": {
                "title": "Random Anime",
                "mal_id": 98765,
                "images": {"jpg": {"large_image_url": "https://image_url"}},
                "synopsis": "Random story",
                "popularity": 4321,
                "episodes": 12,
                "rating": "R",
                "duration": "24 min per ep",
                "genres": [{"name": "Comedy"}]
            }
        }

        result = self.service.get_random_anime(1)

        # Asserts
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], schemas.Anime)
        self.assertEqual(result[0].title, "Random Anime")
