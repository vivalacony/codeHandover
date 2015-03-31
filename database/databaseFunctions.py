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
import keywordDatabase
import time
import MySQLdb


def addNewProject(secretUrl, Uname, title, Author, SourceCode, Description, Input, Output, 
					Requirements,Usage,Example, tags):
	#TODO: replace with get threadId()
	projectId = getNewId()
	tags = tags.split()
	titleDatabase.addTitle(Uname, projectId)
	projectDatabase.addNewProject(secretUrl, Uname, projectId, title, Author, SourceCode, Description, Input, Output, 
									Requirements,Usage,Example, tags)
	globalDatabase.addProjectIdToProjectList(projectId)

	#tagDatabase.addTagsToProject(projectId, tags)
	addKeywordsToProject(projectId, tags)
	addKeywordsToProject(projectId, title.split() )
	addKeywordsToProject(projectId, Description.split())

	#TODO: put keyword database stuff here
	return projectId
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("SELECT UserID FROM CNGL_User_Tbl WHERE UserName LIKE '" + Uname + "'")
	#AddedByID=cur.fetchone()
  
	#cur.execute("INSERT INTO CNGL_Webservices_Tbl (Name,Description,SourceCodeLink,Author,AddedByID,ExpectedInput,Output) VALUES ('" + title + "', '" + Description + "','" + SourceCode + "', '" + "','" + Author + "'," + AddedByID +",'" + Input +"','" + Output + "'")

def getSearch(keywordlist):
	result = []
	projectIds = getIntersection(keywordlist)
	for projectId in projectIds:
		if getProjectInfo(projectId) != None and getProjectInfo(projectId) != {}:
			result.append(getProjectInfo(projectId))
	return result

def getIntersection(keywordlist):
	return keywordDatabase.getIntersection(keywordlist)

def editProject(projectId, secretUrl, Uname, title, Author, SourceCode, Description, Input, Output, 
					Requirements,Usage,Example, tags):
	projectInfo = getProjectInfo(projectId)
	titleDatabase.removeTitle(projectInfo['Uname'])
	titleDatabase.addTitle(Uname, projectId)

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

#	print "projectInfo['title'].split()"
#	print projectInfo['title'].split()
	deleteProjectFromTags(projectId, projectInfo['title'].split())
#	print "projectInfo['Description'].split()"
#	print projectInfo['Description'].split()
	deleteProjectFromTags(projectId, projectInfo['Description'].split())
#	print "projectInfo['tags']"
#	print projectInfo['tags']
	deleteProjectFromTags(projectId, projectInfo['tags'])

	titleDatabase.removeTitle(projectInfo['Uname'])
	projectDatabase.removeProject(projectId)
	globalDatabase.removeProjectIdFromProjectList(projectId)
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	
	#cur.execute("DELETE FROM CNGL_Webservices_Tbl WHERE WebserviceID = " + projectId)


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
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("UPDATE CNGL_User_Tbl SET UserName = '" + newUsername + "' WHERE UserID = " + userId)
	

def changePasswordHash(userId, newPasswordHash):
	userDatabase.changePasswordHash(userId, newPasswordHash)
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("UPDATE CNGL_User_Tbl SET Password = '" + newPasswordHash + "' WHERE UserID = " + userId)

def removePendingUser(userId):
	userInfo = pendingUserDatabase.getUserInfo(userId)
	pendingUserDatabase.removeUser(userId)
	emailDatabase.removeEmail(userInfo['email'])
	usernameDatabase.removeUsername(userInfo['username'])
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("DELETE FROM CNGL_User_Tbl WHERE UserID = " + userId)

def getUsernameUserId(username):
	return usernameDatabase.getUsernameUserId(username)
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("SELECT UserID FROM CNGL_User_Tbl WHERE UserName LIKE '" + username + "'")
	#userName = cur.fetchone()
	#return userName

def getUserInfo(userId):
	userStuff = userDatabase.getUserInfo(userId)
	userStuff['userId'] = userId
	return userStuff
	
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
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("SELECT COUNT(*) FROM CNGL_User_Tbl")
	#ProjectCount = cur.fetchone()
	#return ProjectCount

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
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("INSERT INTO CNGL_User_Tbl (UserName,Password,EmailAddress) VALUES ('" + username + "','" + passwordHash + "','" + email + "')")

def addKeywordsToProject(projectId, keywordList):
	keywordDatabase.addKeywordsToProject(projectId, keywordList)

def getUserListAll():
	result = []
	userList = globalDatabase.getUserListAll()
	for userId in userList:
		userInfo = getUserInfo(userId)
		userInfo['userId'] = userId
		result.append(userInfo)


	return result

def deleteProjectFromTags(projectId, tagsList):
	for tag in tagsList:
		keywordDatabase.removeFileIdFromTag( projectId, tag )


def getStatsData(userId):
	result = []
	projectList = getProjectListRange(0,-1)
	for projectId in projectList:
		#get the project name and the stats
		statsStuff = statsDatabase.getAllUserHits(userId, projectId)
		projectStuff = getProjectInfo(projectId)
		result.append( [projectStuff['title'], len(statsStuff) ] )

	return result	


def moveFromPendingToActive(userId):
	apiKey = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
	apiKeyDatabase.addApiKey(apiKey, userId)
	userInfo = pendingUserDatabase.getUserInfo(userId)
	pendingUserDatabase.removeUser(userId)
	globalDatabase.addToUserList(userId)
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
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("SELECT UserID FROM CNGL_User_Tbl WHERE APIKey LIKE '" + apiKey + "'")
	#userID = cur.fetchone()
	#return userID


def addApiKey( apiKey, userId ):
	apiKeyDatabase.addApiKey(apiKey, userId)
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("UPDATE CNGL_User_Tbl SET APIKey = '" + apiKey + "' WHERE userId = " + userId)

def removeApiKey( apiKey ):
	apiKeyDatabase.removeApiKey(apiKey)
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("UPDATE CNGL_User_Tbl SET APIKey = '' WHERE APIKey LIKE '" + apiKey + "'")

def getTitleProjectId(title):
	return titleDatabase.getTitleProjectId(title)
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("SELECT WebserviceID FROM CNGL_Webservices_Tbl WHERE Name LIKE '" + title + "'")
	#projectID = cur.fetchone()
	#return projectID

def addTitle( title, projectId ):
	titleDatabase.addTitle(title, userId)
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("UPDATE CNGL_Webservices_Tbl SET Name = '" + title + "' WHERE WebserviceID = " + projectId)

def removeTitle( title ):
	titleDatabase.removeTitle(title)
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("UPDATE CNGL_Webservices_Tbl SET Name = '' WHERE WebserviceID = " + projectId)


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
