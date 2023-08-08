import json
from datamanager.data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self) -> list:
        """returns a list of users"""
        with open('datamanager/data.json', "r") as data:
            userdata = json.load(data)
            user_list = []
            for user in userdata:
                user = {
                    'id': user['id'],
                    'name': user['name'],
                    'number_of_movies': len(user['movies'])
                }
                user_list.append(user)

            return user_list

    def delete_user(self, user_id) -> dict:
        """deletes user"""
        with open('datamanager/data.json', "r") as data:
            userdata = json.load(data)
            for user in userdata:
                if user['id'] == user_id:
                     userdata.remove(user)
            # write te to jason file
        with open('datamanager/data.json', 'w') as json_file:
            return json.dump(userdata, json_file, indent=4, separators=(',', ': '))


    def get_user_movies(self, user_id) -> dict:
        """returns a list of movies related to the given user"""
        with open('datamanager/data.json', "r") as data:
            userdata = json.load(data)
            for user in userdata:
                if str(user['id']) == user_id:
                    return user['movies']

    def get_user_movie(self, movie_id, user_id) -> dict:
        """returns a dictonary item of a movie"""
        with open('datamanager/data.json', "r") as data:
            userdata = json.load(data)
            for user in userdata:
                id_user = str(user['id'])
                if id_user == user_id:
                    for movie in user['movies']:
                        id_movie = str(movie['id'])
                        if id_movie == movie_id:
                            return movie

    def add_user(self, new_user, user_id) -> dict:
        """adds a user to json list"""
        file = 'datamanager/data.json'
        with open(file, "r") as data:
            users = json.load(data)
            movie_list = []
            new_user = {
                "id": user_id,
                "name": new_user,
                "movies": movie_list
            }
            users.append(new_user)
        # write te to jason file
        with open(file, 'w') as json_file:
            return json.dump(users, json_file, indent=4, separators=(',', ': '))

    def get_user_name(self, user_id) -> str:
        """returns a name string of the given user"""
        with open('datamanager/data.json', "r") as data:
            userdata = json.load(data)
            for user in userdata:
                if str(user['id']) == user_id:
                    return user['name']

    def get_user_id_from_list(self, user_id) -> str:
        """returns a name string of the given user"""
        with open('datamanager/data.json', "r") as data:
            userdata = json.load(data)
            for user in userdata:
                if str(user['id']) == user_id:
                    return user['id']

    def get_user_movies_lenght(self, user_id) -> int:
        """returns an integer that corresponds to the number of movies per given user"""
        with open('datamanager/data.json', "r") as data:
            userdata = json.load(data)
            total_movies = 0
            for user in userdata:
                if str(user['id']) == user_id:
                    total_movies = len(user['movies'])
                    return total_movies

    def check_if_user_id_exists(self, user_id) -> int:
        """returns an boolean, true if user exists, false if does not"""
        with open('datamanager/data.json', "r") as data:
            userdata = json.load(data)
            for user in userdata:
                if user_id in str(user['id']):
                    return str(user['id'])

    def provide_next_id(self) -> int:
        """provides an integer to the user_id key for users"""
        with open('datamanager/data.json', "r") as data:
            userdata = json.load(data)
            max = 0
            next_id = 0
            for user in userdata:
                id = user['id']
                if max < user['id']:
                    max = id
                    next_id = max + 1
            return next_id

    def provide_next_movie_id(self, user_id) -> int:
        """provides an integer to the user_id key for users"""
        with open('datamanager/data.json', "r") as data:
            userdata = json.load(data)
            for user in userdata:
                next_id = 1
                if user_id == user['id']:
                    max_movie = len(user['movies'])
                    next_id = max_movie +1
                    return next_id

    def add_movie(self, new_movie, user_id):
        """adds a movie to current user list"""
        with open('datamanager/data.json', "r") as data:
            userdata = json.load(data)
            for user in userdata:
                if user_id == user['id']:
                    user['movies'].append(new_movie)
        # write te to jason file
        with open('datamanager/data.json', 'w') as json_file:
            return json.dump(userdata, json_file, indent=4, separators=(',', ': '))

    def delete_movie(self, movie_id, user_id):
        """deletes movie from user list"""
        file = 'datamanager/data.json'
        with open(file, "r") as data:
            userdata = json.load(data)
            for user in userdata:
                if user_id == user['id']:
                    for movie in user['movies']:
                          if movie['id'] == movie_id:
                              user['movies'].remove(movie)
        with open(file, 'w') as json_file:
            return json.dump(userdata, json_file, indent=4, separators=(',', ': '))

    def check_if_movie_exists(self, movie_title, user_id):
        """checks is movie already exists in user list"""
        file = 'datamanager/data.json'
        with open(file, "r") as data:
            userdata = json.load(data)
            for user in userdata:
                if user_id == user['id']:
                    for movie in user['movies']:
                        if movie_title in movie['name']:
                            return True

    def update_movie(self, title, rating, year, director, user_id, movie_id):
        file = 'datamanager/data.json'
        with open(file, "r") as data:
            userdata = json.load(data)
            for user in userdata:
                if user_id == user['id']:
                    for movie in user['movies']:
                        if movie['id'] == movie_id:
                            movie['rating'] = rating
                            movie['year'] = year
                            movie['director'] = director
                            movie['name'] = title
        with open(file, 'w') as json_file:
            return json.dump(userdata, json_file, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    pass


