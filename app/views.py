from app import app
from flask import render_template, redirect, flash
from .forms import LoginForm

# route for handling index page
@app.route('/')
@app.route('/welcome')
# route for handling welcome page
def welcome():
	return render_template('welcome.html')

# route for handling index page
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

# route for handling login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="%s", remember_me=%s' %(form.openid.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template('login.html', title='Sign In', form=form, providers=app.config['OPENID_PROVIDERS'])




