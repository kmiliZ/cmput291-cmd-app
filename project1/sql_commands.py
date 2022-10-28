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

def insertUserDB(id,name,pwd):
    global connection, cursor
    cursor.execute(''' insert into users values(?,?,?)''',(id,name,pwd))
    connection.commit()

def checkValidUidDB(uid):
    global connection, cursor
    cursor.execute('''select * from users where users.uid=?''',[uid])
    result = cursor.fetchone()
    if result == None:
        return False
    return True

def checkValidAidDB(aid):
    global connection, cursor
    cursor.execute('''select * from artists where artists.aid=?''',[aid])
    result = cursor.fetchone()
    if result == None:
        return False
    return True

def checkValidUserPasswordDB(uid,pwd):
    global connection, cursor
    cursor.execute("select * from users where users.uid='{}' and users.pwd='{}'".format(uid,pwd))
    result = cursor.fetchone()
    if result == None:
        return False
    return True

def checkValidArtistPasswordDB(aid,pwd):
    global connection, cursor
    cursor.execute("select * from artists where aid='{}' and pwd='{}'".format(aid,pwd))
    result = cursor.fetchone()
    if result == None:
        return False
    return True

def close():
    connection.commit()
    connection.close()