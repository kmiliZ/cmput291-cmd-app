import sqlite3
import login
import sql_commands
import artistActivity
import userActivity


def main():

    path = "./prj-test.db"
    sql_commands.connect(path)
    while True:

        userId, isArtiest, isExiting = login.login()
        if (isExiting):
            break
        if (isArtiest):
            isReturningtoMainMenu = artistActivity.artistAction(userId)
        else:
            isReturningtoMainMenu = userActivity.userMenu(userId)
        if (not isReturningtoMainMenu):
            break

    sql_commands.close()
    return


if __name__ == "__main__":
    main()
