import socket
from _thread import *
import pickle
from game import Game
counter= 1
server = "0.0.0.0"
port = 5555


connected = set()
games = {}
idCount = 0

def startServer():
    #הגדרת socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    #2 people can connect to a game
    s.listen(2)
    #in this point the server is running
    print("Waiting for a connection, Server Started")
    return s

#the thread will run in the backround, dont have to wait for it to finish before starting another connection
def threaded_client(conn, p, gameId):
    global counter
    # משתנה גלובלי של כמות במשחקים
    global idCount
    #returns from network if it's player 0 or 1
    conn.send(str.encode(str(p)))
    counter=counter+1
    print("111",counter)
    reply = ""
    #runs while the client is still connected
    while True:
        try:
            #data= recieved data- reciving data from the connection- recv(4096)- 4096 is the amount of information trying to recieve
            #המידע מתקבל בביטים והדיקוד מפרש אותו למילים
            data = conn.recv(4096).decode()
#parts=data.split(",")
            #cheacking if the game still exists
            if gameId in games:
                game = games[gameId]
                #if while trying to get information from the client I'm not getting anything, I'm disconnecting from the client
                if not data:
                    break
                else:
                    if data == "reset":
                        #if the recieved data== reset, אני מפעילה את הפעולה על המשחק והפעולה מתאחלת את תנועת השחקנים,
                        #the players now went, so they can play another game
                        game.resetWent()
                    elif data != "get":
                        #the player made a move
                        game.play(p, data)
                    #sends the game to the clients, yhe clients are going to use it to make moves
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    #if there is a problem with the game, I'm trying to delete the game
    try:
        del games[gameId]
        #if deleting the game worked, print closing game
        print("Closing Game", gameId)
    except:
        pass
    # מחסירה אחד ממספר המשחקים
    idCount -= 1
    #closing the connection
    conn.close()



def main():
    global idCount
    s= startServer()
    #continuously looking for a connection using a loop
    while True:
        #accepting any income connections, connection, adress
        #conn= an object representing whats connected
        conn, addr = s.accept()
        #will show what ip adress is connecting
        print("Connected to:", addr)

        idCount += 1
        p = 0
        #keeping track of how many games there are
        gameId = (idCount - 1)//2
        #אם יש מספר אי זוגי של משחקים, צריך להתחיל עוד משחק
        if idCount % 2 == 1:
            games[gameId] = Game(gameId)
            print("Creating a new game...")
        #if there is a pairable number of players, I can start a game
        else:
            games[gameId].ready = True
            p = 1

# start_new_thread(threaded_client, (conn, current player, which one of the clients is playing which game))
        start_new_thread(threaded_client, (conn, p, gameId))




main()