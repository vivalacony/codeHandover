import redis
import MySQLdb

keyFormat = 'email_{0}'
emailRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )

def addEmail( email, userId ):
  key = _emailKey(email)
  emailRedisDB.set(key, userId)
  
  #db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("UPDATE CNGL_User_Tbl SET EmailAddress = '" + email + "' WHERE UserID = " + userId)

def removeEmail( email ):
  key = _emailKey(email)
  emailRedisDB.delete(key)
  
  #db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("UPDATE CNGL_User_Tbl SET EmailAddress = '' WHERE UserID = " + userId)

def getEmailUserId(email):
  key = _emailKey(email)
  return emailRedisDB.get(key)
  
  #db=MySQLdb.connect(host="localhost",user="root",passwd="woot",db="TestDB")
  
	#cur = db.cursor()
	#cur.execute("SELECT UserID FROM CNGL_User_Tbl WHERE EmailAddress LIKE '" + email + "'")

def _emailKey(email):
  return keyFormat.format(email)
