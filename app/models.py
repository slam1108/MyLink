from app import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
	uid = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(54))
	pic = db.Column(db.String(100))

	def __repr__(self):
		return '<User %r>' % (self.firstname)

	def __init__(self, firstname, lastname, email, password, pic):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)
		self.pic = pic

	def set_password(self, p):
		self.password = generate_password_hash(p)

	def check_password(self, p):
		return check_password_hash(self.password, p)

class Post(db.Model):
	pid = db.Column(db.Integer, primary_key=True)
	writer = db.Column(db.Integer, db.ForeignKey('user.uid'))
	belongs = db.Column(db.Integer, db.ForeignKey('user.uid'))
	content = db.Column(db.String(140))
	posted = db.Column(db.DateTime)

	def __repr__(self):
		return '<Post %r>' % (self.content)