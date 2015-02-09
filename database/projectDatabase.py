import redis

keyFormat = 'project_{0}'
projectRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )#TODO: move to config file

def addNewProject(secretUrl, projectId, title, Author, SourceCode, Description, Input, Output, 
					Requirements,Usage,Example, tags):
	projectInfo = {
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

def getProjectInfo(projectId):
	key = _projectKey(projectId)
	result = projectRedisDB.hgetall(key+'_info')

	result['tags'] = projectRedisDB.smembers(key+'_tags')
	return result

def _projectKey(projectId):
	return keyFormat.format(projectId)
