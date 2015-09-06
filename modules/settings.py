import json


class Settings:
    __IP = None
    __username = None
    __password = None

    def __init__(self):

        try:
            with open('./config.json', "r") as outfile:
                data = json.load(outfile)
                self.__IP = data['ip']
                self.__username = data['username']
                self.__password = data['password']
        except:
            # Fallbacks
                self.__IP = '127.0.0.1'
                self.__username = 'admin'
                self.__password = 'default'

    def ipAddress(self):
        return self.__IP

    def username(self):
        return self.__username

    def password(self):
        return self.__password
