"""This file handle user authentications."""
from flask import request, redirect, flash, session
from flask_restful import Resource
from flask_login import (
    login_user,
    logout_user,
    login_required,
)

from .app import (
    app,
    api,
    login,
    db
)
from . utils import email_exists
from .models import User
from .mail import send_verification_code


@login.user_loader
def load_user(user_id):
    """This extension expects that the application will
     configure a user loader function, that can be called to
     load a user given the ID.

      Each time the logged-in user navigates to a new page,
      Flask-Login retrieves the ID of the user from the session,
      and then loads that user into memory.

      The id that Flask-Login passes to the function as an
      argument is going to be a string, so a proper conversion
      is needed."""
    try:
        return User.query.get(int(user_id))
    except:
        return None


class VerifyEmail(Resource):
    """Endpoint to verify the input email corresponds to a Grafana user."""

    def post(self):
        """Email validation."""
        email = str(request.form['email'])  # Get PIN from form
        if not email_exists(email):  # Validate PIN
            return "email does not exist."
        user = User.get_or_create(email)
        verification_code = user.generate_verification_code()
        session['email'] = email
        send_verification_code(email=email, code=verification_code)
        return redirect('/verify_code/')
api.add_resource(VerifyEmail, '/api/auth/verify_email/', endpoint='verify_email')


class VerifyCode(Resource):
    """API Endpoint to verify the code sent to the user's email."""

    def post(self):
        """Verification code validation."""
        code = int(request.form['verification_code'])
        if session['email']:
            email = session['email']
            user = User.query.filter_by(email=email).first()
            if user.verify_code(verification_code=code):
                login_user(user)
                return redirect('/email_preferences/')
            return "Wrong Code, please try again later."
        return redirect('/')
api.add_resource(VerifyCode, '/api/auth/verify_code/', endpoint='verify_code')


class UpdateEmailPreferences(Resource):
    """Endpoint to update the notification topics the user wants."""

    def post(self):
        """Update email preferences based on HTML check-box."""
        if session['email']:
            email = session['email']
            user = User.query.filter_by(email=email).first()

            user.air_chemistry = (
                True if request.form.get('air_chemistry')
                else False
            )
            user.magnetometer = (
                True if request.form.get('magnetometer')
                else False
            )
            user.water_ph = (
                True if request.form.get('water_ph')
                else False
            )
            user.ammeter = (
                True if request.form.get('ammeter')
                else False
            )
            user.tec = (
                True if request.form.get('tec')
                else False
            )
            db.session.add(user)
            db.session.commit()
            session['updated'] = True
        return redirect('/success_update/')
api.add_resource(UpdateEmailPreferences, '/api/auth/update_email_preferences/', endpoint='update')


class LogOut(Resource):
    """Endpoint to LogOut the user."""

    method_decorators = [login_required]

    def get(self):
        """Simple get request to logout."""
        logout_user()
        return redirect('/')
api.add_resource(LogOut, '/api/auth/logout/', endpoint='logout')
