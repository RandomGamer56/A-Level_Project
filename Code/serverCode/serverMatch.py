import socket
import threading
import json
import mysql.connector
from player import Player
from mapFunctions import *
from serverConstants import *

matchSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
matchSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)

try:
    matchSocket.bind((serverAddr, matchServerPort))
except socket.error as e:
    print(e)

matchSocket.listen(2)
print("Waiting for connection, Server Running")

def game_graphics_threaded_client(connection, currentPlayerList, gameInstance, gameID, serverID):
    players = []
    currentPlayer = ""
    try:
        players = gameInstance.players
        currentPlayer = currentPlayerList[0]
        currentPlayerID = currentPlayerList[1]
        playerDict = dict(players[currentPlayer])
        playerDict["gameID"] = gameID
        playerDict["serverID"] = serverID
        playerData = json.dumps(playerDict)
        playerSend = f"{len(playerData):<{serverHeader}}" + playerData
        connection.sendall(bytes(playerSend, 'utf-8'))
    except socket.error as e:
        print(e)

    while not gameInstance.full:
        try:
            playerDict = {"playerCount": gameInstance.playerCount}
            playerData = json.dumps(playerDict)
            playerSend = f"{len(playerData):<{serverHeader}}" + playerData
            connection.sendall(bytes(playerSend, 'utf-8'))

            full_data = ""
            new_data = True
            message_finish = False
            dataLen = 0
            data = ""
            while not message_finish:
                data = connection.recv(2048)
                if new_data:
                    # print(f"New message length: {data[:serverHeader]}")
                    dataLen = int(data[:serverHeader])
                    new_data = False
                full_data += data.decode("utf-8")
                if len(full_data) - serverHeader == dataLen:
                    data = full_data[serverHeader:]
                    message_finish = True
        except socket.error as e:
            print(e)

    playerDict = {"playerCount": gameInstance.playerCount}
    playerData = json.dumps(playerDict)
    playerSend = f"{len(playerData):<{serverHeader}}" + playerData
    connection.sendall(bytes(playerSend, 'utf-8'))

    full_data = ""
    new_data = True
    message_finish = False
    dataLen = 0
    data = ""
    while not message_finish:
        data = connection.recv(2048)
        if new_data:
            # print(f"New message length: {data[:serverHeader]}")
            dataLen = int(data[:serverHeader])
            new_data = False

        full_data += data.decode("utf-8")

        if len(full_data) - serverHeader == dataLen:
            data = full_data[serverHeader:]
            break
    dataJson = json.loads(data)

    gameMap = CellularAutomataMap(60, 60, 0.4)
    gameMap.create_map()
    gameMap.generation(38)

    try:
        playerDict = {"map": gameMap.map}
        playerData = json.dumps(playerDict)
        playerSend = f"{len(playerData):<{serverHeader}}" + playerData
        connection.sendall(bytes(playerSend, 'utf-8'))

        full_data = ""
        new_data = True
        message_finish = False
        dataLen = 0
        data = ""
        while not message_finish:
            data = connection.recv(2048)
            if new_data:
                # print(f"New message length: {data[:serverHeader]}")
                dataLen = int(data[:serverHeader])
                new_data = False

            full_data += data.decode("utf-8")

            if len(full_data) - serverHeader == dataLen:
                data = full_data[serverHeader:]
                break
    except socket.error as e:
        print(e)

    while True:
        try:
            print("listening")
            full_data = ""
            new_data = True
            message_finish = False
            dataLen = 0
            data = ""
            while not message_finish:
                data = connection.recv(2048)
                if new_data:
                    #print(f"New message length: {data[:serverHeader]}")
                    dataLen = int(data[:serverHeader])
                    new_data = False

                full_data += data.decode("utf-8")

                if len(full_data) - serverHeader == dataLen:
                    data = full_data[serverHeader:]
                    message_finish = True
            dataJson = json.loads(data)
            print(dataJson)
            dataPlayer = Player(dataJson["x"], dataJson["y"], dataJson["height"], dataJson["width"], dataJson["colour"])
            players[currentPlayer] = dataPlayer

            if not data:
                print("Disconnected")
                break
            else:
                if currentPlayer == 1:
                    reply = players[0]
                else:
                    reply = players[1]
            print(reply)
            replyDict = dict(reply)
            replyData = json.dumps(replyDict)
            replySend = f"{len(replyData):<{serverHeader}}" + replyData
            connection.sendall(bytes(replySend,'utf-8'))
        except ConnectionResetError and ValueError:
            break

    print("Lost connection")
    connection.close()

currentPlayer = 0

class threadServer:
    def __init__(self):
        self.players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,255,0))]
        self.playerCount = 0
        self.full = False

threadServerList = []
threadList = []
threadCount = 0
threadServerList.append(threadServer())
threadServerCount = 1

while True:
    conn, addr = matchSocket.accept()
    print("Connected to:",addr)
    currentPlayerID = ""

    try:
        full_data = ""
        new_data = True
        message_finish = False
        data = ""
        dataLen = 0
        while not message_finish:
            data = conn.recv(2048)
            if new_data:
                # print(f"New message length: {data[:serverHeader]}")
                dataLen = int(data[:serverHeader])
                new_data = False

            full_data += data.decode("utf-8")

            if len(full_data) - serverHeader == dataLen:
                data = full_data[serverHeader:]
                message_finish = False
                new_data = True
                full_data = ""
                break

        dataJson = json.loads(data)
        dataFinal = list(dataJson[list(dataJson)[0]])
        currentPlayerID = dataFinal[0]

    except ConnectionResetError:
        pass

    threadCount += 1

    threadList.append(threading.Thread(target=game_graphics_threaded_client,
                                       args=(conn,
                                             (currentPlayer,currentPlayerID),
                                             threadServerList[threadServerCount-1],
                                             threadCount,
                                             threadServerCount),
                                       daemon=True))

    threadList[threadCount-1].start()

    threadServerList[threadServerCount-1].playerCount += 1
    currentPlayer += 1
    if threadServerList[threadServerCount-1].playerCount == 2:
        threadServerList.append(threadServer())
        threadServerList[threadServerCount-1].full = True
        threadServerCount += 1
        currentPlayer = 0
