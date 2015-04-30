from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, BooleanField, SubmitField, FileField, validators, StringField
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

class ProfileForm(Form):
	pic = FileField('')

class EditForm(Form):
	password = PasswordField('password', validators=[Required()])
	new_password = PasswordField('password', validators=[Required()])
	confirm_password = PasswordField('password', validators=[Required()])
	firstname = TextField('firstname', validators=[Required()])
	lastname = TextField('lastname', validators=[Required()])

class PostForm(Form):
	content = TextAreaField('content', validators=[Required()])
	pic = FileField('')




