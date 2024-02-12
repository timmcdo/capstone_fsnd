import os
import unittest
import json
from flask_sqlalchemy import sqlalchemy
from sqlalchemy_utils import database_exists, create_database


from app import create_app
from models import *

DIRECTOR_TOKEN = os.environ.get('DIRECTOR_TOKEN')
ASSISTANT_TOKEN = os.environ.get('ASSISTANT_TOKEN')
PRODUCER_TOKEN = os.environ.get('PRODUCER_TOKEN')
INVALID_TOKEN = os.environ.get('INVALID_TOKEN')

def generate_auth_header(token):
    return {
        'Authorization': 'Bearer ' + token
    }

class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.environ.get("TEST_DB_NAME")
        self.database_path = os.environ.get("TEST_DATABASE_URL")
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            if not database_exists(self.database_path):
                create_database(self.database_path)

            self.db.create_all()

        self.new_actor={
            "name": "Kate Winslet",
            "age": 48, 
            "gender": "female"
        }

        self.new_movie={
            "title": "The Wolf of Wall Street",
            "release_date": "17 January 2014"
        }

        self.edit_actor={
            "age": 50
        }

        self.edit_movie={
            "title": "new_title"
        }

        self.new_actor_bad={
            "title": "something"
        }

        self.new_movie_bad={
            "name": "badness"
        }

    def tearDown(self):
        pass

    def test_api_without_token(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_get_actors(self):
        res = self.client().get("/actors", headers=generate_auth_header(ASSISTANT_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data))
        self.assertTrue(data["actors"])

    def test_get_movies(self):
        res = self.client().get("/movies", headers=generate_auth_header(ASSISTANT_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_add_actor(self):
        res = self.client().post("/actors", headers=generate_auth_header(DIRECTOR_TOKEN), json=self.new_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["new actor"]["name"], "Kate Winslet")
    
    def test_add_movie(self):
        res = self.client().post("/movies", headers=generate_auth_header(PRODUCER_TOKEN), json=self.new_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["new movie"]["title"], "The Wolf of Wall Street")

    def test_delete_actor(self):
        res = self.client().delete("/actors/2", headers=generate_auth_header(DIRECTOR_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], "Kate Winslet")


    def test_delete_movie(self):
        res = self.client().delete("/movies/2", headers=generate_auth_header(PRODUCER_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], "Movie The Wolf of Wall Street deleted!")

    def test_edit_actor(self):
        res = self.client().patch("/actors/1", headers=generate_auth_header(DIRECTOR_TOKEN), json=self.edit_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated entry']['age'], 50)

    def test_edit_movie(self):
        res = self.client().patch("/movies/1", headers=generate_auth_header(DIRECTOR_TOKEN), json=self.edit_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated entry']['title'], "new_title")


    def test_get_actors_error(self):
        res = self.client().put("/actors", headers=generate_auth_header(ASSISTANT_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_movies_error(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_add_actors_error(self):
        res = self.client().post("/actors", headers=generate_auth_header(ASSISTANT_TOKEN), json=self.new_actor_bad)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_add_movies_error(self):
        res = self.client().post("/movies", headers=generate_auth_header(DIRECTOR_TOKEN), json=self.new_movie_bad)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_delete_actor_error(self):
        res = self.client().delete("/actors/10000000000", headers=generate_auth_header(PRODUCER_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_delete_movie_error(self):
        res = self.client().delete("/movies/1", headers=generate_auth_header(DIRECTOR_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_edit_movie_error(self):
        res = self.client().delete("/movies/10000000000", headers=generate_auth_header(PRODUCER_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_edit_actor_error(self):
        res = self.client().delete("/movies/1", headers=generate_auth_header(ASSISTANT_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()