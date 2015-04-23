from app import app
from flask import render_template, request
from forms import ContactForm

# route for handling home page
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	form = ContactForm()

	if request.method == 'POST':
		return 'Form posted.'
	elif request.method == 'GET':
		return render_template('contact.html', form=form)

