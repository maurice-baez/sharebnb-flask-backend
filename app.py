import os
from telnetlib import STATUS

from flask import Flask, request, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from forms import UserAddForm, UserEditForm, LoginForm, MessageForm, ListingAddForm, BookingAddForm
from models import db, connect_db, User, Listing, Booking, Message
from helpers import create_token, verify_token

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

##############################################################################
# User signup/login/logout

@app.post('/signup')
def signup():
    """Handle user signup.

    Create new user and add to DB.

    If form not valid, throw Error.

    If theres already a user with that username: throw Error
    """

    received = request.json
    #request.forms, request.files
    form = UserAddForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():

        if 'image_url' in received:
            image_url = received['image_url']
        else: image_url = None

        try:
            User.signup(username=received['username'],
                        password=received['password'],
                        first_name=received['first_name'],
                        last_name=received['last_name'],
                        email=received['email'],
                        image_url=image_url)

            db.session.commit()
            token = create_token(received['username'])
            return jsonify(token=token)

        except IntegrityError:
            return jsonify (error="database error")

    else:
        return jsonify(errors=form.errors)



@app.post('/login')
def login():
    """Handle user login."""

    received = request.json

    form = LoginForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():

        user = User.authenticate(username=received['username'],
                    password=received['password'])

        if user:
            token = create_token(received['username'])
            return jsonify(token=token)
        else:
            return jsonify(error="invalid username/password")

    else:
        return jsonify(errors=form.errors)



##############################################################################
# User routes

@app.get('/users')
def get_users():
    """Get list of all users"""

    users = User.query.all()
    serialize = [u.serialize() for u in users]

    return jsonify(users=serialize)

@app.get('/users/<username>')
def get_user_by_id(username):
    """Get a user by username"""

    user = User.query.get(username)
    serialize = user.serialize()

    return jsonify(user=serialize)

@app.get('/users/<username>/messages')
def get_messages_by_user(username):
    """Get list of users messages"""
    ###### use this on users profile to get all messages
    ###### sort by from_user for host, sort by l_id for guest, pass as props to child component

    messages = Message.query.filter(Message.to_user == username).all()
    serialize = [m.serialize() for m in messages]

    return jsonify(messages=serialize)



##############################################################################
# Listings routes

@app.get('/listings')
def get_listings():

    search = request.args.get("q")

    if not search:
        listings = Listing.query.all()
    else:
        listings = Listing.query.filter(or_(Listing.title.like(f"%{search}%"),
                                        Listing.location.like(f"%{search}%"),
                                        Listing.type.like(f"%{search}%"),
                                        Listing.description.like(f"%{search}%")
                                        )).all()

    serialize = [l.serialize() for l in listings]

    return jsonify(listings=serialize)

@app.post('/listings')
def add_listing():

    token = request.headers['token']

    try:
        curr_user = verify_token(token)
    except:
        return jsonify(error= "Unauthorized", status_code= 404)

    received = request.json
    form = ListingAddForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():

        if 'image_url' in received:
            image_url = received['image_url']
        else: image_url = None

        try:
            new_listing = Listing.add_listing(title=received['title'],
                            description=received['description'],
                            location=received['location'],
                            type=received['type'],
                            price_per_night=received['price_per_night'],
                            image_url=image_url,
                            user_id=curr_user['username'])

            db.session.commit()

            serialize = new_listing.serialize()

            return jsonify(listing=serialize)

        except IntegrityError:

            return jsonify(error="database error")

    else:
        return jsonify(errors=form.errors)

@app.get("/listings/<int:id>")
def get_listing(id):

    """Get a single listing"""

    listing = Listing.query.get(id).serialize()

    return jsonify(listing=listing)

@app.get('/listings/<int:id>/messages')
def get_messages_by_listing(id):
    """Get list of listing's messages"""

    token = request.headers['token']

    try:
        verify_token(token)
    except:
        return jsonify(error= "Unauthorized", status_code= 404)

    messages = Message.query.filter(Message.listing_id == id).all()
    serialize = [m.serialize() for m in messages]

    return jsonify(messages=serialize)


@app.post('/listings/<int:id>/messages')
def send_message_by_listing(id):
    """Send a message to a user by listing id"""

    token = request.headers['token']

    try:
        curr_user = verify_token(token)
    except:
        return jsonify(error= "Unauthorized", status_code= 404)

    received = request.json
    form = MessageForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():
        try:
            new_message = Message.add_message(listing_id=id,
                            to_user=received['to_user'],
                            from_user=curr_user['username'],
                            body=received['body'])

            db.session.commit()

            serialize = new_message.serialize()

            return jsonify(message=serialize)

        except IntegrityError:

            return jsonify(error="database error")

    else:
        return jsonify(errors=form.errors)


##############################################################################
# Bookings routes

@app.get('/bookings')
def get_bookings_by_username():

    token = request.headers['token']

    try:
        curr_user = verify_token(token)
    except:
        return jsonify(error= "Unauthorized", status_code= 404)

    bookings = Booking.query.filter(Booking.guest == curr_user['username']).all()

    serialize = [b.serialize() for b in bookings]

    return jsonify(bookings=serialize)

@app.post('/bookings')
def add_booking():

    token = request.headers['token']

    try:
        curr_user = verify_token(token)
    except:
        return jsonify(error= "Unauthorized", status_code= 404)

    received = request.json

    form = BookingAddForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():

        try:
            new_booking = Booking.add_booking(listing_id=received['listing_id'],
                            start_date=received['start_date'],
                            end_date=received['end_date'],
                            host=received['host'],
                            guest=curr_user['username'])

            db.session.commit()

            serialize = new_booking.serialize()

            return jsonify(booking=serialize)

        except IntegrityError:

            return jsonify(error="database error")

    else:
        return jsonify(errors=form.errors)

@app.get("/bookings/<int:id>")
def get_booking(id):
    """Get a single booking"""

    token = request.headers['token']

    try:
        verify_token(token)
    except:
        return jsonify(error= "Unauthorized", status_code= 404)

    booking = Booking.query.get(id).serialize()

    return jsonify(booking=booking)



