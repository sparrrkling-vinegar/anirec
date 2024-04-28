import pydantic


class Anime(pydantic.BaseModel):
    title: str
    mal_id: int
    main_picture: str
    popularity: int
    synopsis: str
    rating: str
    genre_list: list[str]
    episodes: int
    duration: int
