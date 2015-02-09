import globalDatabase
import projectDatabase
import fileDatabase
import tagDatabase
import pendingUserDatabase
import userDatabase
import usernameDatabase
import emailDatabase

def addNewProject(creatorId, title, shortDescription, longDescription, 
				gitUrl, wikiUrl, attachedFileId, tags):
	#TODO: replace with get threadId()
	projectId = getNewId()
	projectDatabase.addNewProject(projectId, creatorId, title, shortDescription, 
		longDescription, gitUrl, wikiUrl, attachedFileId, tags);
	globalDatabase.addProjectIdToProjectList(projectId)
	tagDatabase.addTagsToProject(projectId, tags)
	return projectId

#function should be run whenever redis database is cleared
#or when you move server ect.
def createAdminAccount():
	userId = getNewId()
	emailDatabase.addEmail('Admin@admin.com', userId)
	usernameDatabase.addUsername('admin', userId)
	userDatabase.addUser(userId, 'Admin@admin.com', 'Admin', 
							'password', '240952', True)

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
	apiKey = '2000143204234' + getNewId()#lol security
	userInfo = pendingUserDatabase.getUserInfo(userId)
	pendingUserDatabase.removeUser(userId)
	userDatabase.addUser(userId, email, username, passwordHash, apiKey, False)

def getAllPendingUsers():
	result = []
	pendingUsersList = pendingUserDatabase.getAllPendingUsers()
	for userId in pendingUsersList:
		temp = pendingUserDatabase.getUserInfo(userId)
		temp['userId'] = userId
		result.append( temp )

	return result