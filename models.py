from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, Integer, String


db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(Boolean, default=True)
    seeking_des = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venues', lazy='joined', cascade="all, delete")

class Show(db.Model):
    __tablename__ = 'shows'
    id = Column(Integer, primary_key=True)
    start_time = Column(db.DateTime, nullable=False)
    artist_id = Column(Integer, db.ForeignKey('artists.id'))
    venue_id = Column(Integer, db.ForeignKey('venues.id'))


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.String(5))
    seeking_des = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy='joined', cascade="all, delete")