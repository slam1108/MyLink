from flask.ext.mail import Message
from app import mail
from flask import url_for, render_template

def send_activate(user):
	message = Message(subject='MyLink Activation.',
					  sender='serendibeats@gmail.com',
					  recipients=[user.get_email()])
	activate_url = url_for('activate_account', uid=user.get_id(), _external=True)
	print '#######################################'
	message.html = activate_url
	print message.html
	mail.send(message)



	
	
