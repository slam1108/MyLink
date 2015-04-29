from app import app, db, login_manager, service, csrf
from flask import flash, render_template, request, session, redirect, url_for, g
from models import User
from forms import LoginForm, RegisterForm, EditForm, ProfileForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_wtf.csrf import CsrfProtect
from werkzeug import secure_filename

CsrfProtect(app)

# route for handling home page
@app.route('/')
@app.route('/intro')
@csrf.exempt
def intro():
    if g.user is None or g.user.is_authenticated() == False:
    	return render_template('intro.html')
    return render_template('intro.html')

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
			return redirect(request.args.get('next') or url_for('intro'))
	return render_template('login.html', title='Register', error=error, form=form)


@app.route('/activate_account/<uid>')
@csrf.exempt
def activate_account(uid):
	user = User.query.filter_by(uid=uid).first()
	db.session.query(User).filter_by(uid=uid).update({"activate":True})
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
			db.session.add(user)
			db.session.commit()
			service.send_activate(user)
			return render_template('welcome.html')
	return render_template('register.html', title='Register', form=form)

@app.route('/profile', methods=['GET','POST'])
@login_required
@csrf.exempt
def profile():
	form = ProfileForm()
	if form.validate_on_submit():
		if form.pic.data.filename and allowed_file
	return render_template('profile.html', user=g.user)

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
			return render_template('profile.html', user=g.user)
	return render_template('edit.html', form=form)
















