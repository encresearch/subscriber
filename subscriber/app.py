"""The main event."""

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from .config import Dev, Prod

app = Flask(__name__)
# TODO change for Prod
app.config.from_object(Dev)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
mail = Mail(app)

from . import api
from . import views
