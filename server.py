import socket
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import sqlite3
#import RPi.GPIO as GPIO
import time

DATABASE = '/tmp/database.db'
DEBUG = True #DONT FORGET TO REMOVE THIS
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
pinList = [4]
#GPIO.setmode(GPIO.BCM)
app = Flask(__name__)
app.config.from_object(__name__)


#DATABASE
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


#ROUTES
#INDEX
@app.route('/')
def index():
    if (session.get('logged_in') == True):
        return render_template('index.html')
    else:
        return render_template('login.html')

#LOGIN
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        #Database Login
        db = get_db()
        user = [request.form['username'], request.form['password']]
        cur = db.execute('select username, password, admin from users order by id desc')
        entries = cur.fetchall()
        for databaseItem in entries:
            if user[0] == databaseItem[0]:
                if user[1] == databaseItem[1]:
                    session['logged_in'] = True
                    return render_template('index.html')

        #Default Login Information
        if (request.form['username'] == app.config['USERNAME']):
            if (request.form['password'] == app.config['PASSWORD']):
                session['logged_in'] = True
                return redirect(url_for('index'))
        return render_template('login.html', error=True)

    if request.method == 'GET':
        return render_template('login.html')

#LOGOUT
@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index')) 

#USERS
@app.route('/user/', methods=['GET', 'POST'])
def users():
    verifyStatus()
    if request.method == 'GET':
        db = get_db()
        cur = db.execute('select username, password from users order by id desc')
        entries = cur.fetchall()
        return render_template('adduser.html', entries=entries)
    g.db.execute('insert into users (username, password, admin) values (?, ?, ?)',
                 [request.form['username'], request.form['password'], request.form['adminuser']])
    g.db.commit()
    return redirect(url_for('index'))

#TOGGLEDOOR
@app.route('/toggledoor/', methods=['POST'])
def toggledoor():
    verifyStatus()
    #Possibly Useless, Do some testing to make sure this page only accepts "POST" requests
    if request.method == 'GET':
        return redirect(url_for('index'))
    openDoor()
    return redirect(url_for('index'))

#OPENDOOR
def openDoor():
    GPIO.output(4, GPIO.LOW)
    time.sleep(.2); 
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for i in pinList:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)


#VERIFY LOGIN
def verifyStatus():
    if session.get('logged_in') != True:
        return redirect(url_for('login'))

















































if __name__ == "__main__":
   # for i in pinList: 
    #    GPIO.setup(i, GPIO.OUT) 
     #   GPIO.output(i, GPIO.HIGH)
    app.run(host='127.0.0.1') 
