from flask import session
from datetime import datetime
import string


class User:

    # Logged In
    def loggedIn(self):
        if session.get('logged_in'):
            return True
        else:
            return False

    # Experation
    def isExpired(self, date):
        now = datetime.now()
        experationDate = self.formatDate(str(date))
        currentDate = str(now.strftime('%Y%m%d'))
        print ('current date ' + str(currentDate))
        print ('experation date ' + str(experationDate))
        if int(experationDate) <= int(currentDate):
            return True
        else:
            return False

    # Is Admin
    def isAdmin(self):
        if session.get('is_admin'):
            return True
        else:
            return False

    # Logout
    def logout(self):
        session.pop('logged_in', None)
        session.pop('is_admin', None)

    # Login
    def login(self):
        session['logged_in'] = True

    # Set Admin
    def setAdmin(self):
        session['is_admin'] = True

    # Forman Date
    def formatDate(self, date):
        all = string.maketrans('', '')
        nodigs = all.translate(all, string.digits)
        date = date.translate(all, nodigs)
        return date
