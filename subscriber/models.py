"""Database Models using Flask SQLAlchemy as ORM."""

from .app import db


class User(db.Model):
    """User model to keep track of topics that a user is subscribed to.

    Here, each user can choose which topic to subscribe to, depending on the sensors that we have.
    """

    __tablename__ = 'enc_earthquake_email_list'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    verification_code = db.Column(db.Integer, nullable=True, default=None)
    air_chemistry = db.Column(db.Boolean, nullable=False, default=False)
    magnetometer = db.Column(db.Boolean, nullable=False, default=False)
    water_ph = db.Column(db.Boolean, nullable=False, default=False)
    ammeter = db.Column(db.Boolean, nullable=False, default=False)
    tec = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email):
        """We only need the user's email to create a new object."""
        self.email = email

    def is_authenticated(self):
        """Set user auth through Flask Login."""
        return True

    def is_active(self):
        """Set up for Flask Login."""
        return True

    def is_anonymous(self):
        """Prevent anonymous users for Flask Login."""
        return False

    def get_id(self):
        """Get the user_id for user authentication (login)."""
        return str(self.user_id)

    def get_or_create(email):
        """If given user email doesn't exist, create it."""
        if User.query.filter_by(email=email).first() is not None:
            return User.query.filter_by(email=email).first()
        new_user = User(email)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def generate_verification_code(self):
        """Generate random verification code for the user."""
        from random import randint
        self.verification_code = randint(100000, 999999)
        db.session.commit()
        return self.verification_code

    def verify_code(self, verification_code):
        """Verify inputted verification code."""
        return verification_code == self.verification_code
