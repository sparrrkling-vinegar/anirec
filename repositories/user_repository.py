from typing import List

from repositories import schemas
from database.models import User, Anime
from repositories.utils import convert_user


class UserRepository:
    def __init__(self, db):
        self.db = db

    def create(self, user: schemas.CreateUser):
        if self.db.query(User).filter(User.username == user.username).first() is not None:
            return
        db_user = User(
            username=user.username,
            password=user.password,  # TODO: use hash instead
            icon=user.icon
        )
        self.db.add(db_user)
        self.db.commit()

    def get(self, username: str) -> schemas.User | None:
        db_user = self.db.query(User).filter(User.username == username).first()
        if db_user is None:
            return None

        return convert_user(db_user)

    def delete(self, username: str):
        db_user = self.db.query(User).filter(User.username == username).first()
        if db_user is None:
            return
        self.db.delete(db_user)
        self.db.commit()

    def edit(self, username: str, user_info: schemas.EditUser):
        db_user = self.db.query(User).filter(User.username == username).first()
        if db_user is None:
            return
        if user_info.username is not None:
            db_user.username = user_info.username
        if user_info.password is not None:
            db_user.password = user_info.password  # TODO: use hash instead
        if user_info.icon is not None:
            db_user.icon = user_info.icon
        self.db.commit()

    def add_anime(self, username: str, mal_id: int):
        db_user = self.db.query(User).filter(User.username == username).first()
        if db_user is None or mal_id in map(lambda x: x.mal_id, db_user.anime):
            return False
        db_anime = self.db.query(Anime).filter(Anime.mal_id == mal_id).first()
        if db_anime is None:
            return False
        db_user.anime.append(db_anime)
        self.db.commit()
        return True

    def delete_anime(self, username: str, mal_id: int):
        db_user = self.db.query(User).filter(User.username == username).first()
        if db_user is None or mal_id not in map(lambda x: x.mal_id, db_user.anime):
            return False
        db_anime = self.db.query(Anime).filter(Anime.mal_id == mal_id).first()
        if db_anime is None:
            return False
        db_user.anime.remove(db_anime)
        self.db.commit()
        return True

    def list(self, skip: int = 0, limit: int = 100) -> List[schemas.User]:
        return list(
            map(
                convert_user,
                self.db.query(User).offset(skip).limit(limit).all()
            )
        )
