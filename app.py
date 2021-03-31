import datetime
import database
from typing import List, Tuple

# Movie = (title, release_timestamp)
Movie = Tuple[str, int]


menu = """Please select one of the following options:
1) Add new movie
2) View upcoming movies
3) View all movies
4) Watch a movie
5) View watched movies
6) Exit

Your selection: """
ADD_MOVIE = '1'
VIEW_UPCOMING = '2'
VIEW_ALL = '3'
WATCH_MOVIE = '4'
VIEW_WATCHED = '5'
EXIT = '6'
welcome = "Welcome to the watchlist app!"


print(welcome)
database.create_tables()


def prompt_add_movie() -> (str, int):
    title = input("Movie title: ")
    release_date = prompt_release_date()

    return (title, release_date)


def print_movie_list(heading: str, movies: List[Movie]):
    print(f"--- {heading} MOVIES ---")
    for (title, release_timestamp) in movies:
        movie_date = datetime.datetime.fromtimestamp(release_timestamp)
        human_readable_date = movie_date.strftime("%Y %b %d")
        print(f"*) {title} (released: {human_readable_date})")
    print("-----------------------\n")


def print_users_watched_movies(username: str, movies: List[Movie]):
    print(f"--- {username}'S WATCHED MOVIES ---")
    for (title, release_timestamp) in movies:
        movie_date = datetime.datetime.fromtimestamp(release_timestamp)
        human_readable_date = movie_date.strftime("%Y %b %d")
        print(f"*) {title} (released: {human_readable_date}")
    print("-----------------------\n")


def prompt_watch_movie() -> (str, str):
    username = input("Username: ")
    title = input("Enter title of movie watched: ")

    return (username, title)


def prompt_release_date() -> (int):
    release_date = input("Release date (YYYY-mm-dd): ")

    parsed_date = datetime.datetime.strptime(release_date, "%Y-%m-%d")
    timestamp = parsed_date.timestamp()

    return timestamp


def print_watched(username: str, title: str):
    (watcher_name, title, watched_amount) = database.get_watched_movie(username, title)
    print(f"{watcher_name} has now watched \"{title}\" {watched_amount} times.")


while (user_input := input(menu)) != EXIT:
    if user_input == ADD_MOVIE:
        (title, release_date) = prompt_add_movie()
        database.add_movie(title, release_date)

    elif user_input == VIEW_UPCOMING:
        movies = database.get_movies(upcoming=True)
        print_movie_list("UPCOMING", movies)

    elif user_input == VIEW_ALL:
        movies = database.get_movies(upcoming=False)
        print_movie_list("ALL", movies)

    elif user_input == WATCH_MOVIE:
        (username, title) = prompt_watch_movie()

        if not database.get_movie(title):
            release_date = prompt_release_date()
            database.add_movie(title, release_date)

        database.watch_movie(username, title)
        print_watched(username, title)

    elif user_input == VIEW_WATCHED:
        username = input("Username: ")
        users_movies = database.get_watched_movies(username)

        movies = []
        for (_, title, _) in users_movies:
            movies.append(database.get_movie(title))

        heading = username.upper() + "'S WATCHED"
        print_movie_list(heading, movies)

    else:
        print("Invalid input, please try again!")
