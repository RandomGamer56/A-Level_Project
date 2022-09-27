import socket
from _thread import *
import json
import mysql.connector
from serverConstants import *
from serverGeneralConnections import *

mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mainSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)

try:
    mainSocket.bind((serverAddr, mainServerPort))
except socket.error as e:
    print(e)

mainSocket.listen()
print("Waiting for connection, Server Running")

players = []

currentPlayer = 0


def database_threaded_client(conn, currentPlayerList):
    while True:
        try:
            command = ""
            commandLen = 1
            fullCommand = ""
            newCommand = True
            finishCommand = False
            while not finishCommand:
                data = conn.recv(2048)
                if newCommand:
                    commandLen = int(data[:serverHeader])
                    newCommand = False

                fullCommand += data.decode("utf-8")

                if len(fullCommand) - serverHeader == commandLen:
                    command = fullCommand[serverHeader:]
                    break

            if not command:
                print("Disconnected")
                break

            else:
                command = json.loads(command)["command"]

                ###REMEMBER TO SEND THESE BACK###

                result = leaderboardMain(command)

                resultDict = {"result": result}
                resultData = json.dumps(resultDict)
                resultSend = f"{len(resultData):<{serverHeader}}" + resultData
                conn.send(bytes(resultSend, 'utf-8'))

        except ValueError:
            players.remove(currentPlayerList[1])
            break

        except:
            break

    print("Lost Connection")
    conn.close()


while True:
    connectionError = False
    dataFinal = []
    conn, addr = mainSocket.accept()
    print("Connected to:", addr)
    try:
        full_data = ""
        new_data = True
        message_finish = False
        dataLen = 0
        data = ""
        while not message_finish:
            data = conn.recv(2048)
            if new_data:
                # print(f"New message length: {data[:header]}")
                dataLen = int(data[:serverHeader])
                new_data = False

            full_data += data.decode("utf-8")

            if len(full_data) - serverHeader == dataLen:
                data = full_data[serverHeader:]
                break

        dataJson = json.loads(data)
        dataIndex = list(dataJson)[0]
        dataFinal = list(dataJson[dataIndex])

    except ValueError:
        connectionError = True
        pass

    except error as e:
        print(e)
        conn.close()
        break

    if not connectionError:

        playerDatabase = []

        if dataFinal[0] == "logIn":
            playerDatabase = logInMain(dataFinal)
        else:
            playerDatabase = logInMain(dataFinal)

        playerDict = {"result": playerDatabase}
        playerData = json.dumps(playerDict)
        playerSend = f"{len(playerData):<{serverHeader}}" + playerData
        conn.send(bytes(playerSend, 'utf-8'))

        players.append(playerDatabase[1][1])

        start_new_thread(database_threaded_client, (conn, playerDatabase[1]))
        currentPlayer += 1
        if currentPlayer == 2:
            currentPlayer = 0
