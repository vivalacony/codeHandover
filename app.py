from database import databaseFunctions
import redis
from flask import Flask, render_template, request, send_file, redirect, url_for
from flask.ext import login
import loginLogic

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'

postRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )
postRedisDB.flushall()
databaseFunctions.createAdminAccount()

projectId = databaseFunctions.addNewProject('secretUrl', 'Uname', 'title', 'Author', 'SourceCode', 'Description', 
											'Input', 'Output', 'Requirements', 'Usage', 'Example', [], [])
projectId = databaseFunctions.addNewProject('secretUrl', 'Uname', 'title', 'Author', 'SourceCode', 'Description', 
											'Input', 'Output', 'Requirements', 'Usage', 'Example', [], [])
projectId = databaseFunctions.addNewProject('secretUrl', 'Uname', 'title', 'Author', 'SourceCode', 'Description', 
											'Input', 'Output', 'Requirements', 'Usage', 'Example', [], [])
projectId = databaseFunctions.addNewProject('secretUrl', 'Uname', 'title', 'Author', 'SourceCode', 'Description', 
											'Input', 'Output', 'Requirements', 'Usage', 'Example', [], [])
projectId = databaseFunctions.addNewProject('secretUrl', 'Uname', 'title', 'Author', 'SourceCode', 'Description', 
											'Input', 'Output', 'Requirements', 'Usage', 'Example', [], [])
projectId = databaseFunctions.addNewProject('secretUrl', 'Uname', 'title', 'Author', 'SourceCode', 'Description', 
											'Input', 'Output', 'Requirements', 'Usage', 'Example', [], [])
projectId = databaseFunctions.addNewProject('secretUrl', 'Uname', 'title', 'Author', 'SourceCode', 'Description', 
											'Input', 'Output', 'Requirements', 'Usage', 'Example', [], [])
projectId = databaseFunctions.addNewProject('secretUrl', 'Uname', 'title', 'Author', 'SourceCode', 'Description', 
											'Input', 'Output', 'Requirements', 'Usage', 'Example', [], [])
projectId = databaseFunctions.addNewProject('secretUrl', 'Uname', 'title', 'Author', 'SourceCode', 'Description', 
											'Input', 'Output', 'Requirements', 'Usage', 'Example', [], [])
projectId = databaseFunctions.addNewProject('secretUrl', 'Uname', 'title', 'Author', 'SourceCode', 'Description', 
											'Input', 'Output', 'Requirements', 'Usage', 'Example', [], [])



databaseFunctions.addPendingUser('tom@example.com', 'pippy360', 'password')

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

	recentProjectsIds = databaseFunctions.getProjectListRange(0, AMOUNT_OF_MOST_RECENT)
	recentProjects = []
	for projectId in recentProjectsIds:
		recentProjects.append( databaseFunctions.getProjectInfo(projectId) )

	return render_template("index.html", recentProjects=recentProjects, errors=errors)

@app.route("/s/<query>")
@app.route("/s/<query>/")
@login.login_required
def showSearch(query):
	return showSearchPage(query, 0)

@app.route("/s/<query>/<pageNo>")
@app.route("/s/<query>/<pageNo>/")
@login.login_required
def showSearchPage(query, pageNo):
	pageNo = str(pageNo)
	if int(pageNo) < 0:
		return render_template("baseLayout.html", 
			errors=[{'message':'bad page number !','class':'bg-danger'}])

	#get the query
	tags = query.split()
	
	#//get the results with the tags
	#get the intersec of the query	

	genPageButtons(1,0)
	
	return render_template("search.html")

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
			request.form.get('secreturl'), 
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
			[], 
			[])
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

	databaseFunctions.editProject(
			request.form.get('existingId'),
			request.form.get('secreturl'), 
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
			[], 
			[])

	return redirect('/dashboard?success=Success: Service Edited')

@app.route('/removeService/<serviceId>')
@login.login_required
def removeServicePage(serviceId):
	if login.current_user.isAdmin == 'False':
		return redirect('/')

	return redirect('/dashboard?success=Success: Service Added')


@app.route('/acceptUser/<userId>')
@login.login_required
def acceptUserPage(userId):
	if login.current_user.isAdmin == 'False':
		return redirect('/')

	databaseFunctions.moveFromPendingToActive(userId)
	return redirect('/dashboard?success=Success: User Accepted')

@app.route('/rejectUser/<userId>')
@login.login_required
def rejectUserPage(userId):
	if login.current_user.isAdmin == 'False':
		return redirect('/')

	databaseFunctions.removePendingUser(userId)
	return redirect('/dashboard?success=Success: User Rejected')

@app.route("/api/<projectTitle>/")
def projectTitlePage(projectTitle):
	#get the apiKey from the get request and revese proxy the url
	return redirect('/')

@app.route("/r/<projectId>")
@app.route("/r/<projectId>/")
@login.login_required
def showProject(projectId):
	projectInfo = databaseFunctions.getProjectInfo(projectId)
	return render_template("project.html", projectInfo=projectInfo)

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

	#make sure they're non empty

	status = loginLogic.loginUser(userStringId, password)
	print 'status'
	print status
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

		oldPasswordHash = oldPassword;
		if oldPasswordHash != login.current_user.passwordHash:#the old password
			return redirect('/changePassword?error=Error: Wrong Old password.')
		elif newPassword1 != newPassword2:
			return redirect('/changePassword?error=Error: New Passwords didn\'t Match')

		newPasswordHash = newPassword1

		databaseFunctions.changePasswordHash(login.current_user.userId, newPasswordHash)
		return redirect('/dashboard?success=Success: Password Changed')
	else:
		return redirect('/dashboard?error=Error: Password Change Failed, darn it :(')


@app.route("/signupSubmit", methods=['POST'])
def signupSubmitPage():

	#FIXME: also check for empty strings !!
	#FIXME: CHECK IF THE EMIAL IS OK
	email = request.form.get('email')
	if email == None or len(email) > MAX_EMAIL_CHARS:
		return redirect('/login?error=Error: Email was greater than '+str(MAX_EMAIL_CHARS)+' chars')

	password = request.form.get('password')
	if password == None or len(password) > MAX_PASSWORD_CHARS:
		return redirect('/login?error=Error: Password was greater than '+str(MAX_PASSWORD_CHARS)+' chars')

	username = request.form.get('username')
	if username == None or len(username) > MAX_USERNAME_CHARS:
		return redirect('/login?error=Error: Username was greater than '+str(MAX_USERNAME_CHARS)+' chars')

	#hash the password and try to add it to the database
	#for the moment we'll just keep it in glorious plain text :D
	passwordHash = password

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