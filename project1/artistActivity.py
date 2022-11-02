from itertools import count
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
    # this function control the whole flow of what a artist user can do
    artistMenu()
    while True:
        userAction = input(">")
        if (userAction == "1"):
            addSongAction(aid)
            artistMenu()
        elif (userAction == "2"):
            findAction(aid)
            artistMenu()
        elif (userAction == "3"):
            return 1
        elif (userAction == "4"):
            return 0
        else:
            print("please choose from 1,2, 3 or 4")
    return


def addPerformanceInfo(sid, userId):
    '''
    This function will insert all the artiests's aid
    who worked on the song to the perform table
    '''
    sql_commands.insertPerform(userId, sid)
    print("including you, how many artists in total worked on this song?")
    while True:
        try:
            collabNum = input(">")
            collabInt = int(collabNum)
            break
        except ValueError:
            print("please enter an integer")

    if (collabInt > 1):
        print("please enter the id of collabrator artists, one by one")
    for i in range(collabInt-1):
        while True:
            print("enter id, presse return/enter to enter the next id:")
            collabArtistId = input(">")
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
    if (sql_commands.isNewSong(sTitle, sDuration, userId)):
        sId = sql_commands.getTheLastSid()+1
        sql_commands.insertNewSong(sId, sTitle, sDuration)
        addPerformanceInfo(sId, userId)
        print("SUCCESSED! new song added.")
    else:
        print("FAIL TO ADD SONG: This song was already added before!")


def findAction(aid):
    pl = sql_commands.findTopPlaylists(aid)
    countPl = 1
    countF = 1
    print("top 3 playlists that include the largest number of your songs ")
    for each in pl:
        print(countPl, ": ", each[0], " ", each[1])
        countPl = countPl+1
    fans = sql_commands.findTopFans(aid)
    print("top 3 users who listen to your songs the longest time")
    for each in fans:
        print(countF, ": ", each[0], " ", each[1])
        countF = countF + 1
