#IMPORTS
from flask import Flask, request, session, g, redirect, url_for, \
     render_template
from security import Security
from user import User
from database import Database
import socket
import time
from flask.views import View
#import RPi.GPIO as GPIO

#GLOBAL VARIABES
DEBUG = True #DONT FORGET TO REMOVE THIS
USERNAME = 'admin'
PASSWORD = 'default'
pinList = [4]
#GPIO.setmode(GPIO.BCM)
app = Flask(__name__)
app.config.from_object(__name__)

##ROUTES
#INDEX
@app.route('/')
def index():
    if user.loggedIn() == False:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


#LOGIN
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        #Database Login
        user = [request.form['username'], security.encrypt(request.form['password'])]
        conn = database.connect()
        cursor = conn.cursor()
        cur = cursor.execute("select username, password, admin from users where username = (?)",(user[0],))
        entries = cur.fetchall()
        for userAccount in entries:
            if (user[0] == userAccount[0] and user[1] == userAccount[1]):
                session['logged_in'] = True
                if userAccount[2] == True:
                    session['is_admin'] = True
                return render_template('index.html')

        #Default Login Information
        if (request.form['username'] == app.config['USERNAME']):
            if (request.form['password'] == app.config['PASSWORD']):
                session['logged_in'] = True
                session['is_admin'] = True
                return redirect(url_for('index'))
        return render_template('login.html', error=True)

    if request.method == 'GET':
        return render_template('login.html')

#LOGOUT
@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('is_admin', None)
    return redirect(url_for('index'))

#USERS
@app.route('/user/', methods=['GET', 'POST'])
def users():
    if user.loggedIn() == False:
        return redirect(url_for('login'))

    conn = database.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        cur = cursor.execute('select username, password, admin from users order by id desc')
        entries = cur.fetchall()
        return render_template('adduser.html', entries=entries)

    isAdmin = False
    if (request.form.get('adminuser') != None):
        isAdmin = True

    cursor.execute('insert into users (username, password, admin) values (?, ?, ?)',
                 [request.form['username'], str(security.encrypt(request.form['password'])) , isAdmin])
    conn.commit()
    return redirect(url_for('index'))

#TOGGLEDOOR
@app.route('/toggledoor/', methods=['POST'])
def toggledoor():
    if user.loggedIn() == False:
        return redirect(url_for('login'))
    toggleDoor()
    return redirect(url_for('index'))

#TOGGLE FUNCTION
def toggleDoor():
    GPIO.output(4, GPIO.LOW)
    time.sleep(.2);
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    cleanupRelay()

#Cleanup PI
def cleanupRelay():
    for i in pinList:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)


if __name__ == "__main__":
    #cleanupRelay()
    security = Security()
    user = User()
    database = Database()
    app.run(host='127.0.0.1')
