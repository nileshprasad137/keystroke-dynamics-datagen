__author__ = 'Tristan Watson'

# Keystroke Dynamic software that covers the following key functionality:
# 1. User File management
# 2. Input gathering and management (including storage)
# 3. Plotting of keystrokes taking into consideration both up events and down events.

import pyHook
import pythoncom
import os
import matplotlib.pyplot as plt
import json
import numpy
import sys

# File is to be opened and closed numerous times. Should be re-written as a class.
global userFilePath

time_between_ups = []
time_between_downs = []


def banner():
    print("------------------------------")
    print("Keystroke Dynamics Software")
    print("Author: Tristan Watson, 2015")
    print("------------------------------")
    print("Current Working Directory: ", os.getcwd())


def menuOptions():
    # Menu
    print("Please choose a following option:")
    print("1: User Login or Create New")
    print("2: Username and Password Input")
    print("3: Plot Graph (Based on Username)")
    print("4: Help")
    print("5: Exit")


def menuHandler():
    choice = input("Please enter option choice: ")
    if choice == "1":
        getUserFileWriteSession()
    elif choice == "2":
        usernamePasswordInput()
    elif choice == "3":
        plotMenu()
    elif choice == "4":
        documentation()
    elif choice == "5":
        print("Program Quitting")
        sys.exit()
    else:
        print("Please select a valid option (1-5)")
        menuHandler()


# For writing events
def getUserFileWriteSession():
    print("File Location: ", os.getcwd())
    username = input("Enter your username: ")
    userFileName = (username + ".txt")

    # If directory DNE.
    if not os.path.isdir((os.path.join("./", "accounts"))):
        # Create it.
        os.makedirs("accounts")

    if os.path.exists(os.path.join("accounts", userFileName)):
        userFile = (os.path.join("accounts", userFileName))
    else:
        print("No File Exists! Creating New User")
        if os.path.exists(os.path.join("accounts", userFileName)):
            print("Username exists! Load it or choose different name")
        else:
            userFile = (os.path.join("accounts", userFileName))
            writeFile = open(userFile, "w")
            # Have to prime a file ready to be used with JSON
            fileSetup = json.dumps([])
            writeFile.write(fileSetup)
            writeFile.close()
            print("User Successfully Created", userFile)
    print("Your account has been created: ", userFile)

    global userFilePath
    userFilePath = userFile


# Used for matplotlib only
def getUserFileReadSession():
    userFileName = input("Username:") + ".txt"
    if os.path.exists(os.path.join("accounts", userFileName)):
        userFile = (os.path.join("accounts", userFileName))
        open(userFile, "r")
        return "File Loaded Successfully"
    else:
        print("Username does not exist")


def plotMenu():
    print("What would you like to plot?")
    print("1. Key Up")
    print("2. Key Down")
    print("3. Back")
    print("4. Quit")
    plotMenuHandler()


def plotMenuHandler():
    plotChoice = input("Choice: ")
    if plotChoice == "1":
        timeBetweenUPS()
    elif plotChoice == "2":
        timeBetweenDOWNS()
    elif plotChoice == "3":
        menuHandler()
    elif plotChoice == "4":
        sys.exit()
    else:
        print("Please Choose Valid Option")


def plotGraph(y):
    userInput = ("Enter if you want to plot KeyUp or KeyDowns")
    data = y
    x = list(range(len(data)))

    # Average
    average = numpy.mean(data)
    # Words Per Minute = (Chr / 5) / Time
    wpm = len(data) / 5

    # MatPlotLib Handling
    plt.title("Time Elapsed Between Down Events")
    plt.ylabel("Key Number")
    plt.ylabel("Milliseconds")
    plt.plot(x, y)
    # Format average display box
    plt.text(5, 35, ("WPM: ", wpm, "Average", average), style='italic',
             bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    plt.show()


def documentation():
    print("The menu works in a way that accepts a corresponding number.")
    print("For example, press 2 to enter information.")
    print("A file must be created or loaded first.")
    print("If not defined, program will exit.")
    print("To end input in option '2'. use ESC character")
    print("Option 3 gives an option to either print out a graph of 'up' or 'down' events")


def userRecordData(eventList):
    userFile = userFilePath

    # Read File to Grab Sessions
    readUserFile = open(userFile, "r")
    testFile = readUserFile.read()
    # print(testFile)
    userSessionList = json.loads(testFile)
    readUserFile.close()

    # Create New Session and Write To File
    writeUserFile = open(userFile, "w")
    newUserEventList = eventList
    userSessionList.append(newUserEventList)
    data = json.dumps(userSessionList)
    writeUserFile.write(data)
    writeUserFile.close()


def timeBetweenUPS():
    # Define the list first
    eventFile = open(userFilePath, "r")
    eventList = json.loads(eventFile.read())
    ups = ([(etype, etime) for etype, etime in eventList[0] if etype == "Up"])

    while len(ups) > 1:
        # Get the time from the tuple
        startTime = ups.pop(0)[1]
        betweenTime = ups[0][1] - startTime
        time_between_ups.append(betweenTime)
        # average = numpy.mean(time_between_downs)
    plotGraph(time_between_ups)


def timeBetweenDOWNS():
    # Define the list first
    eventFile = open(userFilePath, "r")
    eventList = json.loads(eventFile.read())
    downs = ([(etype, etime) for etype, etime in eventList[0] if etype == "Down"])
    while len(downs) > 1:
        startTime = downs.pop(0)[1]  # Get the time from the tuple
        betweenTime = downs[0][1] - startTime
        time_between_downs.append(betweenTime)
        # average = numpy.mean(time_between_downs)
    plotGraph(time_between_downs)


def usernamePasswordInput():
    keyLogger = KeyLogger()

    hookManager = pyHook.HookManager()
    hookManager.KeyDown = keyLogger.keyDownEvent
    hookManager.KeyUp = keyLogger.keyUpEvent
    hookManager.HookKeyboard()

    keyLogger.mainLoop()

    # Unhooks the keyboard, no more data recorded, returns to menu
    hookManager.UnhookKeyboard()


class KeyLogger(object):
    def __init__(self):
        self.enterPressed = False
        self.eventList = []

    def keyDownEvent(self, event):
        self.storeEvent("Down", event)
        return True
        # Fixes Requires Integer Bug (Got Nonetype)

    def keyUpEvent(self, event):
        self.storeEvent("Up", event)
        return True
        # Fixes Requires Integer (Got Nonetype)

    def mainLoop(self):
        while not self.enterPressed:
            pythoncom.PumpWaitingMessages()

    def storeEvent(self, activity, event):
        keystrokeTime = int(event.Time)
        # keystrokeCharacter = chr(event.Ascii)

        self.eventList.append((activity, int(keystrokeTime)))

        # Chosen to use Escape key (ESC) due to input using a similar method
        # Enter Key - KeyCode: 13 Ascii: 13 ScanCode: 28 - ESC = 27 @ Ascii
        if event.Ascii == 27:
            self.enterPressed = True
            userRecordData(self.eventList)


# Starts the program
banner()

# Main Program Loop
while True:
    menuOptions()
    menuHandler()







