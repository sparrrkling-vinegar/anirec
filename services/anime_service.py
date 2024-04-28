from repositories.anime_repository import AnimeRepository
from database import get_db
import schemas


class AnimeAlreadyExists(Exception):
    pass


class AnimeDoesNotExist(Exception):
    pass


class AnimeService:
    def __init__(self, anime_repository: AnimeRepository):
        self.__anime_repository = anime_repository

    def add(self, anime: schemas.Anime):
        if self.__anime_repository.get(anime.mal_id) is not None:
            raise AnimeAlreadyExists()
        self.__anime_repository.create(anime)

    def get(self, mal_id):
        if self.__anime_repository.get(mal_id) is None:
            raise AnimeDoesNotExist()
        return self.__anime_repository.get(mal_id)

    def delete(self, mal_id: int):
        if self.__anime_repository.get(mal_id) is None:
            raise AnimeDoesNotExist()
        self.__anime_repository.delete(mal_id)


class AnimeServiceFactory:
    @staticmethod
    def make() -> AnimeService:
        anime_repository = AnimeRepository(get_db())
        return AnimeService(anime_repository)
