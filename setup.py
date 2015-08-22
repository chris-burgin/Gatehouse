import socket
import string
import fileinput


print('Welcome to Garage PI!')
print('This setup script will walk you through the setup process.')

# IP Address
IP = raw_input("Is your IP Address " + socket.gethostbyname(
               socket.gethostname()) + "? (Y/N): ").lower()
if IP == "y":
    IP = socket.gethostbyname(socket.gethostname())
else:
    IP = raw_input("Enter your IP ex(192.168.1.113):")


# Master Username and Password
print('')
print('Setup Master Username and Password.')
username = raw_input("Master Username: ")
password = raw_input("Master Password: ")


# SETUP
s = open("./modules/settings.py", "r+")
for line in s.readlines():
    string.replace(line, "IP = '*'", "minnie")
s.close()

counter = 0
for line in fileinput.input('./modules/settings.py', inplace=1):
    counter = counter + 1
    if (counter == 7):
        line.strip()
        print ("        IP = '" + IP + "'")
        continue

    if (counter == 10):
        line.strip()
        print ("        username = '" + username + "'")
        continue

    if (counter == 14):
        line.strip()
        print ("        password = '" + password + "'")
        continue

    print(line),
