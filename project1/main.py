import sqlite3
import login
import sql_commands




def main():

    path="./prj-test.db"
    sql_commands.connect(path)

    
    userId,isArtiest,isExiting = login.login()
    if (isExiting):
        return 
    print("isArtiest: ",isArtiest)

    
    sql_commands.close()
    return

if __name__ == "__main__":
    main()