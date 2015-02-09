from flask import Flask
from flask.ext import login
from database import databaseFunctions
from app import app

class User(object):

	def __init__(self, userId, isActive, is_authenticated, 
					isAdmin, username, email, passwordHash, apiKey):
		self.userId 		= userId
		self.isActiveVar 	= isActive
		self.isAuthenticated = is_authenticated
		self.isAdmin 		= isAdmin
		self.username		= username
		self.email			= email
		self.passwordHash	= passwordHash
		self.apiKey			= apiKey

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.userId


#returns a User object if valid userId, None otherwise
def getUserFromId(userId):
	#get the database function
	isPendingUser = False
	userData = databaseFunctions.getUserInfo(userId)
	if userData == None or userData == {}:
		userData = databaseFunctions.getPendingUserInfo(userId)
		isPendingUser = True
	if userData == None or userData == {}:
		return None

	print 'userData'
	print userData

	return User(userId, (not isPendingUser), False, userData.get('isAdmin'), 
				userData['username'], userData['email'], userData['passwordHash'], 
				userData.get('apiKey'))


#userStringId can be username or email 
#returns a status
def loginUser(userStringId, password):
	status = {
		'isValid': False,
		'reason': ''
	}
	#check if valid userName/email
	userId = databaseFunctions.getUsernameUserId(userStringId)
	if userId == None:
		userId = databaseFunctions.getEmailUserId(userStringId)

	if userId == None:
		status['reason'] = 'Error: Invalid username/email address'
		return status

	print 'userId'
	print userId
	
	tempUser = getUserFromId(userId)
	hashedPassword = password#plain text

	if not hashedPassword == tempUser.passwordHash:
		status['reason'] = 'Error: Wrong password.'
		return status

	#actually log in the user
	login.login_user(tempUser)
	
	status['isValid'] = True
	return status

