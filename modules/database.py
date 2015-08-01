from database_model import db
from database_model import UserModel

class Database:
    def __init__(self):
        db.create_all()
        print('Database Created')


    # CREATE USER
    def createUser(self, username, password, admin):
        newUser = UserModel(username, password, admin)
        db.session.add(newUser)
        db.session.commit()


    #EDIT USER
    def editUser(self, userID, username, password, admin):
        user = UserModel.query.filter_by(id=userID).first()
        if username:
            user.username = username
        if password:
            user.password = password
        user.admin = admin
        db.session.commit()


    # GET USER
    def getUser(self, userName):
        user = UserModel.query.filter_by(username=userName).first()
        return user


    #LIST USERS
    def userList(self):
        users = UserModel.query.all()
        return users
