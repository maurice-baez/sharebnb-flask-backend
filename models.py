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

    bookings = db.relationship('Booking', cascade='all, delete')

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

    type = db.Column(
        db.Text,
        nullable=False
    )

    price_per_night = db.Column(
        db.Text,
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

    def __repr__(self):
        return f"<Listing #{self.id}, {self.title}, {self.description}, {self.location}, {self.type}, {self.price_per_night}, {self.image_url}, {self.user_id}>"

    @classmethod
    def add_listing(cls, title, description, location, type, price_per_night, image_url, user_id):
        """Add a new listing to database """

        listing = Listing(
            title=title,
            description=description,
            location=location,
            type=type,
            price_per_night=price_per_night,
            image_url=image_url,
            user_id=user_id
        )

        db.session.add(listing)

        return listing

    def serialize(self):
        """ Serialize to dictionary """

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "type": self.type,
            "pricePerNight": self.price_per_night,
            "imageUrl": self.image_url,
            "userId": self.user_id
        }


class Booking(db.Model):
    """booking in the system."""

    __tablename__ = 'bookings'


    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    listing_id= db.Column(
        db.Integer,
        db.ForeignKey('listings.id', ondelete='CASCADE'),
        nullable=False,
    )

    start_date = db.Column(
        db.Text,
        nullable=False
    )

    end_date = db.Column(
        db.Text,
        nullable=False
    )

    host = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False
    )

    guest = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False
    )

    def __repr__(self):
        return f"<Listing #{self.id},Listing id: {self.listing_id}, Host: {self.host}, Guest: {self.guest}>"

    @classmethod
    def add_booking(cls, listing_id, start_date, end_date, host, guest):
        """Add a new booking to database """

        booking = Booking(
            listing_id=listing_id,
            start_date=start_date,
            end_date=end_date,
            host=host,
            guest=guest
        )

        db.session.add(booking)

        return booking

    def serialize(self):
        """ Serialize to dictionary """

        return {
            "id": self.id,
            "listingId": self.listing_id,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "host": self.host,
            "guest": self.guest
        }


class Message(db.Model):
    """Message in the system."""

    __tablename__ = 'messages'


    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id', ondelete='CASCADE'),
        nullable=False,
    )

    to_user = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False
    )

    from_user = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False
    )

    body = db.Column(
        db.Text,
        nullable=False
    )


    def __repr__(self):
        return f"<Message #{self.id},Listing id: {self.listing_id}, To: {self.to_user}, From: {self.from_user}, Message: {self.body}>"

    @classmethod
    def add_message(cls, listing_id, to_user, from_user, body):
        """Add a new message to database """

        message = Message(
            listing_id=listing_id,
            to_user=to_user,
            from_user=from_user,
            body=body
        )

        db.session.add(message)

        return message

    def serialize(self):
        """ Serialize to dictionary """

        return {
            "id": self.id,
            "listingId": self.listing_id,
            "fromUser": self.from_user,
            "toUser": self.to_user,
            "body": self.body
        }


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)