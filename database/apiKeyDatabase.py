import redis
import MySQLdb

keyFormat = 'apiKey_{0}'
apiKeyRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )

def addApiKey( apiKey, userId ):
  key = _apiKeyKey(apiKey)
  apiKeyRedisDB.set(key, userId)
  #db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
  #cur = db.cursor()
  
  #cur.execute("UPDATE CNGL_User_Tbl SET APIKey = '" + apiKey + "' WHERE UserID = " + userId)

def removeApiKey( apiKey ):
  key = _apiKeyKey(apiKey)
  apiKeyRedisDB.delete(key)
  #db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
  #cur = db.cursor()
  
  #cur.execute("UPDATE CNGL_User_Tbl SET APIKey = NULL WHERE APIKey LIKE '" + apiKey + "'")
  

def getApiKeyUserId(apiKey):
  key = _apiKeyKey(apiKey)
  return apiKeyRedisDB.get(key)
  
  
  #db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
  #cur = db.cursor()
  
  #cur.execute("SELECT UserID FROM CNGL_User_Tbl WHERE APIKey LIKE '" + apiKey + "'")
  
  #return cur.fetchone()

def _apiKeyKey(apiKey):
  return keyFormat.format(apiKey)
