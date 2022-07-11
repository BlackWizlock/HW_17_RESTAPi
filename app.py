from flask import Flask, request
from flask_restx import Api, Resource
from flask_restx.representations import output_json
from model import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

api = Api(app, description='База данных для хранения фильмов')
api.representations = {'application/json; charset=utf-8': output_json}

movie_ns = api.namespace('movies', description='Вьюшки для фильмов')
director_ns = api.namespace('directors', description='Вьюшки для режисеров')
genre_ns = api.namespace('genres', description='Вьюшки для жанров')


# End-points router assignation

@movie_ns.route('/')
@movie_ns.param('director_id', 'ID Директора')
@movie_ns.param('genre_id', 'ID Жанра')
class MoviesView(Resource):
    @movie_ns.doc(description='Гет для фильмов')
    @movie_ns.response(200, 'Success')
    @movie_ns.response(204, 'Not found')
    @movie_ns.response(400, 'Error')
    def get(self):
        director_id = request.args.get('director_id', type=int)
        genre_id = request.args.get('genre_id', type=int)
        if director_id and genre_id:
            directors_genres = db.session \
                .query(Movie) \
                .filter(Movie.director_id == director_id, Movie.genre_id == genre_id) \
                .all()
            if not directors_genres:
                return f"No movies found with the director_id: {director_id}" \
                       f" and the genre_id: {genre_id}", 204
            else:
                return movies_schema.dump(directors_genres), 200

        if director_id:
            directors = db.session \
                .query(Movie) \
                .filter(Movie.director_id == director_id) \
                .all()
            return movies_schema.dump(directors), 200
        if genre_id:
            genres = db.session \
                .query(Movie) \
                .filter(Movie.genre_id == genre_id) \
                .all()
            return movies_schema.dump(genres), 200
        movies = db.session.query(Movie).all()
        # Respond with the movies with the specified director_id and genre_id if found
        return movies_schema.dump(movies), 200


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid: int):
        try:
            movie = db.session \
                .query(Movie) \
                .filter(Movie.id == uid) \
                .one()
            return movie_schema.dump(movie), 200
        except Exception:
            return '', 404


@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        directors = db.session \
            .query(Director) \
            .all()
        return directors_schema.dump(directors), 200


@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid: int):
        try:
            director = db.session \
                .query(Director) \
                .filter(Director.id == uid) \
                .one()
            return director_schema.dump(director), 200
        except Exception:
            return '', 404


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        genres = db.session \
            .query(Genre) \
            .all()
        return genres_schema.dump(genres), 200


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid: int):
        try:
            genre = db.session \
                .query(Genre) \
                .filter(Genre.id == uid) \
                .one()
            return genre_schema.dump(genre), 200
        except Exception:
            return '', 404


if __name__ == '__main__':
    app.run()
