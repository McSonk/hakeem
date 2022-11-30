# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 23:09:13 2022

@author: hakee
"""

from flask import Flask, render_template
import psycopg2 
import sqlalchemy
import os
from pdb import set_trace
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask import render_template
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
import pdb
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

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

# FilmActor = db.Table('film_actor',
#   db.Model.metadata,
#   db.Column('actor_id', db.Integer, ForeignKey('Actor.actor_id'), primary_key=True),
#   db.Column('film_id', db.Integer, ForeignKey('Film.film_id'), primary_key=True)
# )

class Film(db.Model):
  __tablename__ = 'film'
  film_id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)

  #actors = relationship('Actor', secondary=FilmActor, backref='Film')


class Actor(db.Model):
  __tablename__ = 'actor'
  actor_id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)

  #films = relationship('Film', secondary=FilmActor, backref='Actor')

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
    films = db.session.execute(
      db.select(Film).order_by(Film.film_id)
    ).scalars()

    test = db.session.execute(
      db.select(FilmActor)
    ).scalars()

    return render_template("actorfilm.html", actorfilm=test)



if __name__ == "__main__":  
    app.run(debug=True)


#no = db.session.query(db.func.count(Film.film_id)).scalar()

#Construct the declarative base object - a base on which we build our database models
#Base = declarative_base()
#Set the database URI
#db_uri = 'postgresql://imperial:ImperialFDT2022@fdt-do-not-delete.ckp3dl3vzxoh.eu-west-2.rds.amazonaws.com/dvdrental'
#Make an engine (our interface to the database)
#engine = create_engine(db)
#(func.count(Film.film_id))

# db = 'postgresql://imperial:ImperialFDT2022@fdt-do-not-delete.ckp3dl3vzxoh.eu-west-2.rds.amazonaws.com/dvdrental'
# #Construct the declarative base object - a base on which we build our database models
# Base = declarative_base()
# #Make an engine (our interface to the database)
# engine = create_engine(db)
# #Make a sessionmaker (construct sessions), then a session (one engine can have many sessions)
# Session = sessionmaker()
# Session.configure(bind=engine)
# session = Session()

#<link rel = "stylesheet" type = "text/css" href = "{{url_for('static', filename = 'style.css')}}">