import random
import string
import globalDatabase
import projectDatabase
import fileDatabase
import tagDatabase
import pendingUserDatabase
import userDatabase
import usernameDatabase
import emailDatabase
from werkzeug.security import generate_password_hash, check_password_hash
import apiKeyDatabase
import titleDatabase
import statsDatabase
import time


def addNewProject(secretUrl, Uname, title, Author, SourceCode, Description, Input, Output, 
					Requirements,Usage,Example, tags, keywords):
	#TODO: replace with get threadId()
	projectId = getNewId()
	titleDatabase.addTitle(Uname, projectId)
	projectDatabase.addNewProject(secretUrl, Uname, projectId, title, Author, SourceCode, Description, Input, Output, 
									Requirements,Usage,Example, tags)
	globalDatabase.addProjectIdToProjectList(projectId)
	tagDatabase.addTagsToProject(projectId, tags)
	#TODO: put keyword database stuff here
	return projectId

def editProject(projectId, secretUrl, Uname, title, Author, SourceCode, Description, Input, Output, 
					Requirements,Usage,Example, tags, keywords):
	projectInfo = getProjectInfo(projectId)
	titleDatabase.removeTitle(projectInfo['Uname'])
	titleDatabase.addTitle(Uname, projectId)

	print 'projectInfo'
	print projectInfo

	projectDatabase.addNewProject(secretUrl, Uname, projectId, title, Author, SourceCode, 
								Description, Input, Output, Requirements,Usage,Example, tags);

	#FIXME: hm.....you should really remove all the old tags.....
	tagDatabase.addTagsToProject(projectId, tags)
	return 

def removeProject(projectId):
	#remove the keywords
	projectInfo = getProjectInfo(projectId)

#	for utils.getKeywords(description):
#		pass

#	for tag in tags:
#		pass

	titleDatabase.removeTitle(projectInfo['Uname'])
	projectDatabase.removeProject(projectId)
	globalDatabase.removeProjectIdFromProjectList(projectId)


#function should be run whenever redis database is cleared
#or when you move server ect.
def createAdminAccount():
	userId = getNewId()
	emailDatabase.addEmail('Admin@admin.com', userId)
	usernameDatabase.addUsername('admin', userId)
	apiKeyDatabase.addApiKey('241231232130952', userId)
	
	userDatabase.addUser(userId, 'Admin@admin.com', 'Admin', 
							generate_password_hash('password'), '241231232130952', True)

def changeUsername(userId, newUsername):
	userInfo = userDatabase.getUserInfo(userId)
	print 'userInfo'
	print userInfo
	usernameDatabase.removeUsername( userInfo['username'] )
	userDatabase.changeUsername(userId, newUsername)
	usernameDatabase.addUsername(newUsername, userId)

def changePasswordHash(userId, newPasswordHash):
	userDatabase.changePasswordHash(userId, newPasswordHash)

def removePendingUser(userId):
	userInfo = pendingUserDatabase.getUserInfo(userId)
	pendingUserDatabase.removeUser(userId)
	emailDatabase.removeEmail(userInfo['email'])
	usernameDatabase.removeUsername(userInfo['username'])

def getUsernameUserId(username):
	return usernameDatabase.getUsernameUserId(username)

def getUserInfo(userId):
	return userDatabase.getUserInfo(userId)
	
def getPendingUserInfo(userId):
	return pendingUserDatabase.getUserInfo(userId)

def getUserInfo(userId):
	return userDatabase.getUserInfo(userId)

def getEmailUserId(email):
	return emailDatabase.getEmailUserId(email)

def getProjectListRange(start, end):
	return globalDatabase.getProjectListRange(start, end)

def getProjectInfo(projectId):
	return projectDatabase.getProjectInfo(projectId)

def getNewId():
	globalDatabase.incrementGlobalCount()
	return str(globalDatabase.getGlobalCount())

def getProjectCount():
	return globalDatabase.getProjectCount()

#TODO: make this return status with the userId
#return 0 if success, -1 if username already exists, -2 if email already exists
def addPendingUser(email, username, passwordHash):
	#make sure the username and email don't match existing ones
	if not usernameDatabase.getUsernameUserId(username) == None:
		return -1
		
	if not emailDatabase.getEmailUserId(email) 			== None:
		return -2

	userId = getNewId()
	emailDatabase.addEmail(email, userId)
	usernameDatabase.addUsername(username, userId)
	pendingUserDatabase.addUser(userId, email, username, passwordHash)
	return 0

def moveFromPendingToActive(userId):
	apiKey = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
	apiKeyDatabase.addApiKey(apiKey, userId)
	userInfo = pendingUserDatabase.getUserInfo(userId)
	pendingUserDatabase.removeUser(userId)
	userDatabase.addUser(userId, userInfo['email'], userInfo['username'],
						 userInfo['passwordHash'], apiKey, False)

def getAllPendingUsers():
	result = []
	pendingUsersList = pendingUserDatabase.getAllPendingUsers()
	for userId in pendingUsersList:
		temp = pendingUserDatabase.getUserInfo(userId)
		temp['userId'] = userId
		result.append( temp )

	return result


def getApiKeyUserId(apiKey):
	return apiKeyDatabase.getApiKeyUserId(apiKey)

def addApiKey( apiKey, userId ):
	apiKeyDatabase.addApiKey(apiKey, userId)

def removeApiKey( apiKey ):
	apiKeyDatabase.removeApiKey(apiKey)

def getTitleProjectId(title):
	return titleDatabase.getTitleProjectId(title)

def addTitle( title, projectId ):
	titleDatabase.addTitle(title, userId)

def removeTitle( title ):
	titleDatabase.removeTitle(title)


def addUserHit(userId, projectId):
	statId = getNewId()
	statsDatabase.addUserHit(statId, userId, projectId, int(time.time()))

def getAllUserHits(userId, projectId):
	return statsDatabase.getAllUserHits(userId, projectId)


def addProjectHit(projectId):
	statId = getNewId()
	statsDatabase.addProjectHit(statId, projectId, int(time.time()))

def getAllProjectHits(projectId):
	return statsDatabase.getAllProjectHits(projectId)

def getProjectStats():
	#keep going back in 24 hour chunks
	#last 24 hours is "today"
	#get the number of them between that time and add it to the whatever
	#don't bother have the dates just "last 30 days"
	pass
