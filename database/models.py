from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):
    __tablename__ = 'User'

    username = Column(String, primary_key=True)
    password = Column(String)
    icon = Column(String)

    anime = relationship('Anime', secondary='UserAnime', back_populates='users')


class Anime(Base):
    __tablename__ = 'Anime'

    mal_id = Column(Integer, primary_key=True)
    title = Column(String)
    main_picture = Column(String)
    popularity = Column(Integer)
    synopsis = Column(String)
    rating = Column(String)
    genre_list = Column(JSON)
    episodes = Column(Integer)
    duration = Column(Integer)

    users = relationship('User', secondary='UserAnime', back_populates='anime')


class UserAnime(Base):
    __tablename__ = "UserAnime"

    username = Column(Integer, ForeignKey('User.username'), primary_key=True)
    mal_id = Column(Integer, ForeignKey("Anime.mal_id"), primary_key=True)
