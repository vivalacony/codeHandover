from database import databaseFunctions
import redis
from flask import Flask, render_template, request, send_file, redirect, url_for
from flask.ext import login
import loginLogic
import utils
import requests
import time
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'USERNAME',
	MAIL_PASSWORD = 'PASSWORD'
	)

mail=Mail(app)

postRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )
postRedisDB.flushall()
databaseFunctions.createAdminAccount()

projectId = databaseFunctions.addNewProject('http://54.68.182.80:5555/api/summariser/', 'Uname', 'title', 'Author', 'SourceCode', 'Description', 
											'Input', 'Output', 'Requirements', 'Usage', 'Example', "tuna workmen")


AMOUNT_OF_MOST_RECENT = 15#the amount of most recent projects to show on the index page
AMOUNT_OF_PROJECTS_PER_SEARCH_PAGE = 15
MAX_USERNAME_CHARS	= 40
MAX_PASSWORD_CHARS	= 100
MAX_EMAIL_CHARS		= 100

@app.route("/")
@app.route("/home")
@app.route("/home/")
@app.route("/index.html")
@login.login_required
def showIndex(errors=[]):
	if request.args.get('error') != None:
		errors = [{'message':request.args.get('error'),'class':'bg-danger'}]

	recentProjectsIds = databaseFunctions.getProjectListRange(0, -1)
	recentProjects = []
	for projectId in recentProjectsIds:
		recentProjects.append( databaseFunctions.getProjectInfo(projectId) )

	return render_template("index.html", recentProjects=recentProjects, errors=errors)

@app.route("/searchForm")
@app.route("/searchForm")
@login.login_required
def showSearch():
	tags = request.args.get('q').split()
	if tags == None or tags == []:
		return render_template('search.html', results=[], isEmpty=True, errors = [{'message':'Invalid Search','class':'bg-danger'}])

	results = databaseFunctions.getSearch(tags)


	return render_template('search.html', results=results, isEmpty=False)

#getUserListAll
@app.route('/usersStats/')
@login.login_required
def userStatsPage():
	count = []
	packed = []
	users = databaseFunctions.getUserListAll()
	for user in users:
		count.append( len(databaseFunctions.getAllProjectHits(user['userId'])) )
		packed.append([user, len(databaseFunctions.getAllProjectHits(user['userId']))])

	return render_template('userStats.html', packed=packed)

#getUserListAll
@app.route('/usersStats/<userId>')
@login.login_required
def userStatsPageId(userId):
	#get a list of web services
	stats = databaseFunctions.getStatsData(userId)
	return render_template('userStatsDisplay.html', stats=stats)

@app.route('/addService')
@login.login_required
def addServicePage():
	if login.current_user.isAdmin == 'False':
		return redirect('/')

	return render_template('addService.html', serviceInfo={}, formAction="addServiceSubmit")

@app.route('/addServiceSubmit', methods=['POST'])
@login.login_required
def addServiceSubmitPage():
	if login.current_user.isAdmin == 'False':
		return redirect('/')

	print 'request.form'
	print request.form

	#FIXME: check valid title
	if (len(request.form.get('title')) > 0 and len(request.form.get('serviceurl')) > 0
			and len(request.form.get('uname')) > 0):
		databaseFunctions.addNewProject(
			request.form.get('serviceurl'), 
			request.form.get('uname'), 
			request.form.get('title'), 
			request.form.get('Author'), 
			request.form.get('sourcecode'), 				
			request.form.get('description'), 
			request.form.get('input'), 
			request.form.get('output'), 
			request.form.get('requirements'),
			request.form.get('usage'),
			request.form.get('example'), 
			request.form.get('tags'))
		return redirect('/dashboard?success=Success: Service Added')
	else:
		return redirect('/addService?error=Error: Bad Title')

