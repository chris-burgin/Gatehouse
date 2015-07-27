from flask import Flask, request, session, g, redirect, url_for, \
     render_template
import sqlite3
import socket
import time
#import RPi.GPIO as GPIO

DATABASE = './tmp/database.db'
DEBUG = True #DONT FORGET TO REMOVE THIS
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
pinList = [4]
#GPIO.setmode(GPIO.BCM)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

#DATABASE
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'create table if not exists users (id integer primary key autoincrement, username text not null, password text not null, admin boolean not null)'
    cursor.execute(sql)
    conn.commit()

#ROUTES
#INDEX
@app.route('/')
def index():
    if loggedIN() == False:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')
    

#LOGIN
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        #Database Login
        user = [request.form['username'], request.form['password']]
        conn = connect_db()
        cursor = conn.cursor()
        cur = cursor.execute('select username, password, admin from users order by id desc')
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
    return redirect(url_for('index')) 

#USERS
@app.route('/user/', methods=['GET', 'POST'])
def users():
    if loggedIN() == False:
        return redirect(url_for('login'))

    conn = connect_db()
    cursor = conn.cursor()
    if request.method == 'GET':
        cur = cursor.execute('select username, password, admin from users order by id desc')
        entries = cur.fetchall()
        return render_template('adduser.html', entries=entries)

    isAdmin = False
    if (request.form.get('adminuser') != None):
        isAdmin = True
    cursor.execute('insert into users (username, password, admin) values (?, ?, ?)',
                 [request.form['username'], request.form['password'], isAdmin])
    conn.commit()
    return redirect(url_for('index'))

#TOGGLEDOOR
@app.route('/toggledoor/', methods=['POST'])
def toggledoor():
    if loggedIN() == False:
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

def cleanupRelay():
    for i in pinList:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)


#VERIFY LOGIN
def loggedIN():
    if session.get('logged_in') != True:
        return False


if __name__ == "__main__":
    #cleanupRelay()
    init_db()
    app.run(host='127.0.0.1') 
