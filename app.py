from flask import Flask, request
from flask_restx import Api, Resource
from model import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

api = Api(app)

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


# End-points router assignation

@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = db.session.query(Movie).all()
        return movies_schema.dump(all_movies), 200


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
