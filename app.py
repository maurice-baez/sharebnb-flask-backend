import os

from flask import Flask, request, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, UserEditForm, LoginForm, MessageForm, CSRFProtection
from models import db, connect_db, User, Message

CURR_USER_KEY = "curr_user"

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


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.before_request
def add_csrf_form_to_all_pages():
    """Before every route, add CSRF-only form to global object."""

    g.csrf_form = CsrfOnlyForm()


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB.

    If form not valid, throw Error.

    If theres already a user with that username: throw Error
    """

    received = request.json

    form = UserAddForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():

        #try/except here
        newUser = User.signup(received)

        # token = call createToken function

        return jsonify(
            token=token
        )

    else:
        return jsonify(errors=form.errors)



@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""


    received = request.json

    form = LoginForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():

        #try/except here
        user = User.authenticate(received)

        # token = call createToken function

        return jsonify(
            token=token
        )

    else:
        return jsonify(errors=form.errors)


