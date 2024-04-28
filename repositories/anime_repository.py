from typing import Optional, List

import schemas
from database import get_db
from database.models import Anime, User
from repositories.utils import convert_anime, convert_user


class AnimeRepository:

    def __init__(self, db):
        self.db = db

    def create(self, anime: schemas.Anime):
        if self.db.query(Anime).filter(Anime.mal_id == anime.mal_id).first() is not None:
            return
        db_anime: Anime = Anime(
            mal_id=anime.mal_id,
            title=anime.title,
            main_picture=anime.main_picture,
            popularity=anime.popularity,
            synopsis=anime.synopsis,
            rating=anime.rating,
            genre_list=anime.genre_list,
            episodes=anime.episodes,
            duration=anime.duration
        )
        self.db.add(db_anime)
        self.db.commit()

    def get(self, mal_id: int) -> Optional[Anime]:
        db_anime: Anime = self.db.query(Anime).filter(Anime.mal_id == mal_id).first()
        if db_anime is None:
            return None
        return convert_anime(db_anime)

    def delete(self, mal_id: int):
        db_anime: Anime = self.db.query(Anime).filter(Anime.mal_id == mal_id).first()
        if db_anime is None:
            return
        self.db.delete(db_anime)
        self.db.commit()

    def edit(self, anime_info: schemas.EditAnime):
        db_anime: Anime = self.db.query(Anime).filter(Anime.mal_id == anime_info.mal_id).first()
        if db_anime is None:
            return
        if anime_info.title is not None:
            db_anime.title = anime_info.title
        if anime_info.main_picture is not None:
            db_anime.main_picture = anime_info.main_picture
        if anime_info.popularity is not None:
            db_anime.popularity = anime_info.popularity
        if anime_info.synopsis is not None:
            db_anime.synopsis = anime_info.synopsis
        if anime_info.rating is not None:
            db_anime.rating = anime_info.rating
        if anime_info.genre_list is not None:
            db_anime.genre_list = anime_info.genre_list
        if anime_info.episodes is not None:
            db_anime.episodes = anime_info.episodes
        if anime_info.duration is not None:
            db_anime.duration = anime_info.duration
        self.db.commit()

    def add_user(self, username: str, mal_id: int):
        db_anime = self.db.query(Anime).filter(Anime.mal_id == mal_id).first()
        if db_anime is None or username in map(lambda x: x.username, db_anime.users):
            return
        db_user = self.db.query(User).filter(User.username == username).first()
        if db_user is None:
            return
        db_anime.users.append(db_user)
        self.db.commit()

    def delete_user(self, username: str, mal_id: int):
        db_anime = self.db.query(Anime).filter(Anime.mal_id == mal_id).first()
        if db_anime is None or username not in map(lambda x: x.username, db_anime.users):
            return
        db_user = self.db.query(User).filter(User.username == username).first()
        if db_user is None:
            return
        db_anime.users.remove(db_user)
        self.db.commit()

    def list(self, skip: int = 0, limit: int = 100) -> list[Anime]:
        return list(
            map(
                convert_anime,
                self.db.query(Anime).offset(skip).limit(limit).all()
            )
        )

    def users(self, mal_id) -> Optional[List[schemas.User]]:
        db_anime = self.db.query(Anime).filter(Anime.mal_id == mal_id).first()
        if db_anime is None:
            return None
        return list(
            map(
                convert_user,
                db_anime.users
            )
        )


if __name__ == "__main__":
    anime_service = AnimeRepository(get_db())
    anime_service.create(
        schemas.Anime(
            mal_id="1",
            title="Death Note",
            main_picture="None",
            popularity=100,
            synopsis="Note and death",
            rating="BS21",
            genre_list=["Drama", "Thriller"],
            episodes=10,
            duration=123
        )
    )
    # print(anime_service.get("1"))
    # print(anime_service.list())
    # anime_service.delete(mal_id="1")
    # anime_service.edit(
    #     schemas.EditAnime(
    #         mal_id="1",
    #         title="THE BEST ANIME"
    #     )
    # )
    # anime_service.add_user("Anton", "1")
    anime_service.delete_user("Anton", "1")
    # print(anime_service.list())

    # print(us.get_user(
    #     GetUser(username="Anton")
    # ))
