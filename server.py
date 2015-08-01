#  IMPORTS
from flask import Flask, request, session, g, redirect, url_for, \
     render_template
from security import Security
from user import User
from database import Database
from garage import Garage
import socket
import random
import time
from flask.ext.sqlalchemy import SQLAlchemy

# GLOBAL VARIABES
DEBUG = True   # DONT FORGET TO REMOVE THIS
USERNAME = 'admin'
PASSWORD = 'default'
SECRET_KEY = 'hi' #str(random.random())
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tmp/test.db'



@app.route('/', methods=['GET'])
def index():
    if user.loggedIn() == False:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        requestedLogin = [request.form['username'],
                          security.encrypt(request.form['password'])]

        databaseUser = database.getUser(requestedLogin[0])
        if databaseUser:
            if (requestedLogin[0] == databaseUser.username and
                    requestedLogin[1] == databaseUser.password):
                user.login()
                if databaseUser.admin == True:
                    user.setAdmin()
                return redirect(url_for('index'))

            # Default Login Information
        if (request.form['username'] == app.config['USERNAME']):
            if (request.form['password'] == app.config['PASSWORD']):
                user.login()
                user.setAdmin()
                return redirect(url_for('index'))
        return render_template('login.html', error=True)

    if request.method == 'GET':
        return render_template('login.html')


@app.route('/logout/')
def logout():
    user.logout()
    return redirect(url_for('index'))


@app.route('/user/', methods=['GET', 'POST'])
def users():
    if user.loggedIn() == False:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('adduser.html', users=database.userList())

    if (request.form.get('adminuser')):
        isAdmin = True
    else:
        isAdmin = False

    database.createUser(request.form['username'],
                        security.encrypt(request.form['password']),
                        isAdmin)
    return redirect(url_for('index'))


@app.route('/edituser/', methods=['POST'])
def edituser():
    userID = request.args.get('user')
    username = request.form['username']

    if request.form['password']:
        password = security.encrypt(request.form['password'])
    else:
        password = None

    if (request.form.get('adminuser')):
        isAdmin = True
    else:
        isAdmin = False

    database.editUser(userID, username, password, isAdmin)
    return redirect(url_for('users'))


@app.route('/toggledoor/', methods=['POST'])
def toggledoor():
    if user.loggedIn() == False:
        return redirect(url_for('login'))
    garage.toggleDoor()
    return redirect(url_for('index'))


if __name__ == "__main__":
    # garage.cleanupRelay()
    security = Security()
    user = User()
    database = Database()
    garage = Garage()
    app.run(host='127.0.0.1')
