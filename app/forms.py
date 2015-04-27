from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length

class SignupForm(Form):
	firstname = TextField("First name", [validators.Required("Please enter your first name.")])
	lastname = TextField("Last name", [validators.Required("Please enter your last name.")])
	email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	submit = SubmitField("Create account")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user:
			self.email.errors.append("Email address already exists")
			reeturn False
		else :
			return True
