from flask import session
from datetime import datetime


class User:

    # LOGGED IN
    def loggedIn(self):
        if session.get('logged_in'):
            return True
        else:
            return False

    # EXPIRATION
    def isExpired(self, date):
        now = datetime.now()
        experationDate = datetime.strptime(date, '%Y-%m-%d')
        currentDate = datetime.strptime(now.strftime('%Y-%m-%d'), '%Y-%m-%d')

        if experationDate <= currentDate:
            return True
        else:
            return False

    # ISADMIN
    def isAdmin(self):
        if session.get('is_admin'):
            return True
        else:
            return False

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
