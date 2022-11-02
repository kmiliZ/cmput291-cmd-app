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

# for user activity


def findMaxSno(uid):
    cursor.execute(
        '''select MAX(sno) from sessions where sessions.uid=?''', [uid])
    return cursor.fetchone()


def startSession(uid, sno):
    cursor.execute(
        '''insert into sessions values(?,?,DateTime('now'),null)''', (uid, sno))
    connection.commit()


def endSession(uid, sno):
    cursor.execute(
        '''update sessions set end=DateTime('now') where uid=? and sno=?''', (uid, sno))
    connection.commit()


def getSongById(sid):
    cursor.execute(
        '''select sid, title, duration from songs where sid=?''', [sid])
    return cursor.fetchone()


def getArtistById(aid):
    cursor.execute('''
                   select a.aid, a.name, a.nationality, count(p.sid)
                   from artists a
                   left join perform p on a.aid=p.aid
                   where a.aid=?
                   group by a.aid, a.name, a.nationality
                   ''', [aid])
    return cursor.fetchone()


def getArtistSongsById(aid):
    cursor.execute('''select sid from perform where aid=?''', [aid])
    results = cursor.fetchall()
    tList = []
    for i in results:
        song = getSongById(i[0])
        tList.append((0, "Song", song))
    return tList


def getSondPerformerById(sid):
    cursor.execute(
        '''select a.name from artists a, perform p where p.sid=? and p.aid=a.aid''', [sid])
    return cursor.fetchall()

# returns a list of all playlists the song is in (including other users' playlist)


def getSongPLsById(sid):
    cursor.execute(
        '''select p.title from playlists p, plinclude pl where pl.sid=? and p.pid=pl.pid''', [sid])
    return cursor.fetchall()


def getUserPLsById(uid):
    cursor.execute('''select pid, title from playlists where uid=?''', [uid])
    return cursor.fetchall()


def getMaxPLSorder(pid):
    cursor.execute('''select MAX(sorder) from plinclude where pid=?''', [pid])
    return cursor.fetchone()


def addSongToPLById(sid, pid):
    sorder = None
    result = getMaxPLSorder(pid)
    if (result[0] == None):
        sorder = 0
    else:
        sorder = int(result[0]) + 1
    cursor.execute('''insert into plinclude values(?,?,?)''',
                   (pid, sid, sorder))
    connection.commit()


def getMaxPId():
    cursor.execute('''select MAX(pid) from playlists''')
    return cursor.fetchone()


def addNewPL(uid, title):
    pId = None
    result = getMaxPId()
    if (result[0] == None):
        pId = 0
    else:
        pId = int(result[0]) + 1
    cursor.execute('''insert into playlists values(?,?,?)''',
                   (pId, title, uid))
    connection.commit()
    return pId

# returns true if the song is already in session


def checkSongInSession(uid, sno, sid):
    cursor.execute('''
                   select l.cnt 
                   from listen l 
                   where l.uid=? and l.sno=? and l.sid=?
                   ''', (uid, sno, sid))
    result = cursor.fetchone()
    if (result == None):
        return False
    else:
        return True


def listenById(uid, sno, sid):
    if (checkSongInSession(uid, sno, sid)):
        cursor.execute('''
                       update listen 
                       set cnt=cnt+1 
                       where uid=? and sno=? and sid=?
                       ''', (uid, sno, sid))

    else:
        cursor.execute('''insert into listen values(?,?,?,1)''',
                       (uid, sno, sid))
    connection.commit()


def getPlaylistById(pid):
    statement = '''
    select p.pid, p.title, sum(s.duration)
    from playlists p 
    left join plinclude pl on pl.pid=p.pid
    left join songs s on s.sid=pl.sid
    where p.pid=?
    group by p.pid, p.title
    '''
    cursor.execute(statement, [pid])
    return cursor.fetchone()


def getSongsFromPLById(pid):
    cursor.execute('''
                   select s.sid, s.title, s.duration 
                   from songs s, plinclude pl
                   where pl.pid = ? and pl.sid = s.sid''', [pid])
    results = cursor.fetchall()
    sList = []
    for i in results:
        sList.append((0, "Song", i))
    return sList

# https://www.sqlitetutorial.net/sqlite-like/
# https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
# returns a list tuples (#of matches, Song/Playlist, return from sql)


def searchSandP(list):
    songDict = {}
    playlistDict = {}
    for i in list:
        pattern = "%" + i + "%"
        cursor.execute(
            '''select sid from songs where title like ?''', [pattern])
        results1 = cursor.fetchall()
        for j in results1:
            myId = j[0]
            songDict[myId] = songDict.get(myId, 0) + 1

        cursor.execute(
            '''select pid from playlists where title like ?''', [pattern])
        results2 = cursor.fetchall()
        for k in results2:
            myId = k[0]
            playlistDict[myId] = playlistDict.get(myId, 0) + 1

    tList = []
    for x, y in songDict.items():
        song = getSongById(x)
        tList.append((y, "Song", song))

    for x, y in playlistDict.items():
        playlist = getPlaylistById(x)
        tList.append((y, "PlayList", playlist))

    return tList


def searchA(list):
    artistDict = {}
    for i in list:
        pattern = "%" + i + "%"
        cursor.execute('''
                       select DISTINCT(a.aid) 
                       from artists a 
                       left join perform p on a.aid=p.aid 
                       left join songs s on p.sid=s.sid 
                       where a.name like ? or s.title like ?
                       ''', (pattern, pattern))
        results1 = cursor.fetchall()
        for j in results1:
            myId = j[0]
            artistDict[myId] = artistDict.get(myId, 0) + 1

    tList = []
    for x, y in artistDict.items():
        song = getArtistById(x)
        tList.append((y, "Artist", song))

    return tList


def close():
    connection.commit()
    connection.close()
