#!/usr/bin/env python
# IMPORTS
from flask import Flask, request, redirect, url_for, \
    render_template
import random

# MODULES
from modules.security import Security
from modules.user import User
from modules.database import Database
from modules.garage import Garage


# GLOBAL VARIABES
DEBUG = True   # DONT FORGET TO REMOVE THIS
USERNAME = 'admin'
PASSWORD = 'default'
SECRET_KEY = 'asdfasdf'  # str(random.random())
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tmp/test.db'


@app.route('/', methods=['GET', 'POST'])
def index():
    if not user.loggedIn():
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    databaseUser = database.getUser(username)
    if databaseUser:
        if (username == databaseUser.username and
                security.encrypt(password) == databaseUser.password):

            if (databaseUser.experationDate != 'False' and
                    user.isExpired(databaseUser.experationDate)):
                error = "Your temporary account has expired."
                return render_template('login.html', error=error)

            user.login()
            if databaseUser.admin is True:
                user.setAdmin()
            return redirect(url_for('index'))

    if (request.form['username'] == app.config['USERNAME']):
        if (request.form['password'] == app.config['PASSWORD']):
            user.login()
            user.setAdmin()
            return redirect(url_for('index'))

    error = "Invalid Username or Password."
    return render_template('login.html', error=error, username=username)


@app.route('/logout/')
def logout():
    user.logout()
    return redirect(url_for('index'))


@app.route('/users/', methods=['GET', 'POST'])
def users():
    if not user.loggedIn():
        return redirect(url_for('login'))

    if not user.isAdmin():
        return redirect(url_for('index'))

    if request.method == 'GET':
        success = request.args.get('success')
        return render_template('users.html', users=database.userList(),
                               success=success)

    # Verify Username
    username = str(request.form['username'])
    databaseUser = database.getUser(username)
    if (username is "" or databaseUser is not None):
        error = "Invalid Username!"
        return render_template('users.html', users=database.userList(),
                               error=error)

    # Check Password Strength
    password = request.form['password']
    if security.passwordStrength(password) is False:
        error = "Your password must be at least 6 characters long and\
                 contain a number!"
        return render_template('users.html', users=database.userList(),
                               error=error, username=username)
    else:
        password = security.encrypt(password)

    # Get Admin Status
    if request.form.get('adminuser'):
        isAdmin = True
    else:
        isAdmin = False

    # Get Temp User Status
    if request.form.get('tempuser'):
        experationDate = str(request.form.get('dateTmp'))
    else:
        experationDate = 'False'

    # Create User
    database.createUser(username, password, isAdmin, experationDate)

    success = ("%s was created!")
    success = success % username
    return render_template('users.html', users=database.userList(),
                           success=success)


@app.route('/edituser/', methods=['POST'])
def edituser():
    if not user.loggedIn():
        return redirect(url_for('login'))

    if not user.isAdmin():
        return redirect(url_for('index'))

    # Get ID and Username
    userID = request.args.get('user')
    username = request.form['username']

    # Checks Password and checks it so we dont has a blank password
    if request.form['password']:
        password = security.encrypt(request.form['password'])
    else:
        password = None

    # Get Admin Status
    if (request.form.get('adminuser')):
        isAdmin = True
    else:
        isAdmin = False

    # Get Temp User Status
    if (request.form.get('dateTmp')):
        experationDate = str(request.form.get('dateTmp'))
    else:
        experationDate = 'False'

    # Edits User
    database.editUser(userID, username, password, isAdmin, experationDate)
    success = 'User Updated!'
    return render_template('users.html', success=success)


@app.route('/removeuser/', methods=['POST'])
def removeuser():
    if not user.loggedIn():
        return redirect(url_for('login'))

    if not user.isAdmin():
        return redirect(url_for('index'))

    userID = request.json['userID']

    if database.removeUser(userID):
        return 'success'
    else:
        return 'fail'


@app.route('/toggledoor/', methods=['POST'])
def toggledoor():
    if not user.loggedIn():
        return redirect(url_for('login'))
    garage.toggleDoor()
    return redirect(url_for('index'))


if __name__ == "__main__":
    # garage.cleanupRelay()
    security = Security()
    user = User()
    database = Database()
    garage = Garage()
    app.run(host='192.168.1.102')
