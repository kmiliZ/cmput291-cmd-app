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


def insertUserDB(id, name, pwd):
    global connection, cursor
    cursor.execute(''' insert into users values(?,?,?)''', (id, name, pwd))
    connection.commit()


def checkValidUidDB(uid):
    global connection, cursor
    cursor.execute('''select * from users where users.uid=?''', [uid])
    result = cursor.fetchone()
    if result == None:
        return False
    return True


def checkValidAidDB(aid):
    global connection, cursor
    cursor.execute('''select * from artists where artists.aid=?''', [aid])
    result = cursor.fetchone()
    if result == None:
        return False
    return True


def checkValidUserPasswordDB(uid, pwd):
    global connection, cursor
    cursor.execute(
        "select * from users where users.uid='{}' and users.pwd='{}'".format(uid, pwd))
    print("pwd is", pwd)
    result = cursor.fetchone()
    if result == None:
        return False
    return True


def checkValidArtistPasswordDB(aid, pwd):
    global connection, cursor
    cursor.execute(
        "select * from artists where aid='{}' and pwd='{}'".format(aid, pwd))
    result = cursor.fetchone()
    if result == None:
        return False
    return True


def isNewSong(title, duration):
    cursor.execute(
        "select * from songs where title like '{}' and duration={}".format(title, duration))
    result = cursor.fetchone()
    if result == None:
        return True
    return False


def insertNewSong(sid, title, duration):
    global connection, cursor
    cursor.execute(''' insert into songs values(?,?,?)''',
                   (sid, title, duration))
    connection.commit()


def getTheLastSid():
    cursor.execute("select s.sid from songs s order by s.sid DESC LIMIT 1")
    result = cursor.fetchone()
    if result == None:
        return 0
    return result[0]


def insertPerform(aid, sid):
    global connection, cursor
    cursor.execute(''' insert into perform values(?,?)''',
                   (aid, sid))
    connection.commit()


def close():
    connection.commit()
    connection.close()
