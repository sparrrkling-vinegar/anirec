import database
import schemas


def convert_anime(anime: database.Anime) -> schemas.Anime:
    return schemas.Anime(
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


def convert_user(user: database.User) -> schemas.User:
    return schemas.User(
        username=user.username,
        icon=user.icon,
        password=user.password,
        anime=list(map(convert_anime, user.anime))
    )
