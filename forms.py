from datetime import datetime
from enum import Enum
import re
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired

class Genre(Enum):
    ALTERNATIVE = 'Alternative'
    BLUES = 'Blues'
    CLASSICAL = 'Classical'
    COUNTRY = 'Country'
    ELECTRONIC = 'Electronic'
    FOLK = 'Folk'
    FUNK = 'Funk'
    HIP_HOP = 'Hip-Hop'
    HEAVY_METAL = 'Heavy Metal'
    INSTRUMENTAL = 'Instrumental'
    JAZZ = 'Jazz'
    MUSICAL_THEATRE = 'Musical Theatre'
    POP = 'Pop'
    PUNK = 'Punk'
    R_AND_B = 'R&B'
    REGGAE = 'Reggae'
    ROCK_N_ROLL = 'Rock n Roll'
    SOUL = 'Soul'
    OTHER = 'Other'

def is_valid_phone(number):
    """ Validate phone numbers like:
    1234567890 - no space
    123.456.7890 - dot separator
    123-456-7890 - dash separator
    123 456 7890 - space separator

    Patterns:
    000 = [0-9]{3}
    0000 = [0-9]{4}
    -.  = ?[-. ]

    Note: (? = optional) - Learn more: https://regex101.com/
    """
    regex = re.compile('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
    return regex.match(number)
state_choice = [
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state_choice
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=[(genre.value, genre.value) for genre in Genre]
    )
    facebook_link = StringField('facebook_link')
    website_link = StringField(
        'website_link'
    )
    phone = StringField(
        'phone'
    )
    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )

    def validate(self):
        if not super().validate():
            return False

        if not is_valid_phone(self.phone.data):
            self.phone.errors.append('Invalid phone number.')
            return False

        if not set(self.genres.data).issubset([genre.value for genre in Genre]):
            self.genres.errors.append('Invalid genres.')
            return False

        if self.state.data not in [choice[0] for choice in self.state.choices]:
            self.state.errors.append('Invalid state.')
            return False

        return True

class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state_choice
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=[(genre.value, genre.value) for genre in Genre]
    )
    facebook_link = StringField('facebook_link')

    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )
    def validate(self):
        if not super().validate():
            return False

        if not is_valid_phone(self.phone.data):
            self.phone.errors.append('Invalid phone number.')
            return False

        if not set(self.genres.data).issubset([genre.value for genre in Genre]):
            self.genres.errors.append('Invalid genres.')
            return False

        if self.state.data not in [choice[0] for choice in self.state.choices]:
            self.state.errors.append('Invalid state.')
            return False

        return True

