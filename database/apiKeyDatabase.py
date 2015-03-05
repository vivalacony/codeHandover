import redis

keyFormat = 'apiKey_{0}'
apiKeyRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )

def addApiKey( apiKey, userId ):
  key = _apiKeyKey(apiKey)
  apiKeyRedisDB.set(key, userId)

def removeApiKey( apiKey ):
  key = _apiKeyKey(apiKey)
  apiKeyRedisDB.delete(key)

def getApiKeyUserId(apiKey):
  key = _apiKeyKey(apiKey)
  return apiKeyRedisDB.get(key)

def _apiKeyKey(apiKey):
  return keyFormat.format(apiKey)
