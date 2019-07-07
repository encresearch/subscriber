"""Module containing functions pertinent to emails."""

from .app import app, mail
from flask_mail import Message


def send_verification_code(email, code):
    """Send email to user with its verification code."""
    with mail.connect() as conn:
        message = "Your verification code: {code}".format(code=code)
        subject = "Earthquake Notification System Verification Code"
        msg = Message(
            recipients=[email],
            body=message,
            subject=subject
        )
        conn.send(msg)
