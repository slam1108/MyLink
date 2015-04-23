from flask import Flask

app = Flask(__name__)
#Tell Flask to read it and use it.
app.config.from_object('config')

from app import views
