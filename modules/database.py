from database_model import db
from database_model import UserModel
import os


class Database:
    def __init__(self):
        # Checks if database exists and creates it if it doest
        directory = './tmp'
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(directory + "/database.db", "a+") as f:
            if f:
                pass

        db.create_all()

    # Create User
    def createUser(self, username, password, admin, experationDate):
        try:
            newUser = UserModel(username, password, admin, experationDate)
            db.session.add(newUser)
            db.session.commit()
            return True
        except:
            return False

    # Edit User
    def editUser(self, userID, username, password, admin, experationDate):
        try:
            user = self.getUser(None, userID)
            if username:
                user.username = username
            if password:
                user.password = password
            if experationDate is not user.experationDate:
                user.experationDate = experationDate

            user.admin = admin
            db.session.commit()
            return True
        except:
            return False

    # Remove User
    def removeUser(self, userID):
        try:
            user = self.getUser(None, userID)
            db.session.delete(user)
            db.session.commit()
            return True
        except:
            return False

    # Get User
    def getUser(self, username=None, userID=None):
        if username:
            user = UserModel.query.filter_by(username=username).first()
        elif userID:
            user = UserModel.query.filter_by(id=userID).first()
        else:
            user = None
        return user

    # List Users
    def userList(self):
        users = UserModel.query.all()
        return users
