import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True

# Mail configuration
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'serendibeats@gmail.com'
MAIL_PASSWORD = 'Slam1108!'

# IMG Folder configuration
IMAGE_SRC = '/$HOME/Desktop/CS390/MyLink/app/images'

ADMINS = ['yhong@purdue.edu']