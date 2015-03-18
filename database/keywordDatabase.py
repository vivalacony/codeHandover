import redis

keyFormat = 'keyword_{0}'
keywordRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )

def addKeywordsToProject( projectId, tagsList ):
  if isinstance( tagsList, basestring):#if a string is passed in convert it to a list of one element
    tagsList = [ tagsList ]

  for tag in tagsList:
    key = _tagKey(tag.lower())
    keywordRedisDB.sadd( key, projectId )

def getIntersection( keywords ):
  fixed = []
  for keyword in keywords:
    key = _tagKey( keyword.lower() )
    fixed.append( key )

  return keywordRedisDB.sinter( fixed )

def removeFileIdFromTag( projectId, tag ):
  #TODO: what happens if it doesn't exist ??
  key = _tagKey(tag.lower())
  keywordRedisDB.srem( key, projectId )

def getMatchingProjects( keyword ):
  key = _tagKey(keyword.lower())
  return keywordRedisDB.smembers( key )

def _tagKey(tag):
  return keyFormat.format(tag)
