"""SQLAlchemy models for ShareBnb."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    username = db.Column(
        db.Text,
        primary_key=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False
    )

    last_name = db.Column(
        db.Text,
        nullable=False
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )


    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
        nullable=False
    )

    location = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )


    listings = db.relationship('Listing', cascade='all, delete')

    # messages = db.relationship('Message',
    #                             cascade='all, delete',
    #                             order_by='Message.timestamp.desc()')

    def __repr__(self):
        return f"<User #{self.username}: {self.email}>"


    @classmethod
    def signup(cls, username, first_name, last_name, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Listing(db.Model):
    """Listing in the system."""

    __tablename__ = 'listings'


    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.Text,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    location = db.Column(
        db.Text,
        nullable=False
    )

    price_per_night = db.Column(
        db.Float,
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
        nullable=False
    )

    user_id = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False
    )





def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)