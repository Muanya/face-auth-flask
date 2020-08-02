from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)

login_manager = LoginManager(app)

from app.models import User_Profile

from app import views
