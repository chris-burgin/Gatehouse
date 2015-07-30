import sqlite3
class Database:
    def __init__(self):
        conn = self.connect()
        cursor = conn.cursor()
        sql = 'create table if not exists users (id integer primary key autoincrement, username text not null, password text not null , admin boolean not null)'
        cursor.execute(sql)
        conn.commit()
        print('Database Created')

    #DATABASE CONNECT
    def connect(self):
        conn = sqlite3.connect('./tmp/database.db')
        conn.row_factory = sqlite3.Row
        return conn

    #DATABASE
    def getUser(self, username):
        conn = self.connect()
        cursor = conn.cursor()
        cur = cursor.execute("select username, password, admin from users where username = (?)",(username,))
        return cur.fetchall()
