from myanimelistpy.myanimelist import MyAnimeList
import schemas
import requests
import os

CLIENT_ID = os.environ["CLIENT_ID"]

def get_anime_by_name(name: str, limit: int) -> list[schemas.Anime]:
    my_anime_list = MyAnimeList(client_id=CLIENT_ID)

    anime_list = my_anime_list.getAnimeList(
        anime_name = name,
        limit      = limit,
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
        episodes = -1 if (ep := anime.getNumEpisodes()) == None else ep
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
 

def get_random_anime(limit: int) -> list[schemas.Anime]:
    res = []
    for _ in range(limit):

        url = "https://api.jikan.moe/v4/random/anime"
        resp = requests.get(url=url)
        data = resp.json()["data"]
        
        title = data["title"]
        mal_id = data["mal_id"]
        main_picture = data["images"]["jpg"]["large_image_url"]
        synopsis = "" if (syn := data["synopsis"]) == None else syn
        popularity = data["popularity"]
        episodes = -1 if (ep := data["episodes"]) == None else ep
        rating = data["rating"]
        try:
            duration = int(data["duration"].split()[0]) # !!"24 min per ep"!!
        except ValueError as e:
            print(e)
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

if __name__ == "__main__":
    an = get_random_anime(2)

    for a in an:
        print(a)
