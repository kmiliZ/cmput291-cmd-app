import login
import sql_commands


def artistMenu():
    menu = '''
    ARTIST MENU:
    Choose from
    1. Add a song
    2. Find top fans and playlists
    3. Log out
    4. Exit
    '''
    print(menu)


def artistAction(aid):
    artistMenu()
    while True:
        userAction = input()
        if (userAction == "1"):
            addSongAction(aid)
            artistMenu()
        elif (userAction == "2"):
            findAction()
            artistMenu()
        elif (userAction == "3"):
            return 1
        elif (userAction == "4"):
            return 0
        else:
            print("please choose from 1,2 or 3")
    return


def addPerformanceInfo(sid, userId):
    sql_commands.insertPerform(userId, sid)
    collabNum = input(
        "including you, how many artists in total worked on this song?\n")
    print("please enter the id of collabrator artists, one by one")
    for i in range(int(collabNum)-1):
        while True:
            collabArtistId = input(
                "enter id, presse return/enter to enter the next id:")
            if (sql_commands.checkValidAidDB(collabArtistId)):
                sql_commands.insertPerform(collabArtistId, sid)
                break
            print(
                "Invalid artist id. please try enter again")
    return


def addSongAction(userId):
    print("please provide song title and duration")
    sTitle = input("enter song title:")
    sDuration = input("enter song duration:")
    if (sql_commands.isNewSong(sTitle, sDuration)):
        sId = sql_commands.getTheLastSid()+1
        sql_commands.insertNewSong(sId, sTitle, sDuration)
        addPerformanceInfo(sId, userId)
        print("SUCCESSED! new song added.")
    else:
        print("FAIL TO ADD SONG: This song was already added before!")


def findAction():
    print("ad")
