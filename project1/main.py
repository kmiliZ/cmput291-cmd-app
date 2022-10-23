import sqlite3

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return



def main():
    global connection, cursor

    path="./q1.db"
    connect(path)

    


    
    connection.commit()
    connection.close()
    return

if __name__ == "__main__":
    main()