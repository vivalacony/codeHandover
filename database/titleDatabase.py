import redis

keyFormat = 'title_{0}'
titleRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )

def addTitle( title, userId ):
  key = _titleKey(title)
  titleRedisDB.set(key, userId)

def removeTitle( title ):
  key = _titleKey(title)
  titleRedisDB.delete(key)

def getTitleProjectId(title):
  key = _titleKey(title)
  return titleRedisDB.get(key)

def _titleKey(title):
  return keyFormat.format(title)
