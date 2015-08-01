import sqlite3

class Database:
    def __init__(self):
        conn = self.connect()
        cursor = conn.cursor()
        sql = 'create table if not exists users (id integer primary key\
               autoincrement, username text not null, password text not null ,\
               admin boolean not null)'
        cursor.execute(sql)
        conn.commit()
        print('Database Created')

    # DATABASE CONNECT
    def connect(self):
        conn = sqlite3.connect('./tmp/database.db')
        conn.row_factory = sqlite3.Row
        return conn

    # GET USER
    def getUser(self, username):
        conn = self.connect()
        cursor = conn.cursor()
        entries = cursor.execute("select username, password, admin from users\
                                  where username = (?)", (username, )).fetchall()
        return entries

    # CREATE USER
    def createUser(self, username, password, admin):
        conn = self.connect()
        cursor = conn.cursor()
        options = [username, password, admin]
        cursor.execute('insert into users (username, password, admin)\
                        values (?, ?, ?)', options)
        conn.commit()

    #EDIT USER
    def editUser(self, userID, username, password, admin):
        conn = self.connect()
        cursor = conn.cursor()
        print ('ID: ' + userID)
        options = [username, password, admin, userID]
        cursor.execute('update users SET username=(?), password=(?), admin=(?)\
                        WHERE id=(?)', options)
        conn.commit()

    #LIST USERS
    def userList(self):
        conn = self.connect()
        cursor = conn.cursor()
        entries = cursor.execute('select id, username, password, admin from\
                                  users order by id desc').fetchall()
        return entries

    #FETCH SPECIFIC
    def fetchSpecific(self, userID, field, database):
        conn = self.connect()
        cursor = conn.cursor()
        options = [userID]
        query = 'select {field} from {database}\
                 where id=(?)'.format(field=field, database=database)
        entries = cursor.execute(query, options).fetchall()
        return entries[0][0];
