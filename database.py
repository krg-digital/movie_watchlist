# title: string, release_date: timestamp, watched: integer
import datetime
import sqlite3

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    title TEXT UNIQUE,
    release_timestamp REAL
);"""
CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    watcher_name TEXT UNIQUE,
    title TEXT,
    watched_amount INTEGER
);"""

INSERT_MOVIES = """INSERT OR IGNORE INTO movies (
    title, 
    release_timestamp 
) VALUES (?, ?);"""
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"
SELECT_MOVIE = "SELECT * FROM movies WHERE title = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"

INSERT_WATCHER = """INSERT INTO watched (
    watcher_name,
    title,
    watched_amount
) VALUES (?, ?, ?);"""
SELECT_WATCHER = """SELECT * FROM watched WHERE watcher_name = ?;"""
WATCH_MOVIE = "UPDATE watched SET watched_amount = ? WHERE watcher_name = ? AND title = ?;"
SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE watcher_name = ?;"
SELECT_WATCHED_MOVIE = "SELECT * FROM watched WHERE watcher_name = ? AND title = ?;"


connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)

# TODO: validate 'release_timestamp' so that it's valid POSIX time.


def add_movie(title: str, release_timestamp: int):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def watch_movie(username: str, title: str, amount: int = 1):
    current_user = get_user(username)

    with connection:
        cursor = connection.cursor()

        # cursor.execute(DELETE_MOVIE, (title,))

        if not current_user or not any(title in t for t in current_user):
            cursor.execute(INSERT_WATCHER, (username, title, amount))
        else:
            (watcher_name, title, watched_amount) = get_watched_movie(username, title)
            cursor.execute(
                WATCH_MOVIE, (watched_amount + 1, watcher_name, title))


def get_movie(title: str):
    cursor = connection.execute(SELECT_MOVIE, (title,))

    return cursor.fetchone()


def get_movies(upcoming: bool = False):
    cursor = connection.cursor()

    if not upcoming:
        cursor.execute(SELECT_ALL_MOVIES)
    else:
        today_timestamp = datetime.datetime.today().timestamp()
        cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))

    return cursor.fetchall()


def get_watched_movies(username: str):
    with connection:
        cursor = connection.cursor()

        cursor.execute(SELECT_WATCHED_MOVIES, (username,))

        return cursor.fetchall()


def get_watched_movie(username: str, title: str):
    with connection:
        cursor = connection.cursor()

        cursor.execute(SELECT_WATCHED_MOVIE, (username, title))

        return cursor.fetchone()


def get_user(username: str):
    with connection:
        cursor = connection.cursor()

        cursor.execute(SELECT_WATCHER, (username,))

        return cursor.fetchall()
