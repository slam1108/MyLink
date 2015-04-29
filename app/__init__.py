import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir
from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
csrf.init_app(app)

# database setting
app.config.from_object('config')
db = SQLAlchemy(app)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.secret_key = 'mylink_key'

from flask.ext.mail import Mail
mail = Mail(app)

from app import views, models
