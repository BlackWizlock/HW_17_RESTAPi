from flask import Flask, request
from flask_restx import Api, Resource
from flask_restx.representations import output_json
from model import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

api = Api(app)
api.representations = {'application/json; charset=utf-8': output_json}

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


# End-points router assignation

@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        # Get arguments from request
        director_id = request.args.get('director_id', type=int)
        genre_id = request.args.get('genre_id', type=int)

        # Respond with the movies with the specified director_id and genre_id if found
        if director_id and genre_id:
            movies_found = db.session \
                .query(Movie.id,
                       Movie.title,
                       Movie.description,
                       Movie.trailer,
                       Movie.rating,
                       Genre.name.label('genre'),
                       Director.name.label('director')) \
                .join(Movie.genre) \
                .join(Movie.director) \
                .filter(Movie.genre_id == genre_id, Movie.director_id == director_id) \
                .all()
            if not movies_found:
                return f"No movies found with the director_id: {director_id}" \
                       f" and the genre_id: {genre_id}", 204
            else:
                return movies_schema.dump(movies_found), 200

        # Respond with the movies with the specified director_id if found
        if director_id:
            movies_found = db.session \
                .query(Movie.id,
                       Movie.title,
                       Movie.description,
                       Movie.trailer,
                       Movie.rating,
                       Genre.name.label('genre'),
                       Director.name.label('director')) \
                .join(Movie.genre) \
                .join(Movie.director) \
                .filter(Movie.director_id == director_id) \
                .all()
            if not movies_found:
                return f"No movies found with the director_id: {director_id}", 204
            else:
                return movies_schema.dump(movies_found), 200

        # Respond with the movies with the specified genre_id if found
        if genre_id:
            movies_found = db.session \
                .query(Movie.id,
                       Movie.title,
                       Movie.description,
                       Movie.trailer,
                       Movie.rating,
                       Genre.name.label('genre'),
                       Director.name.label('director')) \
                .join(Movie.genre) \
                .join(Movie.director) \
                .filter(Movie.genre_id == genre_id) \
                .all()
            if not movies_found:
                return f"No movies found with the genre_id: {genre_id}", 204
            else:
                return movies_schema.dump(movies_found), 200

        # Respond with all the movies if no arguments passed
        else:
            movies_all = db.session \
                .query(Movie.id,
                       Movie.title,
                       Movie.description,
                       Movie.trailer,
                       Movie.rating,
                       Genre.name.label('genre'),
                       Director.name.label('director')) \
                .join(Movie.genre) \
                .join(Movie.director) \
                .all()
            return movies_schema.dump(movies_all), 200


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.id == uid).one()
            return movie_schema.dump(movie), 200
        except Exception:
            return '', 404


@director_ns.route('/')
class DirectorView(Resource):
    pass


@genre_ns.route('/')
class GenreView(Resource):
    pass


if __name__ == '__main__':
    app.run()
