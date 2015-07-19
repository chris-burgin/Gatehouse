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

def connect_db():
    """Connects to the specific database."""
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
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.route('/')
def index():
    if session.get('logged_in') == True:
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None;
    if request.method == 'POST':
        db = get_db()
        userFound = False;
        user = [request.form['username'], request.form['password']]
        cur = db.execute('select username, password from users order by id desc')
        entries = cur.fetchall()
        for item in entries:
            if user[0] == item[0]:
                if user[1] == item[1]:
                    userFound = True;
                    break

        if userFound == True:
            session['logged_in'] = True
            return render_template('index.html')

        if request.form['username'] != app.config['USERNAME']:
            error = 'invalid'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'invalid'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('login.html', error=error)
   
    if request.method == 'GET' and session.get('logged_in') == True:
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index')) 

@app.route('/user/', methods=['GET', 'POST'])
def users():
    if session.get('logged_in') != True:
        return redirect(url_for('login'))

    if request.method == 'GET':
        db = get_db()
        cur = db.execute('select username, password from users order by id desc')
        entries = cur.fetchall()
        return render_template('adduser.html', entries=entries)

    g.db.execute('insert into users (username, password) values (?, ?, ?)',
                 [request.form['username'], request.form['password'], request.form['adminuser']])
    g.db.commit()
    return redirect(url_for('index'))

@app.route('/toggledoor/', methods=['GET', 'POST'])
def toggledoor():
    if session.get('logged_in') != True:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return redirect(url_for('index'))

    #GPIO.output(4, GPIO.LOW)
    #time.sleep(.2);
    #doorcleanup(); 
    return redirect(url_for('index'))

def doorcleanup():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for i in pinList:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)

if __name__ == "__main__":
   # for i in pinList: 
    #    GPIO.setup(i, GPIO.OUT) 
     #   GPIO.output(i, GPIO.HIGH)
    app.run(host='127.0.0.1') 
