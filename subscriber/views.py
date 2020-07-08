"""Routes for the UI routes."""

from flask_login import login_required, current_user
from flask import (
    render_template,
    redirect,
    session
)

from .app import app, login
from .models import User


@login.unauthorized_handler
def unauthorized():
    """
    Default redirect when tries to access URL that needs authentication,
    without one.
    """
    return redirect('/')


@app.route('/')
def index():
    """Main route that will ask user to input his email."""
    # If user is already logged in, go to preferences
    if current_user.is_authenticated:
        return redirect('/email_preferences/')
    return render_template('index.html')


@app.route('/verify_code/')
def verify_verification_code():
    """Route to verify code sent through email."""
    # Makes sure user comes after email verification
    if 'email' not in session:
        return redirect('/')
    return render_template("verify.html")


@app.route('/email_preferences/')
@login_required
def email_preferences():
    """Route to update the user's email preferences."""
    email = str(session['email'])
    user = User.query.filter_by(email=email).first()
    return render_template("email_preferences.html", user=user)


@app.route('/success_update/')
@login_required
def preferences_updated():
    """Route to update the user's email preferences."""
    if session['updated']:
        session['updated'] = False
        return render_template("success_update.html")
    return redirect('/')
