import time

from player import Player
import socket
import json

class gameNetwork:
    def __init__(self,playerID):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1" #"10.16.164.33" #"82.129.111.198"
        self.port = 5556
        self.header = 64
        self.addr = (self.server, self.port)
        self.id = playerID
        self.p,self.threadID,self.serverID = self.connect()
        print(self.p)

    def getP(self):
        return self.p

    def getPlayerCount(self):
        try:
            full_msg = ""
            new_msg = True
            message_finish = False
            message = ""
            msglen = 0
            while not message_finish:
                message = self.client.recv(2048)
                if new_msg:
                    # print(f"New message length: {message[:self.header]}")
                    msglen = int(message[:self.header])
                    new_msg = False

                full_msg += message.decode("utf-8")

                if len(full_msg) - self.header == msglen:
                    message = full_msg[self.header:]
                    break

            dataJson = json.loads(message)
            playerCount = dataJson[list(dataJson)[0]]

            dataDict = {"Reply":"Received"}
            dataData = json.dumps(dataDict)
            dataSend = f"{len(dataData):<{self.header}}" + dataData
            self.client.sendall(bytes(dataSend, 'utf-8'))

            return playerCount

        except socket.error as e:
            print(e)

    def connect(self):
        try:
            self.client.connect(self.addr)
            command = {"command": self.id}
            commandData = json.dumps(command)
            commandSend = f"{len(commandData):<{self.header}}" + commandData
            self.client.sendall(bytes(commandSend, 'utf-8'))

            full_msg = ""
            new_msg = True
            message_finish = False
            message = ""
            msglen = 0
            while not message_finish:
                message = self.client.recv(2048)
                if new_msg:
                    #print(f"New message length: {message[:self.header]}")
                    msglen = int(message[:self.header])
                    new_msg = False

                full_msg += message.decode("utf-8")

                if len(full_msg) - self.header == msglen:
                    message_finish = False
                    message = full_msg[self.header:]
                    new_msg = True
                    full_msg = ""
                    break

            dataJson = json.loads(message)
            player = Player(dataJson["x"], dataJson["y"], dataJson["height"], dataJson["width"], dataJson["colour"])
            print(player.getAllAtt())
            threadID = dataJson["gameID"]
            serverID = dataJson["serverID"]
            print(player)
            return player,threadID,serverID
        except:
            pass

    def send(self, data):
        try:
            print("sending")
            dataDict = dict(data)
            dataData = json.dumps(dataDict)
            dataSend = f"{len(dataData):<{self.header}}" + dataData
            self.client.sendall(bytes(dataSend,'utf-8'))

            print("listening")
            full_msg = ""
            new_msg = True
            message_finish = False
            msgLen = 0
            message = ""
            while not message_finish:
                message = self.client.recv(2048)
                if new_msg:
                    #print(f"New message length: {message[:self.header]}")
                    msgLen = int(message[:self.header])
                    new_msg = False

                full_msg += message.decode("utf-8")

                if len(full_msg) - self.header == msgLen:
                    message = full_msg[self.header:]
                    break

            dataJson = json.loads(message)
            player = Player(dataJson["x"], dataJson["y"], dataJson["height"], dataJson["width"], dataJson["colour"])
            return player
        except socket.error as e:
            print(e)

    def getMap(self):
        try:
            print("listening")
            full_msg = ""
            new_msg = True
            message_finish = False
            msgLen = 0
            message = ""
            while not message_finish:
                message = self.client.recv(2048)
                if new_msg:
                    # print(f"New message length: {message[:self.header]}")
                    msgLen = int(message[:self.header])
                    new_msg = False

                full_msg += message.decode("utf-8")

                if len(full_msg) - self.header == msgLen:
                    message = full_msg[self.header:]
                    break

            dataJson = json.loads(message)

            print("sending")

            dataDict = {"reply": "received"}
            dataData = json.dumps(dataDict)
            dataSend = f"{len(dataData):<{self.header}}" + dataData
            self.client.sendall(bytes(dataSend, 'utf-8'))

            return list(dataJson[list(dataJson)[0]])
        except socket.error as e:
            print(e)


class mainNetwork:
    def __init__(self,choice,data):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.header = 64
        self.addr = (self.server, self.port)
        self.logInBool, self.id = self.connect(choice,data)

    def connect(self,choice,data):
        try:
            self.client.connect(self.addr)
            command = {"command":(choice,data)}
            commandData = json.dumps(command)
            commandSend = f"{len(commandData):<{self.header}}" + commandData
            self.client.sendall(bytes(commandSend, 'utf-8'))

            full_msg = ""
            new_msg = True
            message_finish = False
            msgLen = 0
            message = ""
            while not message_finish:
                message = self.client.recv(2048)
                if new_msg:
                    # print(f"New message length: {message[:self.header]}")
                    msgLen = int(message[:self.header])
                    new_msg = False

                full_msg += message.decode("utf-8")

                if len(full_msg) - self.header == msgLen:
                    message = full_msg[self.header:]
                    break

            dataJson = json.loads(message)
            dataList = dataJson[list(dataJson)[0]]
            if dataList[1][0] == True:
                return dataList[1]
            else:
                return dataList[1]
        except socket.error:
            return False,"connectionError"

    def send(self,data):
        try:
            print("sending")
            dataDict = {"command":data}
            dataData = json.dumps(dataDict)
            dataSend = f"{len(dataData):<{self.header}}" + dataData
            self.client.sendall(bytes(dataSend, 'utf-8'))

            print("listening")
            full_msg = ""
            new_msg = True
            message_finish = False
            msgLen = 0
            message = ""
            while not message_finish:
                message = self.client.recv(2048)
                if new_msg:
                    # print(f"New message length: {message[:self.header]}")
                    msgLen = int(message[:self.header])
                    new_msg = False

                full_msg += message.decode("utf-8")

                if len(full_msg) - self.header == msgLen:
                    message = full_msg[self.header:]
                    break

            dataJson = json.loads(message)
            return list(dataJson[list(dataJson)[0]])

        except socket.error as e:
            print(e)

    def close(self):
        self.client.close()
