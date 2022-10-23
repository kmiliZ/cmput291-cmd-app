



def printLoginMenu():
    welcome = '''
    ##################################
    ############ welcome! ############
    ##      type 1 to login         ##
    ##      type 2 to register      ##
    ##################################
    ##################################
    '''

    print(welcome)
    userChoice = input()

    while (userChoice != "1" and userChoice != "2"):
        userChoice = input("wrong input: please choose from 1 or 2\n")

    if(userChoice == "1"):
        getUserInto()
    elif(userChoice == "2"):
        register()


def getUserInto():
    print("log in")
    userId = input("please enter your user id:")
    userPwd= input("please enter your password:")
    return 0

def register():
    print("registering new user account")
    userId = input("please enter a unique id:")
    userName= input("please enter a user name:")
    userPwd= input("please enter a password:")

    return 0

def main():
    printLoginMenu()

if __name__ == "__main__":
    main()
