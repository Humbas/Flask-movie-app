from termcolor import cprint
import json

API_KEY = 'df0b223c&t'

"""color functions"""


def warning(string):
    return cprint(string, 'red')


def done(string):
    return cprint(string, 'green')


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path, data):
    with open(file_path, "w") as file:
        file.write(data)


def count_movies(movie_list, movie_title):
    return movie_list.count(movie_title)


def count_titles(movie_list, movie_title):
    count = 0
    for element in movie_list:
        if element == movie_title:
            count = count + 1
    return count



