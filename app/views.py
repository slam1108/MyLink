from app import app, db, login_manager, service, csrf, os
from flask import flash, render_template, request, session, redirect, url_for, g, send_from_directory
from models import User, Post, Request, Friend, Circle, CircleItem
from forms import LoginForm, RegisterForm, EditForm, ProfileForm, PostForm, CircleForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_wtf.csrf import CsrfProtect
from werkzeug import secure_filename
from config import IMAGE_SRC, ALLOWED_EXTENSIONS
from datetime import datetime
from sqlalchemy import func

CsrfProtect(app)

# route for handling home page
@app.route('/')
@app.route('/intro')
@csrf.exempt
def intro():
    if g.user is None or g.user.is_authenticated() == False:
    	return render_template('intro.html')
    return redirect(url_for('newsfeed', wid=g.user.uid))

# loads a user from the database
@login_manager.user_loader
def load_user(uid):
	return User.query.get(int(uid))

@app.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('intro'))
	form = LoginForm()
	error = None
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		email = form.email.data
		password = form.password.data

		user = User.query.filter_by(email=email).first()
		if user is None:
			flash('You are not registered. Please register first.')
		elif not user.check_password(password):
			flash('Incorrect password. Please check again.')
		elif user.activated() == False:
			service.send_activate(user)
			return render_template('welcome.html')
		else:
			session['user_id'] = user.uid
			remember_me = False
			if 'remember_me' in session:
				remember_me = session['remember_me']
				session.pop('remember_me', None)
			login_user(user, remember = remember_me)
			form = PostForm()
			return redirect(request.args.get('next') or url_for('intro'))
	return render_template('login.html', title='Register', error=error, form=form)


@app.route('/activate_account/<int:uid>')
@csrf.exempt
def activate_account(uid):
	user = User.query.filter_by(uid=uid).first()
	db.session.query(User).filter_by(uid=uid).update({"activate":True})

	users = db.session.query(User).filter(User.uid!=uid).all()
	
	# make connection with other users
	for u in users:
		r0 = Request(sender=uid, receiver=u.uid, done=False, connected=False, sent=False)
		r1 = Request(sender=u.uid, receiver=uid, done=False, connected=False, sent=False)
		db.session.add(r0)
		db.session.add(r1)

	db.session.commit()
	return render_template('activate.html')


@app.route('/logout')
@csrf.exempt
def logout():
    logout_user()
    return redirect(url_for('intro'))

# current_user global is set by flask_login
@app.before_request
def before_request():
	g.user = current_user


@app.route('/register', methods=['GET','POST'])
@csrf.exempt
def register():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('intro'))
	form = RegisterForm()
	error = None
	if form.validate_on_submit():
		firstname = form.firstname.data
		lastname = form.lastname.data
		email = form.email.data.lower()
		password = form.password.data
		confirm_password = form.confirm_password.data
		activate = False
		pic = '';

		user = User.query.filter_by(email=email).first()
		if '@' not in email or '.' not in email:
			flash('Invalid email. Please try again.')
		elif User.query.filter_by(email=email).first() is not None:
			flash('Email is already registered.')
		elif password != confirm_password:
			flash('Please check confirm password')
		else:
			user = User(firstname=firstname, lastname=lastname, email=email,
						password=password, pic=pic, activate=activate)
			db.session.add(user);
			db.session.commit()
			service.send_activate(user)
			return render_template('welcome.html')
	return render_template('register.html', title='Register', form=form)

@app.route('/profile', methods=['GET','POST'])
@login_required
@csrf.exempt
def profile():
	form = ProfileForm()
	#print 'fuck'
	if form.validate_on_submit():
		if request.method == 'POST':
			file = request.files['file']
			#print file
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				#print 'filename'+filename
				file.save(os.path.join(IMAGE_SRC, filename))
				#path = '/static/'+filename
				#print 'path'+path
				db.session.query(User).filter_by(uid=g.user.uid).update({"pic":filename})
				db.session.commit()
				#print '#######################'+g.user.pic
				return redirect(url_for('profile'))
			else:
				db.session.query(User).filter_by(uid=g.user.uid).update({"pic":''})
				db.session.commit()
				return redirect(url_for('profile'))

	return render_template('profile.html', user=g.user, form=form)

def allowed_file(filename):
	return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/<filename>', methods = ['GET', 'POST'])
@login_required
def upload_file(filename):
	return send_from_directory(IMAGE_SRC, filename)

@app.route('/edit', methods=['GET','POST'])
@login_required
@csrf.exempt
def edit():
	form = EditForm()
	error = None
	if form.validate_on_submit():
		firstname = form.firstname.data
		lastname = form.lastname.data
		password = form.password.data
		new_password = form.new_password.data
		confirm_password = form.confirm_password.data

		if not g.user.check_password(password):
			flash("Wrong password.")
		elif new_password != confirm_password:
			flash("Please check confirm password")
		else :
			db.session.query(User).filter_by(uid=g.user.uid).update({"firstname":firstname})
			db.session.query(User).filter_by(uid=g.user.uid).update({"lastname":lastname})
			db.session.query(User).filter_by(uid=g.user.uid).update({"password":g.user.hash_password(new_password)})
			db.session.commit()
			return redirect(url_for('profile'))
	return render_template('edit.html', form=form)

