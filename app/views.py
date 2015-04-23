from app import app
from flask import render_template, redirect, url_for, request

# route for handling index page
@app.route('/')
@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/index')
def index():
	user = {'nickname': 'Yongsun'} # fake user
	posts = [
		{
			'user': {'nickname': 'John'},
			'content': 'Post of John!'
		},
		{
			'user': {'nickname': 'Susan'},
			'content': 'Post of Susan!'
		}
	]
	return render_template('index.html', title='Home', user=user, posts=posts)

# route for handling welcome page


