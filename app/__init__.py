from flask import Flask
from models import db

app = Flask(__name__)

app.secret_key = 'mylink_key'
app.config['SQLALCHEMY_DB_DATABASE_URI'] = 'mysql://root:Slam1108!@localhost/mylink'
db.init_app(app)

from app import views