@app.route('/wall', methods=['GET','POST'])
@app.route('/wall/<wid>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def wall(wid):
	form = PostForm()
	error = None
	pic = ''
	#print '***************************************'
	if form.validate_on_submit():
		content = form.content.data
		posted = datetime.utcnow()
		if request.method == 'POST':
			file = request.files['file']
			#print 'request'
			if file and allowed_file(file.filename):
				pic = secure_filename(file.filename)
				file.save(os.path.join(IMAGE_SRC, pic))
				#print 'filename:'+pic
				post = Post(writer=g.user.uid, wid=wid, content=form.content.data, pic=pic, posted=posted)
				db.session.add(post)
				db.session.commit()
				#print 'redirect @@@@@@@@@@@@@@@@@@@@@@@'
				#print 'REDIRECT[1]: wall_id'+wid
				return redirect(url_for('wall',wid=wid))
			else:
				post = Post(writer=g.user.uid, wid=wid, content=form.content.data, pic='', posted=posted)
				db.session.add(post)
				db.session.commit()
				#print 'REDIRECT[2]: wall_id'+wid
				return redirect(url_for('wall',wid=wid))
		
	belongs = User.query.filter_by(uid=wid).first()
	wall = db.session.query(User,Post).filter(Post.wid==wid).filter(User.uid==Post.writer).order_by(Post.pid.desc()).all()
	#print wall
	#print 'render: wid'+wid+' ^^^^^^^^^^^^^^^^^^^^^'
	return render_template("wall.html", form=form, wall=wall, belongs=belongs, writer=g.user)

@app.route('/hack')
@login_required
@csrf.exempt
def hack():
	if g.user.email == 'yhong@purdue.edu':
		users = db.session.query(User).filter(User.activate==False).all()
		for u in users:
			db.session.query(User).filter_by(uid=u.uid).update({"activate":True})
		db.session.commit()
		
		users_1 = db.session.query(User).all()
		users_2 = db.session.query(User).all()

		rs = db.session.query(Request).all()
 
		for r in rs :
			db.session.delete(r)
			db.session.commit()

		for u1 in users_1:
			for u2 in users_2:
				if u1.uid==u2.uid:
					continue
				req = Request(sender=u1.uid, receiver=u2.uid, done=False, connected=False, sent=False)
				db.session.add(req)
				db.session.commit()

	return redirect(url_for('newsfeed',wid=g.user.uid))


@app.route('/delete_user')
@login_required
@csrf.exempt
def delete_user():
	if g.user.email == 'yhong@purdue.edu':
		users = db.session.query(User).filter(User.uid!=g.user.uid).all()
		for u in users:
			db.session.delete(u)
		db.session.commit()
	return redirect(url_for('newsfeed',wid=g.user.uid))


@app.route('/friend', methods=['GET','POST'])
@login_required
@csrf.exempt
def friend():
	users = db.session.query(User).filter(User.uid!=g.user.uid).all()
	friends = db.session.query(Friend).filter(Friend.uid==g.user.uid).all()
	waitings = db.session.query(Request).filter(Request.done==False).filter(Request.connected==True).filter(Request.sent==True).filter(Request.sender==g.user.uid).all()
	accepts = db.session.query(Request).filter(Request.connected==True).filter(Request.sent==True).filter(Request.done==False).filter(Request.receiver==g.user.uid).all()
	strangers = db.session.query(Request).filter(Request.sender==g.user.uid).filter(Request.connected==False).all()
	#print '#####'
	#print accepts
	#print '######'
	#print users
	return render_template('friend.html', users=users, friends=friends, waitings=waitings, accepts=accepts, strangers=strangers)

@app.route('/unfriend/<sender>_<receiver>', methods=['GET','POST'])
@login_required
@csrf.exempt
def unfriend(sender, receiver):
	f1 = db.session.query(Friend).filter(Friend.uid==sender).filter(Friend.fid==receiver).all()
	for f in f1:
		db.session.delete(f)

	f2 = db.session.query(Friend).filter(Friend.uid==receiver).filter(Friend.fid==sender).all()
	for a in f2:
		db.session.delete(a)

	db.session.commit()
	return redirect(url_for('cancel_request',sender=sender, receiver=receiver))

@app.route('/send_request/<sender>_<receiver>', methods=['GET','POST'])
@login_required
@csrf.exempt
def send_request(sender, receiver):
	#print 's='+sender
	#print 'r='+receiver
	req1 = db.session.query(Request).filter(Request.sender==sender).filter(Request.receiver==receiver).first()
	new_req = Request(sender=req1.sender, receiver=req1.receiver, done=False, connected=True, sent=True)
	db.session.delete(req1)
	db.session.add(new_req)

	req2 = db.session.query(Request).filter(Request.sender==receiver).filter(Request.receiver==sender).first()
	new_req2 = Request(sender=req2.sender, receiver=req2.receiver, done=False, connected=True, sent=False)
	db.session.delete(req2)
	db.session.add(new_req2)
	db.session.commit()
	
	#db.session.query(Request).filter(Request.sender==sender and Request.receiver==receiver).update({"sent":True})
	#db.session.query(Request).filter(Request.sender==receiver and Request.receiver==sender).update({"connected":True})
	#db.session.commit()

	#print db.session.query(Request).filter(Request.connected==True).all()
	

	return redirect(url_for('friend'))

@app.route('/canel_request/<sender>_<receiver>', methods=['GET','POST'])
@login_required
@csrf.exempt
def cancel_request(sender, receiver):
	#print 's='+sender
	#print 'r='+receiver
	req1 = db.session.query(Request).filter(Request.sender==sender).filter(Request.receiver==receiver).first()
	new_req = Request(sender=req1.sender, receiver=req1.receiver, done=False, connected=False, sent=False)
	db.session.delete(req1)
	db.session.add(new_req)

	req2 = db.session.query(Request).filter(Request.sender==receiver).filter(Request.receiver==sender).first()
	new_req2 = Request(sender=req2.sender, receiver=req2.receiver, done=False, connected=False, sent=False)
	db.session.delete(req2)
	db.session.add(new_req2)
	db.session.commit()
	
	#db.session.query(Request).filter(Request.sender==sender and Request.receiver==receiver).update({"sent":True})
	#db.session.query(Request).filter(Request.sender==receiver and Request.receiver==sender).update({"connected":True})
	#db.session.commit()

	#print db.session.query(Request).filter(Request.connected==True).all()
	

	return redirect(url_for('friend'))

@app.route('/accept_request/<sender>_<receiver>', methods=['GET','POST'])
@login_required
@csrf.exempt
def accept_request(sender, receiver):
	#print 's='+sender
	#print 'r='+receiver
	req1 = db.session.query(Request).filter(Request.sender==sender).filter(Request.receiver==receiver).first()
	new_req = Request(sender=req1.sender, receiver=req1.receiver, done=True, connected=True, sent=False)
	db.session.delete(req1)
	db.session.add(new_req)

	req2 = db.session.query(Request).filter(Request.sender==receiver).filter(Request.receiver==sender).first()
	new_req2 = Request(sender=req2.sender, receiver=req2.receiver, done=True, connected=True, sent=True)
	db.session.delete(req2)
	db.session.add(new_req2)

	s = Friend(uid=sender, fid=receiver, since=datetime.utcnow())
	r = Friend(uid=receiver, fid=sender, since=datetime.utcnow())
	db.session.add(s)
	db.session.add(r)
	db.session.commit()

	db.session.commit()
	
	#db.session.query(Request).filter(Request.sender==sender and Request.receiver==receiver).update({"sent":True})
	#db.session.query(Request).filter(Request.sender==receiver and Request.receiver==sender).update({"connected":True})
	#db.session.commit()

	#print db.session.query(Request).filter(Request.connected==True).all()
	

	return redirect(url_for('friend'))

@app.route('/newsfeed', methods=['GET','POST'])
@app.route('/newsfeed/<wid>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def newsfeed(wid):
	form = PostForm()
	error = None
	pic = ''
	#print '***************************************'
	if form.validate_on_submit():
		content = form.content.data
		posted = datetime.utcnow()
		if request.method == 'POST':
			file = request.files['file']
			#print 'request'
			if file and allowed_file(file.filename):
				pic = secure_filename(file.filename)
				file.save(os.path.join(IMAGE_SRC, pic))
				#print 'filename:'+pic
				post = Post(writer=g.user.uid, wid=wid, content=form.content.data, pic=pic, posted=posted)
				db.session.add(post)
				db.session.commit()
				#print 'redirect @@@@@@@@@@@@@@@@@@@@@@@'
				#print 'REDIRECT[1]: wall_id'+wid
				return redirect(url_for('wall',wid=wid))
			else:
				post = Post(writer=g.user.uid, wid=wid, content=form.content.data, pic='', posted=posted)
				db.session.add(post)
				db.session.commit()
				#print 'REDIRECT[2]: wall_id'+wid
				return redirect(url_for('wall',wid=wid))
		
	belongs = User.query.filter_by(uid=wid).first()

	wall = []

	friends= db.session.query(Friend).filter(Friend.uid==g.user.uid).all()
	posts = db.session.query(User,Post).filter(Post.wid!=g.user.uid).filter(User.uid==Post.writer).order_by(Post.pid.desc()).all()
	for post in posts:
		for friend in friends:
			if post.Post.writer==friend.fid:
				wall.append(post)
	#print wall
	#print 'render: wid'+wid+' ^^^^^^^^^^^^^^^^^^^^^'
	return render_template("newsfeed.html", form=form, wall=wall, belongs=belongs, writer=g.user)
	
@app.route('/circle', methods=['GET','POST'])
@login_required
@csrf.exempt
def circle():
	form = CircleForm()
	error = None
	
	return render_template("circle.html", form=form, writer=g.user)






