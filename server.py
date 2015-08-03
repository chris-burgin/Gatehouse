#  IMPORTS
from flask import Flask, request, session, g, redirect, url_for, \
     render_template
import socket, random, time

#MODULES
from modules.security import Security
from modules.user import User
from modules.database import Database
from modules.garage import Garage

from flask.ext.sqlalchemy import SQLAlchemy

# GLOBAL VARIABES
DEBUG = True   # DONT FORGET TO REMOVE THIS
USERNAME = 'admin'
PASSWORD = 'default'
SECRET_KEY = '234fse4234gdb' #str(random.random())
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tmp/test.db'



@app.route('/', methods=['GET'])
def index():
    if not user.loggedIn():
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    requestedLogin = [request.form['username'], request.form['password']]

    databaseUser = database.getUser(requestedLogin[0])
    if databaseUser:
        if (requestedLogin[0] == databaseUser.username and
                security.encrypt(requestedLogin[1]) == databaseUser.password):

            if (databaseUser.experationDate != 'False' and
                    user.isExpired(databaseUser.experationDate)):
                return render_template('login.html', expired=True)

            user.login()
            if databaseUser.admin == True:
                user.setAdmin()
            return redirect(url_for('index'))

    if (request.form['username'] == app.config['USERNAME']):
        if (request.form['password'] == app.config['PASSWORD']):
            user.login()
            user.setAdmin()
            return redirect(url_for('index'))
    return render_template('login.html', error=True)



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
        return render_template('users.html', users=database.userList())

    if request.form.get('adminuser'):
        isAdmin = True
    else:
        isAdmin = False

    if request.form.get('tempuser'):
        experationDate = str(request.form.get('dateTmp'))
    else:
        experationDate = 'False'

    database.createUser(request.form['username'],
                        security.encrypt(request.form['password']),
                        isAdmin, experationDate)
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

    experationDate = str(request.form.get('dateTmp'))
    database.editUser(userID, username, password, isAdmin, experationDate)
    return redirect(url_for('users'))


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
    app.run(host='127.0.0.1')
