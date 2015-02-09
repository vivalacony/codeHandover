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

projectId = databaseFunctions.addNewProject("user_id_02", "Some Project About Something", 
	"dicta sunt explicabo."+
	" illum qui dolorem eum fugiat quo voluptas nulla pariatur?", "",
	 "http://github.com/something", "http://wiki.com/somethingElse", 
	 "file_id_001", [ "something", "cats", "nothing", "Ireland", "vague" ])

projectId = databaseFunctions.addNewProject("user_id_02", "A big long project", 
	"dicta sunt explicabo."+
	"qui in ea voluptate velit esse quam nihil molestiae consequatur, vel"+
	" illum qui dolorem eum fugiat quo voluptas nulla pariatur?", "",
	 "http://github.com/something", "http://wiki.com/somethingElse", 
	 "file_id_001", [ "Ireland", "USA", "london" ])

projectId = databaseFunctions.addNewProject("user_id_02", "Cat Chat", 
	"in rescue centres throughout the UK and Ireland", "",
	 "http://github.com/something", "http://wiki.com/somethingElse", 
	 "file_id_001", [ "cats", "chat", "mice", "Ireland" ])

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

@app.route("/r/<projectId>")
@app.route("/r/<projectId>/")
@login.login_required
def showProject(projectId):
	return showIndex()
	#return render_template("index.html")

#TODO: allow editing of projects
@app.route("/r/<projectId>/edit", methods=['POST'])
@login.login_required
def editProject(projectId):
	if request.form.get('postContent'):
		pass
	else:
		pass

@app.route('/projectSubmit', methods=['POST'])
@login.login_required
def projectSubmit():
	threadId = ''
	if request.form.get('subject') != None and request.form.get('comment') != None:
		threadId = databaseFunctions.createThread(boardId, request.form['subject'], 
			request.form['comment'], request)
		return redirect('/thread/'+threadId)
	else:
		return redirect('/')#pass it here and pass on an error message

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
	
	if login.current_user.isAdmin:
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

	if request.form.get('username') != None:
	#	return redirect('/dashboard?success=Success: Username Changed to '+newUsername)
	else:
		return redirect('/dashboard?error=Error: Username Change Failed, darn it :(')
		


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

	return redirect('/dashboard?success=Success: Password Changed')


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