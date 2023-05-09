# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy import Column, Boolean, Integer, String
from flask_migrate import Migrate
from flask import abort
from flask import Flask, request, jsonify
import sys
from datetime import datetime
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(Boolean, default=True)
    seeking_des = db.Column(db.String(500))
    shows = db.relationship("Show", backref="venues")


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.String(5))
    seeking_des = db.Column(db.String(500))
    shows = db.relationship("Show", backref="artists")


class Show(db.Model):
    __tablename__ = 'shows'
    id = Column(Integer, primary_key=True)
    start_time = Column(db.DateTime, nullable=False)
    artist_id = Column(Integer, db.ForeignKey('artists.id'))
    venue_id = Column(Integer, db.ForeignKey('venues.id'))

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

with app.app_context():
    db.create_all()
# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


def get_current_time():
    return datetime.now()


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    current_time = datetime.now()
    # query data and group with show table
    venues_query = db.session.query(
        Venue.city,
        Venue.state,
    ).all()

    res = []
    for ct, st in venues_query:
        dt = {
            "city": ct,
            "state": st,
            "venues": []
        }
        current_venues = Venue.query.filter_by(city=ct, state=st).all()
        for venue in current_venues:
            num_upcoming_shows = Show.query.filter(
                Show.start_time > current_time,
                Show.venue_id == venue.id
            ).count()
            venue_data = {
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': num_upcoming_shows
            }
            dt['venues'].append(venue_data)
        res.append(dt)
    return render_template('pages/venues.html', areas=res)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    count = len(results)
    response = {
        "count": count,
        "data": []
    }
    for item in results:
        response["data"].append(item)
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.filter(Venue.id == venue_id).first()
    genres_string = venue.genres
    genres_array = []
    if genres_string is not None:
        genres_array = genres_string.replace("{", "").replace("}", "").split(",")
    res = {
        "id": venue.id,
        "name": venue.name,
        "genres": genres_array,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_des,
        "image_link": venue.image_link,
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }
    current_time = datetime.now()
    for show in venue.shows:
        artist = Artist.query.get(show.artist_id)
        show_data = {
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
        if show.start_time < current_time:
            res["past_shows"].append(show_data)
            res["past_shows_count"] += 1
        else:
            res["upcoming_shows"].append(show_data)
            res["upcoming_shows_count"] += 1
    return render_template('pages/show_venue.html', venue=res)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    body = {}
    name = ""
    try:
        data = request.get_json()
        name = data.get('name')
        venue = Venue()
        for key, value in data.items():
            setattr(venue, key, value)
        if 'seeking_talent' in data and data['seeking_talent'] == 'y':
            venue.seeking_talent = True
        db.session.add(venue)
        db.session.commit()

    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
        body['success'] = False
        body['msg'] = 'error when inser to DB'
        flash('An error occurred. Artist ' + name + ' could not be listed.')
    else:
        flash('artist ' + name + ' was successfully listed!')
        body['msg'] = 'create sucessfully'
        body['success'] = True
        body["name"] = name

    return jsonify(body)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    body = {}
    try:
        venue = Venue.query.get(venue_id)
        if venue:
            db.session.add(venue)
            db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
        body['success'] = False
        body['msg'] = 'error when inser to DB'
        flash('delete error')
    else:
        flash('delete sucessfully')
        body['msg'] = 'delete sucessfully'
        body['success'] = True

    return jsonify(body)

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    count = len(results)
    response = {
        "count": count,
        "data": results
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    genres_string = artist.genres
    genres_array = []
    if genres_string is not None:
        genres_array = genres_string.replace("{", "").replace("}", "").split(",")
    result = {
        "id": artist_id,
        "name": artist.name,
        "genres": genres_array,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone or "326-123-5000",
        "website": artist.website_link or "https://www.gunsnpetalsband.com",
        "facebook_link": artist.facebook_link or "https://www.facebook.com/GunsNPetals",
        "seeking_venue":  artist.seeking_talent,
        "seeking_description": artist.seeking_des or "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": artist.image_link or "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }
    current_time = datetime.now()
    for show in artist.shows:
        venue = Venue.query.get(show.venue_id)
        show_data = {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
        if show.start_time < current_time:
            result["past_shows"].append(show_data)
            result["past_shows_count"] += 1
        else:
            result["upcoming_shows"].append(show_data)
            result["upcoming_shows_count"] += 1

    return render_template('pages/show_artist.html', artist=result)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    for key, value in artist.__dict__.items():
        form_field = getattr(form, key, None)
        if form_field:
            form_field.data = value
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    body = {}
    name = ""
    try:
        artist = Artist.query.get(artist_id)
        data = request.get_json()
        for key, value in data.items():
            if hasattr(artist, key):
                setattr(artist, key, value)
                if key == 'name':
                    name = value
        db.session.commit()

    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
        body['success'] = False
        body['msg'] = 'An error occurred. Artist ' + name + ' could not be updated.'
    else:
        body['success'] = True
        body['msg'] = 'Artist ' + name + ' was successfully updated.'

    return jsonify(body)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    for key, value in venue.__dict__.items():
        form_field = getattr(form, key, None)
        if form_field:
            form_field.data = value
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = False
    body = {}
    name = ""
    try:
        venue = Venue.query.get(venue_id)
        print(venue)
        data = request.get_json()
        for key, value in data.items():
            if hasattr(venue, key):
                if key == 'seeking_talent':
                    setattr(venue, key, value == 'y')
                else:
                    setattr(venue, key, value)
                if key == 'name':
                    name = value
        db.session.commit()

    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
        body['success'] = False
        body['msg'] = 'An error occurred. Venue ' + name + ' could not be updated.'
    else:
        body['success'] = True
        body['msg'] = 'Venue ' + name + ' was successfully updated.'

    return jsonify(body)

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    body = {}
    name = ""
    try:
        data = request.get_json()
        name = data.get('name')
        artist = Artist()
        for key, value in data.items():
            setattr(artist, key, value)
        if 'seeking_venue' in data and data['seeking_venue'] == 'y':
            setattr(artist, "seeking_talent", True)
        else:
            setattr(artist, "seeking_talent", False)
        db.session.add(artist)
        db.session.commit()

    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
        body['success'] = False
        body['msg'] = 'error when inser to DB'
        flash('An error occurred. Artist ' + name + ' could not be listed.')
    else:
        flash('venue ' + name + ' was successfully listed!')
        body['msg'] = 'create sucessfully'
        body['success'] = True
        body["name"] = name

    return jsonify(body)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    current_time = datetime.now()
    shows = db.session.query(Show,     Venue.name.label('venue_name'),
                             Artist.name.label('artist_name'),
                             Artist.image_link.label('artist_image_link')).\
        join(Venue, Show.venue_id == Venue.id).\
        join(Artist, Show.artist_id == Artist.id).\
        filter(Show.start_time > current_time).\
        all()

    res = []
    for show, venue_name, artist_name, artist_image_link in shows:
        data = {
            "venue_id": show.venue_id,
            "venue_name": venue_name,
            "artist_id": show.artist_id,
            "artist_name": artist_name,  
            "artist_image_link": artist_image_link or "https://cdnimg.vietnamplus.vn/t620/uploaded/znaets/2017_10_16/11.jpg",
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%I')
        }
        res.append(data)
    print(res)
    return render_template('pages/shows.html', shows=res)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    body = {}
    try:
        data = request.get_json()
        show = Show()

        venue_id = data.get('venue_id')
        artist_id = data.get('artist_id')
        start_time = data.get('start_time')

        # check missing field
        if not venue_id or not artist_id or not start_time:
            print("vo tren")
            return jsonify({'error': 'Venue ID, Artist ID and Start time are required'}), 400

        # check database if venue_id is valid
        venue = Venue.query.get(venue_id)
        if not venue:
            print("vo duoi")
            return jsonify({'error': 'Invalid Venue ID'}), 400

        # check database if artist_id is valid
        artist = Artist.query.get(artist_id)
        if not artist:
            return jsonify({'error': 'Invalid Artist ID'}), 400
        # check start time must greater than current time
        if start_time:
            current_time = datetime.now()
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        if start_time <= current_time:
            return jsonify({'error': 'Start time must be greater than current time'}), 400

        # add to database
        for key, value in data.items():
            setattr(show, key, value)
        db.session.add(show)
        db.session.commit()

    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
        body['success'] = False
        body['msg'] = 'error when inser to DB'
        flash('An error occurred. show could not be listed.')
    else:
        flash('show was successfully listed!')
        body['msg'] = 'create sucessfully'
        body['success'] = True

    return jsonify(body)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
