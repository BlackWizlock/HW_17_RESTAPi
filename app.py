from flask import Flask, request
from flask_restx import Api, Resource
from flask_restx.representations import output_json
from model import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

api = Api(app, docs='/', description='База данных для хранения фильмов')
api.representations = {'application/json; charset=utf-8': output_json}

movie_ns = api.namespace('movies', description='Вьюшки для фильмов')
director_ns = api.namespace('directors', description='Вьюшки для директоров')
genre_ns = api.namespace('genres', description='Вьюшки для жанров')


# End-points router assignation

@movie_ns.route('/')
class MoviesView(Resource):
    @movie_ns.param('director_id', 'ID Директора')
    @movie_ns.param('genre_id', 'ID Жанра')
    @movie_ns.doc(description='[Movie] Database methods get')
    def get(self):

        director_id = request.args.get('director_id', type=int)
        genre_id = request.args.get('genre_id', type=int)
        if director_id and genre_id:
            directors_genres = db.session \
                .query(Movie.id,
                       Movie.title,
                       Movie.description,
                       Movie.trailer,
                       Movie.rating) \
                .filter(Movie.director_id == director_id, Movie.genre_id == genre_id) \
                .all()
            if not directors_genres:
                return f"Not found", 204
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
        return movies_schema.dump(movies), 200

    @movie_ns.doc(description='[Movie] Database methods post')
    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return new_movie, 201


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    @movie_ns.doc(description='[Movie] Database methods get by uid')
    def get(self, uid: int):
        try:
            movie = db.session \
                .query(Movie) \
                .filter(Movie.id == uid) \
                .one()
            return movie_schema.dump(movie), 200
        except Exception:
            return '', 404

    @movie_ns.doc(description='[Movie] Database methods put by uid')
    def put(self, uid: int):
        try:
            movie = Movie.query.get(uid)
            req_json = request.json

            movie.id = req_json.get("id")
            movie.title = req_json.get("title")
            movie.description = req_json.get("description")
            movie.trailer = req_json.get("trailer")
            movie.year = req_json.get("year")
            movie.rating = req_json.get("rating")
            movie.genre_id = req_json.get("genre_id")
            movie.director_id = req_json.get("director_id")

            db.session.add(movie)
            db.session.commit()
            return "", 204
        except Exception:
            return '', 404

    @movie_ns.doc(description='[Movie] Database methods delete by uid')
    def delete(self, uid: int):
        try:
            movie = Movie.query.get(uid)
            db.session.delete(movie)
            db.session.commit()
            return "", 204
        except Exception:
            return '', 404


@director_ns.route('/')
class DirectorView(Resource):
    @director_ns.doc(description='[Director] Database methods get')
    def get(self):
        directors = db.session \
            .query(Director) \
            .all()
        return directors_schema.dump(directors), 200

    @director_ns.doc(description='[Director] Database methods post')
    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return new_director, 201


@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    @director_ns.doc(description='[Director] Database methods get by uid')
    def get(self, uid: int):
        try:
            director = db.session \
                .query(Director) \
                .filter(Director.id == uid) \
                .one()
            return director_schema.dump(director), 200
        except Exception:
            return '', 404

    @director_ns.doc(description='[Director] Database methods put by uid')
    def put(self, uid: int):
        try:
            director = Director.query.get(uid)
            req_json = request.json

            director.id = req_json.get("id")
            director.name = req_json.get("name")

            db.session.add(director)
            db.session.commit()
            return "", 204
        except Exception:
            return '', 404

    @director_ns.doc(description='[Director] Database methods delete by uid')
    def delete(self, uid: int):
        try:
            director = Director.query.get(uid)
            db.session.delete(director)
            db.session.commit()
            return "", 204
        except Exception:
            return '', 404


@genre_ns.route('/')
class GenreView(Resource):
    @genre_ns.doc(description='[Genre] Database methods get')
    def get(self):
        genres = db.session \
            .query(Genre) \
            .all()
        return genres_schema.dump(genres), 200

    @genre_ns.doc(description='[Genre] Database methods post')
    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return new_genre, 201


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    @genre_ns.doc(description='[Genre] Database methods get by uid')
    def get(self, uid: int):
        try:
            genre = db.session \
                .query(Genre) \
                .filter(Genre.id == uid) \
                .one()
            return genre_schema.dump(genre), 200
        except Exception:
            return '', 404

    @genre_ns.doc(description='[Genre] Database methods put by uid')
    def put(self, uid: int):
        try:
            genre = Genre.query.get(uid)
            req_json = request.json

            genre.id = req_json.get("id")
            genre.name = req_json.get("name")

            db.session.add(genre)
            db.session.commit()
            return "", 204
        except Exception:
            return '', 404

    @genre_ns.doc(description='[Genre] Database methods delete by uid')
    def delete(self, uid: int):
        try:
            genre = Genre.query.get(uid)
            db.session.delete(genre)
            db.session.commit()
            return "", 204
        except Exception:
            return '', 404


if __name__ == '__main__':
    app.run()
