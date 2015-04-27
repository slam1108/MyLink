from app import app 
from models import db
from forms import SignupForm
from flask import Flask, render_template, request

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
			return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
	elif request.method == 'GET':
		return render_template('signup.html', form=form)