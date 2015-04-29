from app import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
	uid = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(54))
	pic = db.Column(db.String(100))
	activate = db.Column(db.Boolean)

	def __repr__(self):
		return '<User %r>' % (self.firstname)

	def __init__(self, firstname, lastname, email, password, pic, activate):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)
		self.pic = pic
		self.activate = activate

	def activated(self):
		return self.activate

	def set_password(self, p):
		self.password = generate_password_hash(p)

	def check_password(self, p):
		return check_password_hash(self.password, p)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.uid)
		except NameError:
			return str(self.uid)

class Post(db.Model):
	pid = db.Column(db.Integer, primary_key=True)
	writer = db.Column(db.Integer, db.ForeignKey('user.uid'))
	belongs = db.Column(db.Integer, db.ForeignKey('user.uid'))
	content = db.Column(db.String(140))
	posted = db.Column(db.DateTime)

	def __repr__(self):
		return '<Post %r>' % (self.content)


