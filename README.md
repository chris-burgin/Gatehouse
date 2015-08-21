#### Still in development, beta coming soon.
## What is this?
PIGARAGE is a dynamic multi user application for controlling your garage door
remotely from anywhere in the world. Its a little more complication but in
return will provide you with a larger feature base.

![Pi Garage Home](http://i.imgur.com/D7vS2HI.png)


## Key Features
#### Multiple Users
One of the key features of PIGARAGE is the ability to have multiple users with
a varying level of control. Below are the different types of users available:
    - Admin User: Add, Remove and Edit users.
    - Normal User: Toggle the garage door.
    - Temporary User: Toggle the garage door, this account expires on a set day.

The concept behind multiple users can be explained in this simple example.
    Your leaving on vacation and billy is watching your house, in the stone
    age you would leave billy a house key. But now you can just give him
    temporary access to open your garage door. If he looses his phone he can
    simply jump on the nearest computer and your cat continues to live. When
    you finally return from your trip billys account automatically expires on
    the date you set.

![Multiple User](http://i.imgur.com/rjRuYSy.png)

This also provides a great set of tools for future expansion of pigarage. Which
include a log to show admin users when the door has been opened and closed. So
you know if billy is actually feeding your cat(s).

#### Secure Login
Pi Garage is centered around the Idea that opening and closing your garage should be a secure operation that only approved parties can operate. Due to this the login system is very important, much time has gone into securing this system and doing countless tests to make sure this system is secured against to the outside world.

But who wants to login every single time they have to open their garage. No one does, because of this each login session will be stored until either this software is restarted or the end user logs out.

![Pigarage Login](http://i.imgur.com/7wxUytC.png)

#### Error Checking
A lot of simple projected created for the raspberry pi are thrown together and
easy to break. This is not the case with PIGARAGE. While I can not guarantee
that there will be no errors I can assure that there has been quite extensive
testing and bug fixing before this beta release. If you find an error please
let me know and I will fix it asap, please also feel free to submit pull
requests with any optimization or bug fixes.



## Installation
#### Dependencies
- Flask ``` $ pip install flask ```
- SQLAlchemy ``` $ pip install SQLAlchemy  ```
- Python 2.7

#### Clone

- ``` $ git clone https://github.com/chrisburgin95/pigarage.git ```

#### Start application
To start this application you can do one of the following.
- ``` $ python server.py ```

or you can run

- ``` $ npm start ```

if you have node installed. The nice thing about using npm start is that if there is an error in your application it will restart as soon as the error is resolved.

If all has worked correctly you should be able to navigate to localhost:4000/ and login using the following

    username: admin
    password: default


#### Customizing
##### Master Login
There are several things that need to be done to secure this application. The first is to change the master username and password. This username and password can never be added or removed and does not show up in the user list.

Open "server.py" and change the following information to be your master username and password. Its very important that you do this, if not your application will be vulnerable.

    USERNAME = 'admin'
    PASSWORD = 'default'

After changing this information restart your application and check to make sure that your new login information works.


##### Server Port
Next we want to change what port our application is listening too. At the bottom of the server.py file find the line that says.

    app.run(host='127.0.0.1')

Change the IP address to that of the local ip of your computer. If you now restart your server you can access your server at the following.

    yourserverslocalip:4000/


#### Connecting your PI
Connect your [Relay](http://www.amazon.com/SainSmart-4-CH-4-Channel-Relay-Module/dp/B0057OC5O8/ref=pd_sim_422_3?ie=UTF8&refRID=0W5N4BWDCDYXT46VJ0D5) to the raspberry pi GPIO 4. Checkout [this](http://www.hobbytronics.co.uk/image/data/tutorial/raspberry-pi/gpio-pinout.jpg) chart to figure out which pin is GPIO 4.


#### Connect to your garage door
This part is fairly simple. Your opener should have a hot wire that when connected to neutral wire will trigger the door to open. I recommend taking a spare piece of wire that is shielded and try connecting the two wired together to test if you have found the correct pair.

When you hit the toggle button in the application the relay that is connected to GPIO 4 will be connected and trigger the two wires will be connected, opening the door.


## Future Features
#### Log
The next logical step in a user based system is to track when users open
and close the garage door. This can be great for parents or if you are
away on vacation with a house sitter(billy).



#### Webcam
This is going to need to be implemented on a user by user basis. I will
add the ability for PIGARAGE to show a webcam photo in the area below the
home button. Each time the home page is loaded PIGARAGE will look for a
a shell file to execute and take a photo that PIGARAGE will load. This is
where its left to the user, I will provide a shell script with support for
common web cam types.

The webcam will be used to show whether the garage door is open or closed,
as you noticed the application says "Toggle Door". I wanted to keep this
simple and avoid purchasing extra equipment to provide an actual status of
the door. I believe it is more important to be able to see the door and the
enviorment around.

Note: If the user has no script written the application will look as currently
presented with no webcam photo.



## Code Notes
My code is not perfect and is in need or organization, this is one of the areas
I will be strongly focusing on before moving forward with more features. My
goals include making sure im not writing code twice and providing a bug free
user experiance.

## Known Bugs
- Users page has more grey area above the login than below.
