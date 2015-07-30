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
