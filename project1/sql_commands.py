from sqlite3 import Cursor


def insertUser(id,name,pwd):
    global connection, cursor
    cursor.execute(''' insert into users values(?,?,?)''',(id,name,pwd))
    connection.commit()

def checkValidUid(uid):
    cursor.execute('''select * from users where users.uid=?''',uid)
    result = cursor.fetchone()
    if result == None:
        return False
    return True

def checkValidAid(aid):
    cursor.execute('''select * from artists where artists.aid=?''',aid)
    result = cursor.fetchone()
    if result == None:
        return False
    return True