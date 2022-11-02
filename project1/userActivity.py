import sql_commands
import math

sno = None
userId = None

def userMenu():
    menu = '''
    USER MENU:
    Choose from
    1. Start a session
    2. Search for songs and playlists
    3. Search for artists
    4. Log out
    5. Exit
    '''
    print(menu)

def startSession(uId):
    global sno
    sno = sql_commands.findMaxSno(uId)[0]
    print(sno)
    if(sno == None):
        sno = 0
    else:
        sno += 1
    sql_commands.startSession(uId, sno)

def showSongDetails(sid):
    song = sql_commands.getSongById(sid)
    aList = sql_commands.getSondPerformerById(sid)
    pList = sql_commands.getSongPLsById(sid)
    print('''
          SongId:   {}
          Title:    {}
          Duration: {}
          Performer(s):
          '''.format(song[0], song[1], song[2]))
    for i in aList:
        print(i[0])
    print("Playlists that include this song:\n")
    for j in pList:
        print(j[0])
    input("Enter any key to go back.\n")
    
def addToExistingPL(sid):
    pls = sql_commands.getUserPLsById(userId)
    myLen = len(pls)
    if(myLen == 0):
        print("It is empty.\n")
        return -1
    maxP = math.ceil(myLen/5)
    page = 1
    lastPage = False
    notFinished = True
    while(notFinished):
        start = (page-1)*5
        end = page*5
        if(page == maxP):
            end = myLen
            lastPage = True
        for i in range(start, end):
            print("Index: {:2} ID: {:4} Playlist Title: {}".format(i+1, pls[i][0], pls[i][1]))
        print('''
              Select by entering an index.
              Enter -1 to return to previous menu.
              Page {:3d}/{:3d}
              '''.format(page, maxP))
        if(not lastPage):
            print("Enter 0 for next page.\n")
        
        cmd = int(input(">"))
        if(cmd>end or cmd<-1):
            print("Invalid input!\n")
            continue
        if(cmd == -1):
            return -1
        
        if(cmd==0 and not lastPage):
            page += 1
            continue
        elif(cmd==0 and not lastPage):
            print("This is the last page!\n")
            continue
        
        # a selection is made
        newIdex = cmd + start - 1
        myPId = pls[newIdex][0]
        sql_commands.addSongToPLById(sid, myPId)
        return 0
        
def addToNewPL(sid):
    title = input("Enter a titil for your new Playlist: ")
    myPId = sql_commands.addNewPL(userId, title)
    sql_commands.addSongToPLById(sid, myPId)
        
def addToPlaylist(sid):
    while(True):
        print('''
          Enter 1 to add to an existing playlist
          Enter 2 to add to a new playlist
          Enter -1 to go back
          ''')
        userChoice = input(">")
        if(userChoice == "1"):
            addToExistingPL(sid)
            return 0 
                  
        elif(userChoice == "2"):
            addToNewPL(sid)
            return 0
            
        elif(userChoice == "-1"):
            return -1
        else:
            print("Invalid input -_-!\n")
            continue
        
def songActionMenu():
    menu = '''
    SONGACTION MENU:
    Choose from
    1. Listen to it
    2. See more info
    3. Add to playlist
    -1. Return to prevous menu
    '''
    print(menu)
    
def songAction(sid):
    while(True):
        songActionMenu()
        userChoice = input(">")
        if (userChoice == "1"):
            # listen to it
            if(sno == None):
                startSession(userId)
            sql_commands.listenById(userId, sno, sid)
            print("You just listened to a song ^_^\n")
            
        elif (userChoice == "2"):
            # search for songs and playlists
            showSongDetails(sid)
            continue
            
        elif (userChoice == "3"):
            # add to playlist
            addToPlaylist(sid)
            return 0
            
        elif (userChoice == "-1"):
            # Return to previous menu
            return -1
        else:
            print("Invalid choice!\n")
            continue  
    
def pageDisp(myList):
    myLen = len(myList)
    if(myLen == 0):
        print("It is empty.\n")
        return -1
    
    maxP = math.ceil(myLen/5)
    page = 1
    lastPage = False
    notFinished = True
    while(notFinished):
        start = (page-1)*5
        end = page*5
        if(page == maxP):
            end = myLen
            lastPage = True
        for i in range(start, end):
            if(myList[i][1]=="Song"):
                print("Index {:d} #ofMatch: {:2}  Type: {:<8} Id: {:5} Title: {:15} Duration: {:3}"
                      .format(i+1, myList[i][0], myList[i][1], myList[i][2][0], myList[i][2][1], myList[i][2][2]) )
            elif(myList[i][1]=="PlayList"):
                print("Index {:d} #ofMatch: {:2}  Type: {:<8} Id: {:5} Title: {:15} Total Duration: {:3}"
                      .format(i+1, myList[i][0], myList[i][1], myList[i][2][0], myList[i][2][1], myList[i][2][2]) )
            elif(myList[i][1]=="Artist"):
                print("Index {:d} #ofMatch: {:2}  Type: {:<8} Name: {:15} Nationality: {:15} #ofSongs: {:3}"
                    .format(i+1, myList[i][0], myList[i][1], myList[i][2][1], myList[i][2][2], myList[i][2][3]) )
        print('''
              Select by entering an index.
              Enter -1 to return to previous menu.
              Page {:3d}/{:3d}
              '''.format(page, maxP))
        if(not lastPage):
            print("Enter 0 for next page.\n")
            
        cmd = int(input(">"))
        if(cmd>end or cmd<-1):
            print("Invalid input!\n")
            continue
        if(cmd == -1):
            return -1
        
        if(cmd==0 and not lastPage):
            page += 1
            continue
        elif(cmd==0 and not lastPage):
            print("This is the last page!\n")
            continue
        
        # a selection is made
        newIdex = cmd + start -1
        if(myList[newIdex][1] == "Song"):
            songAction(myList[newIdex][2][0])
            continue
        elif(myList[newIdex][1] == "PlayList"):
            sList = sql_commands.getSongsFromPLById(myList[newIdex][2][0])
            pageDisp(sList)
            continue
        elif(myList[newIdex][1] == "Artist"):
            aList = sql_commands.getArtistSongsById(myList[newIdex][2][0])
            pageDisp(aList)
            continue
    
def searchSandP():
    keyWords = input("Please enter space-separated keywords: ")
    myList = keyWords.split()
    results = sql_commands.searchSandP(myList)
    results = sorted(results, key=lambda x: x[0], reverse=True)
    
    return results
    
def searchA():
    keyWords = input("Please enter space-separated keywords: ")
    myList = keyWords.split()
    results = sql_commands.searchA(myList)
    results = sorted(results, key=lambda x: x[0], reverse=True)
    return results

def userActivity(uId):
    global userId
    userId = uId
    while True:
        userMenu()
        userChoice = input(">")
        if (userChoice == "1"):
            # start a session
            startSession(uId)
        elif (userChoice == "2"):
            # search for songs and playlists
            results = searchSandP()
            pageDisp(results)
        elif (userChoice == "3"):
            # search for artists
            results = searchA()
            pageDisp(results)
        elif (userChoice == "4"):
            # Log out
            sql_commands.endSession(uId, sno)
            return 1
        elif (userChoice == "5"):
            # Exit
            sql_commands.endSession(uId, sno)
            return 0
        else:
            print("Invalid choice!\n")
            continue