@app.route('/editService/<serviceId>')
@login.login_required
def editServicePage(serviceId):
	if login.current_user.isAdmin == 'False':
		return redirect('/')

	serviceInfo = databaseFunctions.getProjectInfo(serviceId)
	serviceInfo['id'] = serviceId
	return render_template('addService.html', serviceInfo=serviceInfo, formAction="editServiceSubmit")

@app.route('/editServiceSubmit', methods=['POST'])
@login.login_required
def editServiceSubmitPage():
	if login.current_user.isAdmin == 'False':
		return redirect('/')

	projectInfo = databaseFunctions.getProjectInfo(request.form.get('existingId'))
	#remove the stuff
#	print "projectInfo['title'].split()"
#	print projectInfo['title'].split()
	deleteProjectFromTags(projectId, projectInfo['title'].split())
#	print "projectInfo['Description'].split()"
#	print projectInfo['Description'].split()
	deleteProjectFromTags(projectId, projectInfo['Description'].split())
#	print "projectInfo['tags']"
#	print projectInfo['tags']
	deleteProjectFromTags(projectId, projectInfo['tags'])


	tagsList = request.form.get('tags')#do the title and other stuff !!!!
	databaseFunctions.deleteProjectFromTags(request.form.get('existingId'), tagsList)

	databaseFunctions.editProject(
			request.form.get('existingId'),
			request.form.get('serviceurl'), 
			request.form.get('uname'), 
			request.form.get('title'), 
			request.form.get('Author'), 
			request.form.get('sourcecode'), 				
			request.form.get('description'), 
			request.form.get('input'), 
			request.form.get('output'), 
			request.form.get('requirements'),
			request.form.get('usage'),
			request.form.get('example'), 
			request.form.get('tags'))

	return redirect('/dashboard?success=Success: Service Edited')

@app.route('/removeService/<serviceId>')
@login.login_required
def removeServicePage(serviceId):
	if login.current_user.isAdmin == 'False':
		return redirect('/')

	databaseFunctions.removeProject(serviceId)
	return redirect('/?success=Success: Service removed')


@app.route('/acceptUser/<userId>')
@login.login_required
def acceptUserPage(userId):
	if login.current_user.isAdmin == 'False':
		return redirect('/')

	databaseFunctions.moveFromPendingToActive(userId)
	#msg = Message("Hello tom what's up ?", sender=("Me", "tom@79.97.58.215.com"), recipients=["tomnomnom1@gmail.com"])
	#mail.send(msg)
	return redirect('/dashboard?success=Success: User Accepted')

@app.route('/rejectUser/<userId>')
@login.login_required
def rejectUserPage(userId):
	if login.current_user.isAdmin == 'False':
		return redirect('/')

	databaseFunctions.removePendingUser(userId)
	return redirect('/dashboard?success=Success: User Rejected')

@app.route("/api/<projectTitle>/", methods=['POST'])
def projectTitlePage(projectTitle):

	#check if the api key is valid
	apiKey = request.form.get('apikey')

	if apiKey == None or apiKey == '':
		return '/error=Error: bad api key'

	#get the user of the api key 
	userId = databaseFunctions.getApiKeyUserId(apiKey)

	if userId == None or userId == '':
		return '/error=Error: bad api key'

	userInfo = databaseFunctions.getUserInfo(userId)
	
	#hit the stats 

	#find the project
	projectId = databaseFunctions.getTitleProjectId(projectTitle)
	
	if projectId == None:
		return '/error=Error: Bad Project Name'
	
	projectInfo = databaseFunctions.getProjectInfo(projectId)
	
	databaseFunctions.addUserHit(userId, projectId)
	databaseFunctions.addProjectHit(userId)
	print request.form.to_dict(flat=False)
	try:
		r = requests.post(projectInfo['secretUrl'], data=request.form.to_dict(flat=False))
	except Exception, e:
		return '/error=Error: bad secret url: ' + projectInfo.get('secretUrl')
	
	#get the contents from the url (with the post data sent)

	return r.text

