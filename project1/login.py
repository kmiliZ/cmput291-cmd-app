

from sre_constants import SUCCESS
from sql_commands import insertUserDB, checkValidAidDB, checkValidUidDB, checkValidUserPasswordDB, checkValidArtistPasswordDB
import os


def clear():
    os.system('clear')

# TODO: this verify does not work


def verifyPassWord(loginType, uid, pwd):
    if (loginType == "1"):
        while (not checkValidUserPasswordDB(uid, pwd)):
            print(
                "Password incorrect. Please try again, or type exit to return to main menu:")
            pwd = input()
            if (pwd == "exit"):
                return 0
    elif (loginType == "2"):
        while (not checkValidArtistPasswordDB(uid, pwd)):
            print(
                "Password incorrect. Please try again, or type exit to return to main menu:")
            pwd = input()
            if (pwd == "exit"):
                return 0
    return 1


def register():
    clear()
    print("registering new user account")
    userId = input("please enter a unique id:")
    while (checkValidUidDB(userId)):
        print("This id is already taken.")
        userId = input(
            'Please try a different one, or type exit to return to main menu\n')
        if (userId == "exit"):
            return userId, "not registered"
    userName = input("please enter a user name:")
    userPwd = input("please enter a password:")
    insertUserDB(userId, userName, userPwd)
    print("successfully registered!")
    return userId, "1"


def pickLogin():
    logInChoiceLine = '''
    please choose to
    log in as
        1.User
        2.Artist
    '''
    print(logInChoiceLine)
    loginAs = input(">")
    while (loginAs != "1" and loginAs != "2"):
        loginAs = input("wrong input: please choose from 1 or 2\n")
    return loginAs


def inValidID():
    isValidId = False
    while (not isValidId):
        print("Entered id is not valid")
        loginAs = input(
            "press 1 to try again, press 2 to register a new account\n")
        while (loginAs != "1" and loginAs != "2"):
            loginAs = input("wrong input: please choose from 1 or 2\n")
        if (loginAs == "1"):
            id = input("please enter your ID again:\n")
            isValidId = checkValidUidDB(id) or checkValidAidDB(id)
            if (isValidId):
                if (checkValidUidDB(id) and checkValidAidDB(id)):
                    return "3", id
                elif (checkValidUidDB(id)):
                    return "1", id
                elif (checkValidAidDB(id)):
                    return "2", id
        elif (loginAs == "2"):
            return 0, 0


def getUserLogInInfo():
    clear()
    print("log in")
    userId = input("please enter your user id:")
    isValidAid = checkValidAidDB(userId)
    isValidUid = checkValidUidDB(userId)
    if (isValidAid and isValidUid):
        userType = pickLogin()
    elif (not isValidAid and not isValidUid):
        result, id = inValidID()
        if (not result):
            return register()
        elif (result == "3"):
            userType = pickLogin()
        else:
            userType = result
        userId = id
    elif (isValidAid):
        userType = "2"
    elif (isValidUid):
        userType = "1"
    userPwd = input("please enter your password:")
    isVerified = verifyPassWord(userType, userId, userPwd)
    if (isVerified):
        print("SUCCESS ON LOGIN!")
        return userId, userType
    return userId, "not verified"


def login():
    while True:
        welcome = '''

                     welcome!             
                type 1 to login         
                type 2 to register
                type 3 to exit      

        '''

        print(welcome)
        userChoice = input(">")
        isExiting = False

        while (userChoice != "1" and userChoice != "2" and userChoice != "3"):
            userChoice = input("wrong input: please choose from 1, 2 or 3\n")

        if (userChoice == "1"):
            userId, userType = getUserLogInInfo()
            if (userType == "not verified" or userType == "not registered"):
                print("return to main screen")
            else:
                return userId, (userType == "2"), isExiting
        elif (userChoice == "2"):
            userId, userType = register()
            if (userType == "not registered"):
                print("return to main screen")
            else:
                return userId, (userType == "2"), isExiting
        else:
            isExiting = True
            return '0', False, isExiting
