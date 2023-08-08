from istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        with open('data.json', "r") as data:
            datamovies = json.load(data)
            movielist = []
            for movie in datamovies:
                movie = {
                    'Title': movie['Title'],
                    'Rating': movie['Rating'],
                    'Year': movie['Year'],
                    'Photo': movie['Photo'],
                    'Plot': movie['Plot'],
                    'IMDB': movie['IMDB']
                }
                movielist.append(movie)
            return movielist

    def add_movie(self, new_movie):
        # add to json file
        file = 'data.json'
        with open(file, "r") as data:
            movies = json.load(data)
            movies.append(new_movie)
            # write te to jason file
        with open(file, 'w') as json_file:
            return json.dump(movies, json_file, indent=4, separators=(',', ': '))

    def check_if_movie_exists(self, movie_title, movie_year):
        file = 'data.json'
        with open(file, "r") as data:
            datamovies = json.load(data)
            movie_list = list(datamovies)
            for movie in movie_list:
                if movie_title in movie['Title'] and movie_year in movie['Year']:
                    return True

    def delete_movie(self, title):
        file = 'data.json'
        with open(file, "r") as data:
            movies = json.load(data)
            for movie in movies:
                if title == movie['Title']:
                    movies.remove(movie)
        with open(file, 'w') as json_file:
            return json.dump(movies, json_file, indent=4, separators=(',', ': '))

    def delete_from_repeated_titles(self, title, year):
        file = 'data.json'
        with open(file, "r") as data:
            movies = json.load(data)
            year = str(year)
            year = year[0:4]
            for movie in movies:
                if title == movie['Title'] and year == movie['Year']:
                    movies.remove(movie)
            movies
        with open(file, 'w') as json_file:
            return json.dump(movies, json_file, indent=4, separators=(',', ': '))

    def update_movie_repeated(self, title, rating, year, plot, old_year):
        file = 'data.json'
        with open(file, "r") as data:
            movies = json.load(data)
            year = str(year)
            year = year[0:4]
            old_year = str(old_year)
            print(old_year)
            for movie in movies:
                if title == movie['Title'] and old_year == movie['Year']:
                    movie['Rating'] = rating
                    movie['Year'] = year
                    movie['Plot'] = plot
        with open(file, 'w') as json_file:
            return json.dump(movies, json_file, indent=4, separators=(',', ': '))

    def update_movie(self, title, rating, year, plot):
        file = 'data.json'
        with open(file, "r") as data:
            movies = json.load(data)
            year = str(year)
            year = year[0:4]
            print(year)
            for movie in movies:
                if title == movie['Title']:
                    movie['Rating'] = rating
                    movie['Year'] = year
                    movie['Plot'] = plot
        with open(file, 'w') as json_file:
            return json.dump(movies, json_file, indent=4, separators=(',', ': '))
