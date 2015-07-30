from flask import session
class User:
    def __init__(self):
        print('User Created')

    #LOGIN
    def loggedIn(self):
        if session.get('logged_in') != True:
            return False

    #ISADMIN
    def isAdmin(self):
        if session.get('is_admin') != True:
            return False

    def logout(self):
        session.pop('logged_in', None)
        session.pop('is_admin', None)

    def login(self):
        session['logged_in'] = True

    def setAdmin(self):
        session['is_admin'] = True
