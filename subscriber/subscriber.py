
from flask import Flask, render_template, url_for, request, flash, redirect, session
from forms import SubscribeForm, VerifySubscriptionForm
from flask_mail import Mail, Message
from random import randint


app = Flask(__name__)
app.config['SECRET_KEY'] = '260892c601c030dbc35778a9184e127d'

#Initializing sending-email address information
from_email = "encearthquakenotification@gmail.com"
from_email_password = "kohyomumdlonqmtq"

#Configuring Flask
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = from_email
app.config['MAIL_PASSWORD'] = from_email_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#Initializing Flask-mail
mail = Mail(app)



@app.route("/")
@app.route("/subscribe", methods=['GET', 'POST'])
def subscribe():
	
	form = SubscribeForm()
	
	if form.validate_on_submit():
		
		if request.method == 'POST':
			
			session['email'] = form.email.data
			session['code'] = randint(100000,999999)
		
			with mail.connect() as conn:
				
	
				email = session['email']
				
				messageToSend = "Your verification code: " + str(session['code'])
				subject = "Earthquake Noficiation System Verification Code"
				
				msg = Message(recipients=[email],
							  body=messageToSend,
							  sender = from_email,
							  subject=subject)

				conn.send(msg)
		
		return redirect(url_for("verify"))
		
		
	
	return render_template("subscribe.html", title="Subscribe to Earthquake Alert", form=form)
	
	
	
	
@app.route("/verify", methods=['GET', 'POST'])
def verify():

	if 'email' not in session:
		return redirect(url_for("subscribe"))
	
	form = VerifySubscriptionForm()
	
	if form.validate_on_submit():
		if request.method == 'POST':
			if form.code.data.strip() == str(session['code']):
				#Add to database
				return redirect(url_for("confirmed"))
			else:
				return redirect(url_for("verify"))
	
	return render_template("verify.html", title ="Verify", form=form)
	
	
	
	
@app.route("/confirmed")
def confirmed():
	
	return render_template("confirmed.html", title ="Subscription Confirmed")
	
	
	
	
if __name__ == "__main__":
    app.run()

	
