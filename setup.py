import socket
import json


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
print("Setup Master Username and Password.")
username = raw_input("Master Username: ")
password = raw_input("Master Password: ")

print("Other Settings")
activeSensors = raw_input("Will you have sensors connected? (Y/N): ").lower()
if activeSensors == "y":
    activeSensors = True
else:
    activeSensors = False

# Write to config
with open('config.json', "r+") as outfile:
    data = json.load(outfile)
    outfile.seek(0)
    outfile.truncate()
    data['username'] = username
    data['password'] = password
    data['ip'] = IP
    data['activeSensors'] = activeSensors
    json.dump(data, outfile)
