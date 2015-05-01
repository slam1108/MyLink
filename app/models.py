from app import db
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

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

	def get_email(self):
		return self.email
		
	def activated(self):
		return self.activate

	def set_password(self, p):
		self.password = generate_password_hash(p)

	def check_password(self, p):
		return check_password_hash(self.password, p)

	def hash_password(self, p):
		return generate_password_hash(p)

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
	wid = db.Column(db.Integer, db.ForeignKey('user.uid'))
	content = db.Column(db.String(140))
	pic = db.Column(db.String(1000))
	posted = db.Column(db.DateTime)

	def __init__(self, writer, wid, content, pic, posted):
		self.writer = writer
		self.wid = wid
		self.content = content
		self.pic = pic
		self.posted = posted

	def __repr__(self):
		return '<Post %r>' % (self.content)

	def get_id(self):
		try:
			return unicode(self.pid)
		except NameError:
			return str(self.pid)

class Request(db.Model):
	rid = db.Column(db.Integer, primary_key=True)
	sender = db.Column(db.Integer, db.ForeignKey('user.uid'))
	receiver = db.Column(db.Integer, db.ForeignKey('user.uid'))
	done = db.Column(db.Boolean)
	connected = db.Column(db.Boolean)
	sent = db.Column(db.Boolean)

	def __repr__(self):
		return '<Request[%s] %r_%r>' % (self.rid, self.sender, self.receiver)

	def __init__(self, sender, receiver, done, connected, sent):
		self.sender = sender
		self.receiver = receiver
		self.done = done
		self.connected = connected
		self.sent = sent;

	def mutual(self):
		self.done = True
		s = Friend(self.sender, self.receiver)
		r = Friend(self.receiver, self.sender)
		db.session.add(s)
		db.session.add(r)
		db.session.commit()

	def getConnected(self):
		return self.connected

	def get_id(self):
		try:
			return unicode(self.rid)
		except NameError:
			return str(self.rid)
	

class Friend(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
	fid = db.Column(db.Integer, db.ForeignKey('user.uid'))
	since = db.Column(db.DateTime)

	def __repr__(self):
		return '<Friend %r>' % (self.id)

	def __init__(self, uid, fid, since):
		self.uid = uid;
		self.fid = fid;
		self.since = since

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

class Circle(db.Model):
	cid = db.Column(db.Integer, primary_key=True)
	owns = db.Column(db.Integer, db.ForeignKey('user.uid'))
	name = db.Column(db.String(100))

	def __repr__(self):
		return '<Circle[%r]:[%s]%s>' % (self.owner, self.cid, self.name)

	def __init__(self, owns, name):
		owns = owns
		name = name

	def get_id(self):
		try:
			return unicode(self.cid)
		except NameError:
			return str(self.cid)


	






