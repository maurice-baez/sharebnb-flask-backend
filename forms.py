from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, InputRequired, Email, NumberRange, AnyOf


class ListingAddForm(FlaskForm):
    """Form for adding a new Listing"""

    class Meta:
        csrf = False

    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price_per_night = StringField('Price', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    image_url = StringField('(Optional) Image URL')

class BookingAddForm(FlaskForm):
    """Form for adding a new booking"""

    class Meta:
        csrf = False

    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    listing_id = IntegerField('Listing ID', validators=[DataRequired()])
    guest = StringField('Guest', validators=[DataRequired()])

class MessageForm(FlaskForm):
    """Form for adding/editing messages."""


    class Meta:
        csrf = False

    body = TextAreaField('body', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    class Meta:
        csrf = False

    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class UserEditForm(FlaskForm):
    """Form for editing users."""

    class Meta:
        csrf = False

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    password = PasswordField('Password', validators=[Length(min=6)])
    location = StringField('(Optional) Location')


class LoginForm(FlaskForm):
    """Login form."""

    class Meta:
        csrf = False

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])