# IMPORTS
from flask import Flask, request, redirect, url_for, \
    render_template
import random

# MODULES
from modules.security import Security
from modules.user import User
from modules.database import Database
from modules.garage import Garage
from modules.settings import Settings


# GLOBAL VARIABES
DEBUG = True  # This needs to be commented out in master for security.

# Master login
settings = Settings()
USERNAME = settings.username()
PASSWORD = settings.password()

# Secret Key for sessions
SECRET_KEY = str(random.random())

# Init App
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tmp/database.db'


@app.route('/', methods=['GET'])
# GET - Shows main page
# POST - None
def index():
    if not user.loggedIn():
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
# GET - Shows login page
# POST - Logs user in
def login():
    # Redirects on GET request
    if request.method == 'GET':
        return render_template('login.html')

    # Gets login info from page
    username = request.form['username']
    password = request.form['password']

    # fetches user from database
    databaseUser = database.getUser(username)
    if databaseUser:
        # Checks username and password against the database
        if (username == databaseUser.username and
                security.encrypt(password) == databaseUser.password):
            # Checks if user is temporary and if the date is expired
            if (databaseUser.experationDate != 'False' and
                    user.isExpired(databaseUser.experationDate)):
                # Returns expired message
                error = "Your temporary account has expired."
                return render_template('login.html', error=error)

            # Logs user in
            user.login()
            # Checks if user is admin
            if databaseUser.admin is True:
                # Sets admin status
                user.setAdmin()
            # Returns Index
            return redirect(url_for('index'))

    # Checks if master user
    if (request.form['username'] == app.config['USERNAME'] and
       request.form['password'] == app.config['PASSWORD']):
            # Logs user in
            user.login()
            # Sets admin status
            user.setAdmin()
            # Returns Index
            return redirect(url_for('index'))

    # Returns invalid login message
    error = "Invalid Username or Password."
    return render_template('login.html', error=error, username=username)


@app.route('/logout/', methods=['GET'])
# GET - Logs user out
# POST - None
def logout():
    # Logs user out
    user.logout()
    # Returns index
    return redirect(url_for('index'))


@app.route('/users/', methods=['GET', 'POST'])
# GET - Shows user creation and lists users
# POST - Creates Users
def users():
    # Checks if logged in
    if not user.loggedIn():
        # Returns logged in if not
        return redirect(url_for('login'))

    # Checks if admin
    if not user.isAdmin():
        # Returns index if not
        return redirect(url_for('index'))

    # Checks if GET request
    if request.method == 'GET':
        # Returns users and success message if available
        success = request.args.get('success')
        return render_template('users.html', users=database.userList(),
                               success=success)

    # Get username from page
    username = request.form['username']
    # Gets user from database
    databaseUser = database.getUser(username)
    # Checks if user exists
    if (databaseUser is not None):
        # Returns error message
        error = "User already exists"
        return render_template('users.html', users=database.userList(),
                               error=error)

    # Checks if username is valid
    if (not security.usernameStrength(username)):
        error = "Username must be at least 3 characters long"
        return render_template('users.html', users=database.userList(),
                               error=error)

    # Get password from page
    password = request.form['password']
    # Checks if password is valid
    if security.passwordStrength(password) is True:
        # Encrypts password
        password = security.encrypt(password)
    else:
        # Returns invalid password
        error = "Your password must be at least 6 characters long and\
                 contain a number"
        return render_template('users.html', users=database.userList(),
                               error=error, username=username)

    # Checks if admin is checked
    if request.form.get('adminuser'):
        # A checkbox does not return true or false, so we set it here
        isAdmin = True
    else:
        isAdmin = False

    # Checks if temp user is checked
    if request.form.get('tempuser'):
        # Sets experation date from page
        experationDate = str(request.form.get('dateTmp'))
    else:
        experationDate = 'False'

    # Creates user
    database.createUser(username, password, isAdmin, experationDate)

    # Returns success message
    success = ("%s was created!")
    success = success % username
    return render_template('users.html', users=database.userList(),
                           success=success)


@app.route('/edituser/', methods=['POST'])
# GET - None
# POST - Edits User
def edituser():
    # Checks if the user is logged in
    if not user.loggedIn():
        return redirect(url_for('login'))

    # Checks if the user is an admin
    if not user.isAdmin():
        return redirect(url_for('index'))

    # Get ID and Username
    userID = request.args.get('userID')

    # Checks if username already exists
    username = request.form['username']

    # Gets user from the database
    databaseUser = database.getUser(username)

    # Checks if username already exists
    if (databaseUser is not None):
        # Returns username error message
        error = "User already exists"
        return render_template('users.html', users=database.userList(),
                               error=error)

    # Gets password from the page, already checked in javascript so no
    # checking needs to happen here.
    if request.form['password']:
        # Encrpys the password
        password = security.encrypt(request.form['password'])
    else:
        password = None

    # Checks admin status
    if (request.form.get('adminuser')):
        isAdmin = True
    else:
        isAdmin = False

    # Gets temp checkbox status from page
    tmpStatus = request.form.get('dateTmp')

    # Checks if temp is checked
    if (tmpStatus):
        # Sets experation date
        experationDate = str(tmpStatus)
    else:
        # Uses string for jinja template (May be able to use actual False)
        experationDate = 'False'

    # Edits user, returns true if success
    if database.editUser(userID, username, password, isAdmin, experationDate):

        # Sends success message
        success = 'User Updated!'
        return redirect(url_for('users', success=success))
    else:
        # Sends error message
        error = 'An error has occured.'
        return redirect(url_for('users', error=error))


@app.route('/removeuser/', methods=['POST'])
# GET - None
# POST - Removes the user
def removeuser():
    # Checks if user is logged in
    if not user.loggedIn():
        return redirect(url_for('login'))

    # Checks if user is admin
    if not user.isAdmin():
        return redirect(url_for('index'))

    # Gets user to remove from json object
    userID = request.json['userID']

    # Removes user, returns a message to page if sucessfull
    if database.removeUser(userID):
        return 'success'
    else:
        return 'fail'


@app.route('/toggledoor/', methods=['POST'])
# GET - None
# POST - Toggles the status of the door
def toggledoor():
    # Checks if user is logged in
    if not user.loggedIn():
        return redirect(url_for('login'))

    # Toggles Door
    garage.toggleDoor()

    # Reloads index
    return redirect(url_for('index'))


# INIT the application
if __name__ == "__main__":
    # Class Instances
    security = Security()
    user = User()
    database = Database()
    garage = Garage()

    # Do Stuff
    garage.cleanupRelay()

    # Start The App
    settings = Settings()
    garage.cleanupRelay()
    app.run(host=settings.ipAddress())
