from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
from datamanager import accessory_functions
import requests

data_manager = JSONDataManager('data.json')

app = Flask(__name__)


@app.route('/')
def home():
    """shows movie users"""
    users = data_manager.get_all_users()
    users_length = len(users)
    return render_template('users.html', users=users, users_length=users_length)


@app.route('/users', methods=['GET'])
def list_users():
    """shows movie users"""
    users = data_manager.get_all_users()
    users_length = len(users)
    return render_template('users.html', users=users, users_length=users_length)


@app.route('/users/<user_id>', methods=['GET', 'POST'])
def user_movies(user_id):
    """shows movie list by user"""
    movies = data_manager.get_user_movies(user_id)
    user = data_manager.get_user_name(user_id)
    number_movies = data_manager.get_user_movies_lenght(user_id)
    list_id_users = []
    for datauser in data_manager.get_all_users():
        list_id_users.append(str(datauser['id']))
    if user_id not in list_id_users:
        return render_template('404.html'), 404
    else:
        if number_movies > 0:
            message = 'You may update or delete any of the movies by using the links at the left'
        else:
            message = ''
        if data_manager.check_if_user_id_exists(user_id):
            return render_template('movies.html', movies=movies, user=user, number_movies=number_movies,
                                   user_id=user_id, message=message)
        else:
            return render_template('404.html'), 404


@app.route('/users/delete_user/<user_id>', methods=['GET'])
def delete_user(user_id):
    """deletes user and its movie list"""
    if request.method == 'GET':
        if data_manager.check_if_user_id_exists(user_id) is None:
            return render_template('404.html'), 404
        data_manager.delete_user(int(user_id))
        return redirect(url_for('list_users'))
    return render_template('users.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """adds user"""
    if request.method == 'POST':
        username = request.form.get('username')
        user_id = data_manager.provide_next_id()
        data_manager.add_user(username, user_id)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """adds movie to current user list"""
    message = 'Please write a movie name'
    user = data_manager.get_user_name(user_id)
    # check how many movies current user has
    number_movies = data_manager.get_user_movies_lenght(user_id)
    # get user movies
    movies = data_manager.get_user_movies(user_id)
    user_id = data_manager.get_user_id_from_list(user_id)
    if request.method == 'POST':
        form_user_id = request.form.get('user_id')
        movie_name = request.form.get('movie_name')
        url_movie = f'https://omdbapi.com/?apikey={accessory_functions.API_KEY}&s={movie_name}'
        data = requests.get(url_movie)
        data.raise_for_status()
        response = requests.get(url_movie).json()
        if response['Response'] == 'False':
            message = 'Please write a valid movie name'
            return render_template('add_movie.html', user=user, user_id=form_user_id, message=message,
                                   number_movies=number_movies, movies=movies)

        else:
            for movie in response['Search']:
                year = movie['Year']
                name = movie['Title']
                movie_id = movie['imdbID']
                """using another dict to access more movie data"""
                more_movie_data = f'http://www.omdbapi.com/?apikey={accessory_functions.API_KEY}&i={movie_id}&plot=short&r=json'
                movie_data_dict = requests.get(more_movie_data).json()
                director = movie_data_dict['Director']
                rating = movie_data_dict['imdbRating']
                id = data_manager.provide_next_movie_id(user_id)
                year = year[0:4]
                # dealing with rating value constrains
                if rating != 'N/A':
                    rating = float(rating)
                else:
                    rating = str(rating)
                result = {
                    'id': id,
                    'name': name,
                    'director': director,
                    'year': int(year),
                    'rating': rating
                }
            if data_manager.check_if_movie_exists(name, user_id):
                message = f'{name} already exists in this list'
            else:
                data_manager.add_movie(result, user_id)
                return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html', user=user, movies=movies, user_id=user_id, message=message,
                           number_movies=number_movies)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(movie_id, user_id):
    """ updates movie by post method"""
    message = 'Please edit the following movie:'
    user = data_manager.get_user_name(user_id)
    number_movies = data_manager.get_user_movies_lenght(user_id)
    movies = data_manager.get_user_movies(user_id)
    movie_to_edit = data_manager.get_user_movie(movie_id, user_id)
    if movie_to_edit is None:
        return render_template('movie_not_found.html'), 404
    else:
        # by having these variables we ensure that the form has always elements even if the user does not make input
        name = movie_to_edit['name']
        director = movie_to_edit['director']
        year = int(movie_to_edit['year'])
        rating = movie_to_edit['rating']
        # dealing with rating value constrains
        if rating != 'N/A':
            rating = float(rating)
        else:
            rating = str(rating)
        if request.method == 'POST':
            name = request.form.get('movie_name')
            director = request.form.get('movie_director')
            year = request.form.get('movie_year')
            rating = request.form.get('movie_rating')
            data_manager.update_movie(name, rating, int(year), director, int(user_id), int(movie_id))
            return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', user=user, movie_name=name, movies=movies, movie_director=director,
                           movie_rating=rating, movie_year=year, user_id=user_id, message=message,
                           number_movies=number_movies, movie_id=movie_id)


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET'])
def delete_movie(movie_id, user_id):
    movie_to_delete = data_manager.get_user_movie(movie_id, user_id)
    user = data_manager.get_user_name(user_id)
    number_movies = data_manager.get_user_movies_lenght(user_id)
    movies = data_manager.get_user_movies(user_id)
    if number_movies > 0:
        message = 'hey, do you wish to delete a movie?'
    else:
        message = ''
    if movie_to_delete is None:
        return render_template('movie_not_found.html'), 404
    else:
        if request.method == 'GET':
            data_manager.delete_movie(int(movie_id), int(user_id))
            return redirect(url_for('user_movies', user_id=user_id))
    return render_template('delete_movie.html', movies=movies, user=user, number_movies=number_movies, user_id=user_id,
                           message=message)


if __name__ == '__main__':
    app.run(debug=True)
