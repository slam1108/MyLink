from app import app, db, login_manager, open_id
from flask import flash, render_template, request, session, redirect, url_for, g
from models import User
from forms import LoginForm, RegisterForm
from flask.ext.login import login_user, logout_user, current_user, login_required

# route for handling home page
@app.route('/')
@app.route('/index')
@login_required
def index():
    if g.user is None or g.user.is_authenticated() == False:
    	return render_template('intro.html')

# loads a user from the database
@login_manager.user_loader
def load_user(uid):
	return User.query.get(int(uid))

@app.route('/login', methods=['GET', 'POST'])
@open_id.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return	open_id.try_login(form.openid.data, ask_for=['nickname', 'email'])
	return render_template('login.html', title='Sign In',
							form=form, providers=app.config['OPENID_PROVIDERS'])

@open_id.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))
	user = User.query.filter_by(email=resp.email).first()
	if user is None:
		firstname = resp.firstname
		lastname = resp.lastname
		email = resp.email
		password = resp.password
		pic = ''
		user = User(firstname=firstname, lastname=lastname, email=email,
					password=password, pic=pic)
		db.session.add(user)
		db.session.commit()
	remember_me=False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# current_user global is set by flask_login
@app.before_request
def before_request():
	g.user = current_user


@app.route('/register', methods=['GET','POST'])
def register():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = RegisterForm()
	error = None
	if form.validate_on_submit():
		firstname = form.firstname.data
		lastname = form.lastname.data
		email = form.email.data.lower()
		password = form.password.data
		confirm_password = form.confirm_password.data
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
						password=password, pic=pic)
			db.session.add(user)
			db.session.commit()
			return render_template('login.html')
	return render_template('register.html', title='Register', form=form)













