from app import app 
from models import db

# route for handling home page
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/testdb')
def testdb():
	if db.session.query("1").from_statement("SELECT 1").all():
		return 'It works'
	else:
		return 'Something is broken'

