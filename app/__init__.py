from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='tracktracker.log', level=logging.DEBUG)
# logging.basicConfig(filename='tracktracker.log', level=logging.INFO)

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

admin = Admin(app, template_mode='bootstrap4')

login = LoginManager(app)
login.login_view = 'login'

from app import views, models