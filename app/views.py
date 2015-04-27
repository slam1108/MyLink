from app import app 
from forms import SignupForm
from flask import Flask, render_template, request, session
from models import db, User

# route for handling home page
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/testdb')
def testdb():
	if db.session.query("1").from_statement("SELECT 1").all():
		return 'It works'
	else :
		return 'Something is broken'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else :
			new_user = User(form.firstname,data, form.lastname.data, form.email.data, form.password.data, '')
			db.sessoin.add(new_user)
			db.session.commit()

			session['email'] = new_user.email
			return redirect(url_for('profile'))

			return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/profile')
def profile():
	if('email') not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html')