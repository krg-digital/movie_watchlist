import database

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

while (user_input := input(menu)) != EXIT:
    if user_input == ADD_MOVIE:
        title = input("Movie title: ")
        release_date = input("Release date (YYYY-mm-dd): ")
        database.add_movie(title, release_date)

    elif user_input == VIEW_UPCOMING:
        print(database.get_movies(upcoming=True))

    elif user_input == VIEW_ALL:
        print(database.get_movies(upcoming=False))

    elif user_input == WATCH_MOVIE:
        title = input("Movie title: ")
        database.watch_movie(title)
        (title, _, watched) = database.get_movie(title)
        print(f"You've now watched \"{title}\" {watched} times.")

    elif user_input == VIEW_WATCHED:
        print(database.get_watched_movies())

    else:
        print("Invalid input, please try again!")