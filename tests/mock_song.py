from typing import List

from random import randint, choice, sample
from itertools import product
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker, Session
from faker import Faker

from model.alchemy.tables import *
from model.alchemy.install import sqlite_engine


def mock_song_name():
    """
    https://wordcounter.net/blog/2017/01/09/102797_most-popular-words-songs.html
    """

    verbs = [
        "Breathe", "Get", "Cry", "Dance",
        "Beat", "Raise", "Imagine", "Draw", "Kill",
        "Mourn", "Like", "Run", "Swing", "Bang", "Loose",
        "Love", "Fly"
    ]

    adjectives = [
        "Little", "Lonely", "Cute",
        "Dancin’", "Rock", "Disco", "Crazy", "Mad",
        "Christmas", "New Years", "Easter", "Holiday", "Haloween's",
        "Violent", "Brutal", "Reckless", "Heedless", "Gentle",
        "Sexy", "Funny", "Naive", "Romantic",
        "Red", "Green", "Blue", "Violet", "Pink", "Purple",
        "Yellow", "Moon", "Sunny"
    ]

    nouns = [
        "Girl", "Heart", "Life", "Back",
        "Time", "Night", "Day", "Man", "Dream", "World",
        "Moon", "Serenade", "Blues", "Hell", "Heaven",
        "Angel", "Devil", "Death", "Booze", "Airplane",
        "Faith", "Money", "Honey", "Bunny", "Sonata",
        "Arctic", "Sword", "Field", "Glamour", "Magic",
        "Chant", "Enchantment", "Spell", "Monkey", "Zoo",
        "Elephant", "Cat", "Dog", "Eye", "Lip", "Booze",
        "Moon", "Sun", "Wine", "Beach", "Heart", "Wing",
        "Hand", "House", "Car", "Garden", "Tree", "Song",
        "Rhyme", "Ghost", "Trap", "Maze", "Tear", "Lake",
        "River", "Vale", "Wind", "Heat", "Beat", "Mirror"
    ]

    prefix = ["The"] * 10 + ["My", "Your"]

    name_parts = [
        choice(verbs) if randint(0, 4) > 1 else None,
        choice(prefix),
        choice(adjectives) if randint(0, 4) > 3 else None,
        choice(adjectives) if randint(0, 1) else None,
        choice(nouns)
    ]
    name_parts = [part for part in name_parts if part is not None]
    return " ".join(name_parts)


def mock_genre():
    sub = [
        "Synth", "Black", "Doom", "Punk", "Blues", "Death",
        "Speed", "Power", "Glam", "Hard", "Heavy", "Thrash",
        "Gothic", "Folk", "Progressive", "Industrial", "Nu",
        "Post", "Alternative", "Symphonic", "Dark", "Melodic",
        "Classical", "Electronic", "Reggae", "Soul",
        "Funk", "Disco", "Techno", "House", "Trance",
        "Ambient", "Industrial"
    ]
    main = [
        "Rock", "Pop", "Jazz", "Metal", "Folk", "Grunge",
        "Rap", "Drum&Bass", "Country", "Blues", "Reggae",
        "Soul", "Funk", "Disco", "Techno", "House", "Trance",
        "Gospel", "Hip-Hop",
    ]
    return [
        " ".join(pair)
        for pair in product(sub + main, main)
        if pair[0] != pair[1]
    ]


def db_tags(session: Session, limit: int = 100):
    f = Faker()
    existing_tags = set(
        session.execute(
            select(Tag.name).distinct()
        ).scalars().all()
    )
    new_tags = []
    i = len(existing_tags)
    while i < limit:
        name = f.word()
        if name in existing_tags:
            continue
        existing_tags.add(name)
        new_tags.append(Tag(name=name))
        i += 1
    session.add_all(new_tags)
    session.flush()
    session.commit()
    return [
        row[0]
        for row in session.execute(
            select(Tag)
        ).all()
    ]


def db_artists(session: Session, limit: int = 100):
    """
    Adds artists to the database
    """
    f = Faker()
    existing_artists = set(
        session.execute(
            select(Artist.name).distinct()
        ).scalars().all()
    )
    new_artists = []
    i = len(existing_artists)
    while i < limit:
        name = f.name()
        if name in existing_artists:
            continue
        existing_artists.add(name)
        new_artists.append(Artist(name=name))
        i += 1
    session.add_all(new_artists)
    session.flush()
    session.commit()
    return [
        row[0]
        for row in session.execute(
            select(Artist)
        ).all()
    ]


def db_genres(session: Session):
    """
    Adds genres to the database
    """
    existing_genres = set(
        session.execute(
            select(Genre.name).distinct()
        ).scalars().all()
    )
    genres = set(mock_genre())
    new_genres = genres - existing_genres
    new_genres = [
        Genre(name=genre)
        for genre in new_genres
    ]
    session.add_all(new_genres)
    session.flush()
    session.commit()
    return [
        row[0]
        for row in session.execute(
            select(Genre).distinct()
        ).all()
    ]


def mock_songs(n: int):
    """
    Mocks n songs and adds them to the database
    """
    engine = sqlite_engine("../db.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    genres = db_genres(session)
    artists = db_artists(session)
    tags = db_tags(session)

    existing_songs = set(
        session.execute(
            select(Song.name).distinct()
        ).scalars().all()
    )
    i = len(existing_songs)
    new_files = []
    new_songs = []
    while i < n:
        song_name = mock_song_name()
        if song_name in existing_songs:
            continue
        existing_songs.add(song_name)
        new_file = SongFile(duration=500 + randint(-120,120))
        new_song = Song(
            name=song_name
        )
        new_song.file = new_file

        new_song.artist = choice(artists)

        song_genres = sample(genres, randint(1, 3))
        for genre in song_genres:
            new_song.genres.append(genre)

        song_tags = sample(tags, randint(1, 3))
        for tag in song_tags:
            new_song.tags.append(tag)

        new_files.append(new_file)
        new_songs.append(new_song)
        i += 1
    session.add_all(new_files)
    session.flush()
    session.commit()
    session.add_all(new_songs)
    session.flush()
    session.commit()


if __name__ == "__main__":
    print(mock_songs(10_000))