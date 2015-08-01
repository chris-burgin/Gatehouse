from flask import session


class User:
    def __init__(self):
        print('User Created')


    # LOGIN
    def loggedIn(self):
        if session.get('logged_in'):
            return True


    # ISADMIN
    def isAdmin(self):
        if session.get('is_admin'):
            return True


    # LOGOUT
    def logout(self):
        session.pop('logged_in', None)
        session.pop('is_admin', None)


    # LOGIN
    def login(self):
        session['logged_in'] = True


    # SET ADMIN
    def setAdmin(self):
        session['is_admin'] = True
