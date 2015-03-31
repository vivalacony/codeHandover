import redis
import MySQLdb

keyUserFormat = 'stats_user_{0}_{1}'
keyProjectFormat = 'stats_project_{0}'
statsRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )

def addUserHit(statId, userId, projectId, time):
	key = _statsUserKey(userId, projectId)
	statsRedisDB.zadd(key, time, statId)
	
	#db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	
	#cur.execute("INSERT INTO CNGL_UserAnalytics_Tbl (UserID, WebServiceID) VALUES ('" + userId + "','"+ projectId +"')" )

def getAllUserHits( userId, projectId ):
	key = _statsUserKey(userId, projectId)
  	return statsRedisDB.zrange(key, 0, -1)


def addProjectHit(statId, projectId, time):
	key = _statsProjectKey(projectId)
	statsRedisDB.zadd(key, time, statId)

def getAllProjectHits(projectId):
	key = _statsProjectKey(projectId)
  	return statsRedisDB.zrange(key, 0, -1)


def _statsUserKey(userId, projectId):
  return keyUserFormat.format(userId, projectId)

def _statsProjectKey(projectId):
  return keyProjectFormat.format(projectId)
