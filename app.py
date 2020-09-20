import datetime
import database
from typing import List, Tuple

# Movie = (title, release_timestamp, watched)
Movie = Tuple[str, int, int]

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
    release_date = input("Release date (YYYY-mm-dd): ")
    parsed_date = datetime.datetime.strptime(release_date, "%Y-%m-%d")
    # NOTE: Windows won't parse anything before the Unix epoch.
    timestamp = parsed_date.timestamp()

    return (title, timestamp)


def print_movie_list(heading: str, movies: List[Movie]):
    print(f"--- {heading} MOVIES ---")
    for movie in movies:
        movie_date = datetime.datetime.fromtimestamp(movie[1])
        human_date = movie_date.strftime("%Y %b %d")
        print(f"*) {movie[0]} (released: {human_date})")
    print("-----------------------\n")


def prompt_watch_movie() -> str:
    title = input("Enter title of movie watched: ")

    return title


def print_watched(title: str):
    (title, _, watched) = database.get_movie(title)
    print(f"You've now watched \"{title}\" {watched} times.")

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
        title = prompt_watch_movie()
        database.watch_movie(title)
        print_watched(title)

    elif user_input == VIEW_WATCHED:
        movies = database.get_watched_movies()
        print_movie_list("WATCHED", movies)

    else:
        print("Invalid input, please try again!")