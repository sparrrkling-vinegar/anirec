from repositories.user_repository import UserRepository
from repositories.anime_repository import AnimeRepository
from database import get_db
import schemas


class EnrollService:

    def __init__(self, user_repository: UserRepository, anime_repository: AnimeRepository):
        self.__user_repository = user_repository
        self.__anime_repository = anime_repository

    def connect(self, username: str, mal_id: int):
        self.__user_repository.add_anime(username, mal_id)

    def disconnect(self, username: str, mal_id: int):
        self.__user_repository.delete_anime(username, mal_id)


class EnrollServiceFactory:
    @staticmethod
    def make() -> EnrollService:
        user_repository = UserRepository(get_db())
        anime_repository = AnimeRepository(get_db())
        return EnrollService(user_repository, anime_repository)
