import os

from flask import Flask, request, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from forms import UserAddForm, UserEditForm, LoginForm, MessageForm, ListingAddForm
from models import db, connect_db, User, Listing
from helpers import create_token

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
# Listings routes

@app.get('/listings')
def get_listings():
    search = request.args.get("q")

    print("search=", search)
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
                            user_id="yuribelo")
                            # CHANGE TO DYNAMIC USERID FROM TOKEN
            db.session.commit()

            new_listing.serialize()

            return jsonify(listing=new_listing)

        except IntegrityError:

            return jsonify(error="database error")

    else:
        return jsonify(errors=form.errors)

@app.get("/listings/<int:id>")
def get_listing(id):

    """Get a single listing"""

    listing = Listing.query.get(id).serialize()

    return jsonify(listing=listing)