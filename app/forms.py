from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, BooleanField, SubmitField, validators, StringField
from wtforms.validators import Required, Length, DataRequired
from models import User

class LoginForm(Form):
    email = TextField('email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
	firstname = TextField('firstname', validators=[Required()])
	lastname = TextField('lastname', validators=[Required()])
	email = TextField('email', validators=[Required()])
	password = PasswordField('password', validators=[Required()])
	confirm_password = PasswordField('confirm_password', validators=[Required()])




