from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, BooleanField, SubmitField, validators, StringField
from wtforms.validators import Required, Length, DataRequired
from models import User

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
	firstname = TextField('firstname', validators=[Required()])
	lastname = TextField('lastname', validators=[Required()])
	email = TextField('email', validators=[Required()])
	password = TextField('password', validators=[Required()])
	confirm_password = TextField('confirm_password', validators=[Required()])