@app.route("/api/<projectTitle>/<apiKey>")
def testProjectTitlePage(projectTitle, apiKey):

	#check if the api key is valid
	#apiKey = request.form.get('apikey')

	if apiKey == None or apiKey == '':
		return '/error=Error: bad api key'

	#get the user of the api key 
	userId = databaseFunctions.getApiKeyUserId(apiKey)

	if userId == None or userId == '':
		return '/error=Error: bad api key'

	userInfo = databaseFunctions.getUserInfo(userId)
	
	#hit the stats 

	#find the project
	projectId = databaseFunctions.getTitleProjectId(projectTitle)
	
	if projectId == None:
		return '/error=Error: Bad Project Name'
	
	projectInfo = databaseFunctions.getProjectInfo(projectId)
	
	databaseFunctions.addUserHit(userId, projectId)
	databaseFunctions.addProjectHit(userId)

	try:
		r = requests.post(projectInfo['secretUrl'], data=request.form.to_dict(flat=False))
	except Exception, e:
		return '/error=Error: bad secret url: ' + projectInfo.get('secretUrl')
	
	#get the contents from the url (with the post data sent)

	return r.text

@app.route("/r/<projectId>")
@app.route("/r/<projectId>/")
@login.login_required
def showProject(projectId):
	projectInfo = databaseFunctions.getProjectInfo(projectId)
	stats = databaseFunctions.getAllUserHits(login.current_user.get_id(), projectId)
	return render_template("project.html", projectInfo=projectInfo, stats=stats)

#TODO: allow editing of projects
@app.route("/r/<projectId>/edit", methods=['POST'])
@login.login_required
def editProject(projectId):
	if not login.current_user.isAdmin:
		return redirect('/')

	if request.form.get('postContent'):
		pass
	else:
		pass

@app.route('/logout')
def logoutPage(errors=[]):
	login.logout_user()
	return redirect('/')

@app.route('/login')
def loginPage(errors=[]):
	if request.args.get('error') != None:
		errors = [{'message':request.args.get('error'),'class':'bg-danger'}]
	if request.args.get('success') != None:
		errors = [{'message':request.args.get('success'),'class':'bg-success'}]
	return render_template("loginPage.html", errors=errors)

@app.route('/loginSubmit', methods=['POST'])
def loginSubmitPage():
	userStringId = request.form.get('username')
	password 	 = request.form.get('password')

	if userStringId == None or userStringId == '':
		return redirect('/login?error=Error: Invlaid Email or username')

	if password == None or password == '':
		return redirect('/login?error=Error: Invlaid Password')

	status = loginLogic.loginUser(userStringId, password)
	if not status['isValid']:
		return redirect('/login?error='+status['reason'])

	return redirect('/')

@app.route('/dashboard')
@app.route('/admin')
@login.login_required
def dashboardPage(errors=[]):
	if request.args.get('error') != None:
		errors = [{'message':request.args.get('error'),'class':'bg-danger'}]
	if request.args.get('success') != None:
		errors = [{'message':request.args.get('success'),'class':'bg-success'}]
	
	if login.current_user.isAdmin == 'True':
		pendingUsers = []
		pendingUsers = databaseFunctions.getAllPendingUsers()
	else:
		pendingUsers = []

	return render_template("dashboard.html", pendingUsers=pendingUsers, errors=errors)

@app.route('/changeUsername')
@login.login_required
def changeUsernamePage(errors=[]):
	if request.args.get('error') != None:
		errors = [{'message':request.args.get('error'),'class':'bg-danger'}]

	return render_template("changeUsername.html", errors=errors)

@app.route('/changeUsernameSubmit', methods=['POST'])
@login.login_required
def changeUsernameSubmitPage(errors=[]):
	if request.args.get('error') != None:
		errors = [{'message':request.args.get('error'),'class':'bg-danger'}]

	#FIXME: make sure the username is a valid username
	if request.form.get('username') != None:
		databaseFunctions.changeUsername(login.current_user.userId, request.form.get('username'))
		return redirect('/dashboard?success=Success: Username Changed to '+request.form.get('username'))
	else:
		return redirect('/dashboard?error=Error: Username Change Failed, darn it :(')
		
