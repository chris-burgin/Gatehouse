import json


class Settings:
    __IP = None
    __username = None
    __password = None
    __pinList = None
    __inputPin = None
    __activeSensors = None

    def __init__(self):
        try:
            with open('./config.json', "r") as outfile:
                data = json.load(outfile)
                self.__IP = data['ip']
                self.__username = data['username']
                self.__password = data['password']
                self.__pinList = data['pinList']
                self.__inputPin = data['inputPin']
                self.__activeSensors = data['activeSensors']
                print self.__activeSensors
        except:
            # Fallbacks
                self.__IP = '127.0.0.1'
                self.__username = 'admin'
                self.__password = 'default'
                self.__pinlist = [4]

    def ipAddress(self):
        return self.__IP

    def username(self):
        return self.__username

    def password(self):
        return self.__password

    def pinList(self):
        return self.__pinList

    def inputPin(self):
        return self.__inputPin

    def activeSensors(self):
        return self.__activeSensors
