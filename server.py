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

# GLOBAL VARIABES
DEBUG = True   # DONT FORGET TO REMOVE THIS
USERNAME = 'admin'
PASSWORD = 'default'
SECRET_KEY = str(random.random())
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    if user.loggedIn() == False:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        # Database Login
        requestedLogin = [request.form['username'],
                          security.encrypt(request.form['password'])]

        entries = database.getUser(requestedLogin[0])
        for userAccount in entries:
            if (requestedLogin[0] == userAccount[0] and
                    requestedLogin[1] == userAccount[1]):
                user.login()
                if userAccount[2] == True:
                    user.setAdmin()
                return render_template('index.html')

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

    conn = database.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        cur = cursor.execute('select username, password, admin from\
                              users order by id desc')
        entries = cur.fetchall()
        return render_template('adduser.html', entries=entries)

    isAdmin = False
    if (request.form.get('adminuser') != None):
        isAdmin = True
        
    database.createUser(request.form['username'],
                        str(security.encrypt(request.form['password'])),
                        isAdmin)
    return redirect(url_for('index'))


@app.route('/toggledoor/', methods=['POST'])
def toggledoor():
    if user.loggedIn() == False:
        return redirect(url_for('login'))
    garage.toggleDoor()
    return redirect(url_for('index'))


if __name__ == "__main__":
    # cleanupRelay()
    security = Security()
    user = User()
    database = Database()
    garage = Garage()
    app.run(host='127.0.0.1')
