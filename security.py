from flask import session
class Security:
    def __init__(self):
        print('Security Created')

    def loggedIn(self):
        if session.get('logged_in') != True:
            return False

    def isAdmin():
        if session.get('is_admin') != True:
            return False
