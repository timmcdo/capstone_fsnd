import os
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from flask_cors import CORS
from flask_migrate import Migrate
from models import *
from auth import AuthError, requires_auth
from settings import *

def create_app():
    app = Flask(__name__)
    app.debug = True
    setup_db(app)
    # db_drop_and_create_all()

    with app.app_context():
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        db.create_all()

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    migrate = Migrate(app, db, compare_type=True)

    @app.after_request  
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/')
    def home_page():
        return("Hello!")
    
    @app.route('/login', methods=['GET'])
    def login():
        return(redirect(location=LOGIN_LINK))
        
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.order_by(Actor.id).all()

        if len(actors)==0:
            abort(404)

        list = []
        for actor in actors:
            list.append(actor.format())

        return jsonify({
            "success": True,
            "actors": list,
            "number of actors": len(list)
        }), 200

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.order_by(Movie.id).all()

        if len(movies)==0:
            abort(404)
        
        list = []
        for movie in movies:
            list.append(movie.format())

        return jsonify({
            "success": True,
            "movies": list,
            "number of movies": len(movies)
        }), 200
    
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body=request.get_json()
        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')

        try:
            actor = Actor(name=new_name,
                          age=new_age,
                          gender=new_gender)
            actor.insert()

            return jsonify({
                "success":True,
                "new actor": actor.format()
            }), 200

        except Exception as e:
            print(e)
            abort(422)


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body=request.get_json()
        new_title = body.get('title')
        new_release_date = body.get('release_date')

        try:
            movie = Movie(title=new_title,
                          release_date=new_release_date)
            movie.insert()

            return jsonify({
                "success":True,
                "new movie": movie.format()
            }), 200

        except Exception as e:
            print(e)
            abort(422)
    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
         abort(404)

        try:
            actor.delete()
            return jsonify({
                "success": True,
                "deleted": actor.name
            }), 200
        
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
         abort(404)

        try:
            movie.delete()
            return jsonify({
                "success": True,
                "deleted": "Movie " + movie.title + " deleted!"
            }), 200
        
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(payload, movie_id):
        body=request.get_json()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        try:
            if 'title' in body:
                movie.title = body.get("title")
            if 'release_date' in body:
                movie.release_date = body.get("release_date")
                
            movie.update()

            return jsonify({
                "success":True,
                "updated entry": movie.format() 
            }), 200

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(payload, actor_id):
        body=request.get_json()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)
        
        try:
            if 'name' in body:
                actor.name = body.get("name")
            if 'age' in body:
                actor.age = body.get("age")
            if 'gender' in body:
                actor.gender = body.get("gender")

            actor.update()

            return jsonify({
                "success":True,
                "updated entry": actor.format() 
            }), 200

        except Exception as e:
            print(e)
            abort(422)


    @app.errorhandler(401)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 401, 
                "message": "unauthorised"
            }), 401
        )
    
    @app.errorhandler(403)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 403, 
                "message": "permission not found"
            }), 403
        )

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": auth_error.error['description']
        }), auth_error.status_code

    return app


    return app



app = create_app()

if __name__ == '__main__':
    app.run()