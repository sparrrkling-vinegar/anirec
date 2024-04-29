from abc import ABC, abstractmethod

import requests
from myanimelistpy.myanimelist import MyAnimeList

from svc import schemas


class AnimeApiService(ABC):
    @abstractmethod
    def get_anime_by_name(self, name: str, limit: int = 10, offset: int = 0) -> list[schemas.Anime]:
        pass

    @abstractmethod
    def get_random_anime(self, limit: int) -> list[schemas.Anime]:
        pass


class BaseAnimeApiService(AnimeApiService):
    def __init__(self, client_id: str):
        self.client_id = client_id

    def get_anime_by_name(self, name: str, limit: int = 10, offset: int = 0) -> list[schemas.Anime]:
        my_anime_list = MyAnimeList(client_id=self.client_id)

        anime_list = my_anime_list.getAnimeList(
            anime_name=name,
            limit=limit,
            offset=offset,
            fields=["id", "title", "main_picture",
                    "synopsis", "popularity", "num_episodes",
                    "genres", "rating", "average_episode_duration"]
        )

        res = []

        for anime in anime_list:
            title = anime.getTitle()
            mal_id = anime.getId()
            main_picture = anime.getMainPicture().getMedium()
            synopsis = anime.getSynopsis()
            popularity = anime.getPopularity()
            episodes = -1 if (ep := anime.getNumEpisodes()) is None else ep
            rating = anime.getRating()
            duration = anime.getAvgEpisodeDurationInSeconds() // 60
            genres = [genre.getName() for genre in anime.getGenres()]
            res.append(
                schemas.Anime(
                    title=title,
                    mal_id=mal_id,
                    main_picture=main_picture,
                    synopsis=synopsis,
                    popularity=popularity,
                    rating=rating,
                    genre_list=genres,
                    episodes=episodes,
                    duration=duration
                )
            )

        return res

    def get_random_anime(self, limit: int) -> list[schemas.Anime]:
        res = []
        for _ in range(limit):

            url = "https://api.jikan.moe/v4/random/anime"
            resp = requests.get(url=url, timeout=10)
            data = resp.json()["data"]

            title = data["title"]
            mal_id = data["mal_id"]
            main_picture = data["images"]["jpg"]["large_image_url"]
            synopsis = "" if (syn := data["synopsis"]) is None else syn
            popularity = data["popularity"]
            episodes = -1 if (ep := data["episodes"]) is None else ep
            rating = "" if (rat := data["rating"]) is None else rat
            try:
                duration = int(data["duration"].split()[0])  # !!"24 min per ep"!!
            except ValueError:
                duration = -1

            genres = [genre["name"] for genre in data["genres"]]

            res.append(
                schemas.Anime(
                    title=title,
                    mal_id=mal_id,
                    main_picture=main_picture,
                    synopsis=synopsis,
                    popularity=popularity,
                    rating=rating,
                    genre_list=genres,
                    episodes=episodes,
                    duration=duration
                )
            )

        return res
