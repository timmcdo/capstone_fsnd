import os
from sqlalchemy import Column, String, Integer, Enum, create_engine
from flask_sqlalchemy import SQLAlchemy, functools
import json
import sys
import dateutil.parser
import babel
from settings import *

DB_NAME = os.environ.get("DB_NAME")
database_path = os.environ.get('DATABASE_URL')

if database_path is None:
    database_path = "postgresql://postgres:postgres@localhost:5432/capstone"

db = SQLAlchemy()

genders = ('male', 'female', 'non-binary', 'other', 'prefer not to say')

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    actor = Actor(
        name='Leonardo DiCaprio',
        age=49,
        gender='male'
    )
    actor.insert()
    movie = Movie(
        title='Titanic',
        release_date='17 December 1999'
        )
    movie.insert()

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    release_date = db.Column(db.DateTime)

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release date': self.release_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    age =  db.Column(db.Integer)
    gender = db.Column(db.Enum(*genders, name='genders'))

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    



