import redis
import MySQLdb

keyFormat = 'project_{0}'
projectRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )#TODO: move to config file

def addNewProject(secretUrl, Uname, projectId, title, Author, SourceCode, Description, Input, Output, 
					Requirements,Usage,Example, tags):
	projectInfo = {
		'Uname':  Uname,
		'secretUrl': secretUrl,
		'projectId': projectId,
		'title': title,
		'Author': Author,
		'SourceCode': SourceCode,
		'Description': Description,
		'Input': Input,
		'Output': Output,
		'Requirements': Requirements,
		'Usage': Usage,
		'Example': Example
	}
	key = _projectKey(projectId)
	projectRedisDB.hmset(key+'_info', projectInfo)
	for tag in tags:
		projectRedisDB.sadd(key+'_tags', tag)
		
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("SELECT UserID FROM CNGL_User_Tbl WHERE UserName LIKE '" + Uname + "'")
	#AddedByID=cur.fetchone()
  
	#cur.execute("INSERT INTO CNGL_Webservices_Tbl (Name,Description,SourceCodeLink,Author,AddedByID,ExpectedInput,Output) VALUES ('" + title + "', '" + Description + "','" + SourceCode + "', '" + "','" + Author + "'," + AddedByID +",'" + Input +"','" + Output + "'")

def removeProject(projectId):
	key = _projectKey(projectId)
	projectRedisDB.delete(key+'_info')
	projectRedisDB.delete(key+'_tags')
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	
	#cur.execute("DELETE FROM CNGL_Webservices_Tbl WHERE WebserviceID = " + projectId)

def getProjectInfo(projectId):
	key = _projectKey(projectId)
	result = projectRedisDB.hgetall(key+'_info')

	result['tags'] = projectRedisDB.smembers(key+'_tags')
	return result

def _projectKey(projectId):
	return keyFormat.format(projectId)
