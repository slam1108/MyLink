import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

app = Flask(__name__)

# database setting
app.config.from_object('config')
db = SQLAlchemy(app)

# login manager & open_id
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
open_id = OpenID(app, os.path.join(basedir, 'tmp'))

app.secret_key = 'mylink_key'

from app import views, models
