from repositories import schemas
from services.anime_service import AnimeService
from services.enroll_service import EnrollService
from services.user_service import UserService
from svc.myanimelist_service import AnimeApiService
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from collections import defaultdict


class RecommendationsService(ABC):
    @abstractmethod
    def get_recommendations(self, users_anime: [schemas.Anime], limit: int = 10):
        pass


class BaseRecommendationsService(RecommendationsService):
    def __init__(
            self,
            user_service: UserService,
            enroll_service: EnrollService,
            anime_service: AnimeService,
            anime_api_service: AnimeApiService
    ):
        self.__user_service = user_service
        self.__enroll_service = enroll_service
        self.__anime_service = anime_service
        self.__anime_api_service = anime_api_service

    def get_recommendations(
            self,
            users_anime: List[schemas.Anime],
            limit: int = 10
    ) -> List[schemas.Anime]:
        result = []
        watched_ids = set(map(lambda x: x.mal_id, users_anime))
        users_most_watched_categories = self.__most_watched_categories(users_anime, limit=3)
        most_frequent_anime = list(
            map(
                lambda x: x[0],
                sorted(
                    self.__get_frequency_anime(),
                    key=lambda x: -x[1]
                )
            )
        )

        for anime in most_frequent_anime:
            if len(set(anime.genre_list).union(users_most_watched_categories)) == 0 \
                    or anime.mal_id in watched_ids:
                continue
            result.append(anime)
            if len(result) == limit:
                return result
        result.extend(self.__anime_api_service.get_random_anime(limit=limit - len(result)))
        return list(sorted(result, key=lambda x: -x.popularity))

    def __most_watched_categories(self, users_anime: List[schemas.Anime], limit=None) -> List[str]:
        counter = defaultdict(int)
        for anime in users_anime:
            for genre in anime.genre_list:
                counter[genre] += 1
        return list(map(lambda x: x[0], sorted(counter.items(), key=lambda x: -x[1])))[:limit]

    def __get_frequency_anime(self, limit=10000) -> List[Tuple[schemas.Anime, int]]:
        result_dict: Dict[int, Tuple[schemas.Anime, int]] = dict()
        for user in self.__user_service.list(limit=limit):
            for anime in user.anime:
                if anime.mal_id in result_dict:
                    result_dict[anime.mal_id] = (
                        result_dict[anime.mal_id][0],
                        result_dict[anime.mal_id][1] + 1
                    )
                else:
                    result_dict[anime.mal_id] = (anime, 1)
        return list(result_dict.values())
