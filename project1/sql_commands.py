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

# for log in


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

# for artist activity


def isNewSong(title, duration, aid):
    cursor.execute(
        "select * from songs join perform on songs.sid=perform.sid where songs.title like '{}' and songs.duration={} and perform.aid={}".format(title, duration, aid))
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

# top 3 users who listen to artist's songs the longest time


def findTopFans(aid):
    statement = '''select users.uid,users.name from users
   join listen on listen.uid = users.uid
   join songs on songs.sid = listen.sid
   join perform on perform.sid = songs.sid
   where perform.aid ='{}'
   group by users.uid,users.name
   order by sum(songs.duration * listen.cnt) DESC
   limit 3'''
    cursor.execute(statement.format(aid))
    allFans = cursor.fetchall()
    return allFans

# top 3 playlists that include the largest number of their songs


def findTopPlaylists(aid):
    statement = '''select pl.pid,playlists.title from plinclude pl join
    perform p on pl.sid = p.sid
    join playlists on playlists.pid = pl.pid
    where p.aid = '{}'
    group by pl.pid,playlists.title
    order by count(pl.sid) DESC
    limit 3'''
    cursor.execute(statement.format(aid))
    allTopPlayLists = cursor.fetchall()
    return allTopPlayLists


def close():
    connection.commit()
    connection.close()
