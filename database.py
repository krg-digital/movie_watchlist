# title: string, release_date: timestamp, watched: integer
import datetime
import sqlite3

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies(
    title TEXT,
    release_timestamp REAL,
    watched INTEGER
);"""
INSERT_MOVIES = """INSERT INTO movies (
    title, 
    release_timestamp, 
    watched
) VALUES (?, ?, 0);"""
WATCH_MOVIE = "UPDATE movies SET watched = ? WHERE title = ?;"
SELECT_MOVIE = "SELECT * FROM movies WHERE title = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = "SELECT * FROM movies WHERE watched >= 1;"

connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)

# TODO: validate 'release_timestamp' so that it's valid POSIX time.


def add_movie(title: str, release_timestamp: int):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def watch_movie(title: str):
    cursor = connection.execute(SELECT_MOVIE, (title,)).fetchone()
    current_watched = cursor[2]
    with connection:
        connection.execute(WATCH_MOVIE, (current_watched + 1, title))


def get_movie(title: str):
    cursor = connection.execute(SELECT_MOVIE, (title,)).fetchone()

    return cursor


def get_movies(upcoming: bool = False):
    cursor = connection.cursor()

    if not upcoming:
        cursor.execute(SELECT_ALL_MOVIES)
    else:
        today_timestamp = datetime.datetime.today().timestamp()
        cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))

    return cursor.fetchall()


def get_watched_movies():
    cursor = connection.execute(SELECT_WATCHED_MOVIES)

    return cursor.fetchall()
