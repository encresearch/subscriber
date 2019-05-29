from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email, Length 
from wtforms.fields.html5 import EmailField

class SubscribeForm(FlaskForm):
	email = EmailField('Email: ', validators=[InputRequired(), Email("This Field Requires an Email Address")])
	
	submit = SubmitField('Send Code')
	

class VerifySubscriptionForm(FlaskForm):
	code = StringField('Code: ', validators=[InputRequired()])
	
	submit = SubmitField('Verify')