@app.route('/apiKeyDocs')
@login.login_required
def apiKeyDocsPage(errors=[]):
	if request.args.get('error') != None:
		errors = [{'message':request.args.get('error'),'class':'bg-danger'}]

	return render_template("docs.html", errors=errors)

@app.route('/changePassword')
@login.login_required
def changePasswordPage(errors=[]):
	if request.args.get('error') != None:
		errors = [{'message':request.args.get('error'),'class':'bg-danger'}]

	return render_template("changePassword.html", errors=errors)

@app.route('/changePasswordSubmit', methods=['POST'])
@login.login_required
def changePasswordSubmitPage(errors=[]):
	if request.args.get('error') != None:
		errors = [{'message':request.args.get('error'),'class':'bg-danger'}]
	
	if (request.form.get('oldpassword') != None and request.form.get('password') != None 
			and request.form.get('passwordAgain') != None):
		oldPassword  = request.form.get('oldpassword')
		newPassword1 = request.form.get('password')
		newPassword2 = request.form.get('passwordAgain')

		status = utils.isValidPassword(newPassword1)
		if not status['isValid']:
			return redirect('/changePassword?error=Error '+status['reason'])

		if not loginLogic.checkUserPassword(login.current_user, oldPassword):
			return redirect('/changePassword?error=Error: Wrong Old password.')
		elif newPassword1 != newPassword2:
			return redirect('/changePassword?error=Error: New Passwords didn\'t Match')

		newPasswordHash = loginLogic.hashPassword(newPassword1)

		databaseFunctions.changePasswordHash(login.current_user.userId, newPasswordHash)
		return redirect('/dashboard?success=Success: Password Changed')
	else:
		return redirect('/dashboard?error=Error: Password Change Failed, darn it :(')


@app.route("/signupSubmit", methods=['POST'])
def signupSubmitPage():

	username = request.form.get('username')
	status = utils.isValidUsername(username)
	if not status['isValid']:
		return redirect('/login?error=Error '+status['reason'])

	email = request.form.get('email')
	status = utils.isValidEmail(email)
	if not status['isValid']:
		return redirect('/login?error=Error '+status['reason'])

	password = request.form.get('password')
	status = utils.isValidPassword(password)
	if not status['isValid']:
		return redirect('/login?error=Error '+status['reason'])

	#hash the password and try to add it to the database
	#for the moment we'll just keep it in glorious plain text :D
	passwordHash = loginLogic.hashPassword(password);
	
	statusCode = databaseFunctions.addPendingUser(email, username, passwordHash)
	if statusCode == -1:
		return redirect('/login?error=Error: Username is already registered.')
	elif statusCode == -2:
		return redirect('/login?error=Error: Email is already registered.')

	#TODO: redirect so we don't get double submitting when the user hits the back button
	return redirect('/login?success=Success! please wait for the Admin to accept your registration.')
 
def genPageButtons(resultsNo, pageNo):
	#FIX ME: THE +1 HERE IS WRONG, 
	#IT SHOULD ONLY +1 IF resultsNo%AMOUNT_OF_PROJECTS_PER_SEARCH_PAGE > 0
	pages = (resultsNo/AMOUNT_OF_PROJECTS_PER_SEARCH_PAGE)+1;
	result = []
	for x in range(pages):
		if int(x+1) == int(pageNo):
			result.append({'number':str(x+1), 'active':str(True) })
		else:
			result.append({'number':str(x+1), 'active':str(False)})
	return result

def init_login():
	login_manager = login.LoginManager()
	login_manager.init_app(app)

	# Create user loader function
	@login_manager.user_loader
	def load_user(user_id):
		return loginLogic.getUserFromId(user_id)

	@login_manager.unauthorized_handler
	def showLoginPage():
		return redirect("/login")


init_login()

if __name__ == "__main__":
	app.debug = True
	app.run()
