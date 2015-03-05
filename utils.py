import re
from database import databaseFunctions

#all the isValid* functions return a status dict
#status = {
#	'isValid': False,
#	'reason' : '',#Reason why it is not valid 
#}
MAX_EMAIL_SIZE 	  = 100
MIN_EMAIL_SIZE 	  = 3
MAX_PASSWORD_SIZE = 100
MIN_PASSWORD_SIZE = 4
MAX_USERNAME_SIZE = 30
MIN_USERNAME_SIZE = 3

def isValidEmail(email):
	if email == None:
		return {'isValid':False, 'reason':'Invalid Email'}

	email = (str(email)).lower()
	if len(email) > MAX_EMAIL_SIZE:
		return {'isValid':False, 'reason':'Email was more than '+str(MAX_EMAIL_SIZE)+' characters'}

	if len(email) < MIN_EMAIL_SIZE:
		return {'isValid':False, 'reason':'Email was lass than '+str(MIN_EMAIL_SIZE)+' characters'}

	if re.match(r"[^@]+@[^@]+\.[^@]+", email) != None:
		return {'isValid':True, 'reason':''}
	else:
		return {'isValid':False, 'reason':'Invalid Email'}


def isValidUsername(username):
	if username == None:
		return {'isValid':False, 'reason':'Invalid Username'}

	username = (str(username)).lower()
	if len(username) > MAX_USERNAME_SIZE:
		return {'isValid':False, 'reason':'Username was more than '+str(MAX_USERNAME_SIZE)+' characters'}

	if len(username) < MIN_USERNAME_SIZE:
		return {'isValid':False, 'reason':'Username was lass than '+str(MIN_USERNAME_SIZE)+' characters'}

	if re.match("^[a-zA-Z0-9_.-]+$", username) != None:
		return {'isValid':True, 'reason':''}
	else:
		return {'isValid':False, 'reason':'Invalid Password'}


def isValidPassword(password):
	if password == None:
		return {'isValid':False, 'reason':'Invalid Password'}

	password = str(password)
	if len(password) > MAX_PASSWORD_SIZE:
		return {'isValid':False, 'reason':'Password was more than '+str(MAX_PASSWORD_SIZE)+' characters'}

	if len(password) < MIN_PASSWORD_SIZE:
		return {'isValid':False, 'reason':'Password was lass than '+str(MIN_PASSWORD_SIZE)+' characters'}

	if re.match(r'[A-Za-z0-9@#$%^&+=]{3,}', password) != None:
		return {'isValid':True, 'reason':''}
	else:
		return {'isValid':False, 'reason':'Invalid Password'}
