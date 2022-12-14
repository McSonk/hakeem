# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 23:09:13 2022

@author: hakee
"""

import psycopg2
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (Column, ForeignKey, Integer, text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

#create the app
app = Flask(__name__)

#create extension
db = SQLAlchemy()
#configure
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://imperial:ImperialFDT2022@fdt-do-not-delete.ckp3dl3vzxoh.eu-west-2.rds.amazonaws.com:5432/dvdrental"
app.config['SQLALCHEMY_ECHO'] = True
#initialize app with extension
db.init_app(app)


connection = psycopg2.connect(host = 'fdt-do-not-delete.ckp3dl3vzxoh.eu-west-2.rds.amazonaws.com',
                       database = 'dvdrental',
                       user = 'imperial',
                       password = 'ImperialFDT2022')

cursor = connection.cursor()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/table')
def tables():
    query1 = "SELECT * FROM actor ORDER BY actor_id;"
    cursor.execute(query1)
    record = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("actors.html", actors = record)


db.Model = declarative_base()

class Film(db.Model):
  __tablename__ = 'film'
  film_id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)

class Actor(db.Model):
  __tablename__ = 'actor'
  actor_id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)

class FilmActor(db.Model):
  __tablename__ = 'film_actor'
  actor_id = Column(Integer, ForeignKey(Actor.actor_id), primary_key=True)
  film_id = Column(Integer, ForeignKey(Film.film_id), primary_key=True)

  actor = relationship('Actor', foreign_keys='FilmActor.actor_id')
  film = relationship('Film', foreign_keys='FilmActor.film_id')


@app.route('/films')
def films():
    film_count = db.session.query(Film.film_id).count()
    films = db.session.execute(db.select(Film).order_by(Film.film_id)).scalars()
    return render_template("filmslist.html", films = films, count = film_count)


@app.route('/allfilms')
def allfilms():
    allfilms = db.session.execute(
      db.select(Film).order_by(Film.film_id)\
    ).scalars()
    return render_template("allfilms.html", allfilms = allfilms)


@app.route('/actorfilm')
def actorfilm():
    query = '''
    SELECT
        actor_id,
        film_id
    FROM (
        SELECT *,
        row_number() OVER (partition by film_id order by film_id) FROM film_actor) temp
    WHERE
        row_number = 1
    LIMIT 10
    '''
    statement = text(query).columns(FilmActor.actor_id, FilmActor.film_id)
    test = db.session.execute(
      db.select(FilmActor).from_statement(statement)
    ).scalars()
    return render_template("actorfilm.html", actorfilm=test)



if __name__ == "__main__":  
    app.run(debug=True)
