from database_model import db
from database_model import UserModel


class Database:
    def __init__(self):
        db.create_all()

    # CREATE USER
    def createUser(self, username, password, admin, experationDate):
        newUser = UserModel(username, password, admin, experationDate)
        db.session.add(newUser)
        db.session.commit()

    # EDIT USER
    def editUser(self, userID, username, password, admin, experationDate):
        user = self.getUser(None, userID)
        if username:
            user.username = username
        if password:
            user.password = password
        if experationDate:
            user.experationDate = experationDate
        user.admin = admin
        db.session.commit()

    def removeUser(self, userID):
        user = self.getUser(None, userID)
        db.session.delete(user)
        db.session.commit()

    # GET USER
    def getUser(self, username=None, userID=None):
        if username:
            user = UserModel.query.filter_by(username=username).first()
        elif userID:
            user = UserModel.query.filter_by(id=userID).first()
        else:
            user = None

        return user

    # LIST USERS
    def userList(self):
        users = UserModel.query.all()
        return users
