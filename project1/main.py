import sqlite3
import login
import sql_commands
import artistActivity
import userActivity


def main():

    path = "./prj-test.db"  # this should not be hard coded
    # path = input("please enter db path:")
    sql_commands.connect(path)
    while True:
        userId, isArtiest, isExiting = login.login()
        if (isExiting):
            break
        if (isArtiest):
            # artistAction return false if user chose the option to exit
            # returns true if user chose to log out
            isReturningtoMainMenu = artistActivity.artistAction(userId)
        else:
            isReturningtoMainMenu = userActivity.userActivity(userId)
        if (not isReturningtoMainMenu):
            break

    sql_commands.close()
    return


if __name__ == "__main__":
    main()
