from typing import Optional

from pydantic import BaseModel


class AnimeBase(BaseModel):
    mal_id: int
    title: str
    main_picture: str
    popularity: int
    synopsis: str
    rating: str
    genre_list: list[str]
    episodes: int
    duration: int


class CreateAnime(AnimeBase):
    pass


class GetAnime(BaseModel):
    mal_id: int


class Anime(AnimeBase):
    class Config:
        from_attributes = True


class EditAnime(BaseModel):
    mal_id: int
    title: Optional[str] = None
    main_picture: Optional[str] = None
    popularity: Optional[int] = None
    synopsis: Optional[str] = None
    rating: Optional[str] = None
    genre_list: Optional[list[str]] = None
    episodes: Optional[int] = None
    duration: Optional[int] = None


class UserBase(BaseModel):
    username: str
    icon: Optional[int] = None
    password: str


class CreateUser(UserBase):
    pass


class User(UserBase):
    anime: list[Anime]

    class Config:
        from_attributes = True


class EditUser(BaseModel):
    username: Optional[str]
    icon: Optional[str] = None
    password: Optional[str] = None
