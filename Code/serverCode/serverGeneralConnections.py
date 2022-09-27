import os
import sys
from serverConstants import *
import mysql.connector

basePath = os.getcwd()[:-11]

playerInfoDB = mysql.connector.connect(
    host = "localhost",
    user = serverUser,
    password = serverPass,
    database = "playerInfo"
)

myCursor = playerInfoDB.cursor()

def logInMain(data):
    def register(data):
        while True:
            overall = []
            command = "SELECT playerID FROM playerInfo ORDER BY playerID DESC LIMIT 1"
            myCursor.execute(command)
            fetched = myCursor.fetchall()
            for row in fetched:
                overall.append(row)
            playerID = int(overall[0][0]) + 1
            command = f"""INSERT INTO playerInfo (playerID,username,password,nationality,continent)
            VALUES ('{str(playerID)}','{data[0]}','{data[1]}','{data[2]}','{data[3]}')"""
            try:
                myCursor.execute(command)
                break
            except mysql.connector.errors.IntegrityError:
                pass

        commandList = [["overall","over"],["drengr","dre"],["sidasveinn","sid"],["beserkr","bes"]]
        for i in range(0,len(commandList)):
            command = f"""INSERT INTO {commandList[i][0]} ({commandList[i][1]}ID, {commandList[i][1]}Kills,
            {commandList[i][1]}Deaths, {commandList[i][1]}KD, {commandList[i][1]}Wins, {commandList[i][1]}Losses,
            {commandList[i][1]}WL)
            VALUES ('{str(playerID)}','0','0','0','0','0','0')"""
            myCursor.execute(command)
        playerInfoDB.commit()
        return True

    def logIn(data):
        overall = []
        givenUser = data[0]
        givenPassword = data[1]
        command = f"SELECT password,playerID FROM playerInfo WHERE username = '{str(givenUser)}'"
        myCursor.execute(command)
        fetched = myCursor.fetchall()
        for row in fetched:
            overall = row
        if givenPassword == overall[0]:
            logInBool = True
        else:
            logInBool = False
        return [logInBool, overall[1]]

    if data[0] == "logIn":
        return ["logIn", logIn(data[1])]
    elif data[0] == "register":
        return ["register", register(data[1])]

def leaderboardMain(data):
    def getLeaderboard(data):
        if data[0] == "Global":
            command = f"""SELECT playerInfo.playerID, playerInfo.username, 
            playerInfo.nationality, {data[1]}.{data[2]}Kills, 
            {data[1]}.{data[2]}Deaths, {data[1]}.{data[2]}KD, 
            {data[1]}.{data[2]}Wins, {data[1]}.{data[2]}Losses, {data[1]}.{data[2]}WL
            FROM {data[1]}
            LEFT OUTER JOIN playerInfo
            ON playerInfo.playerID = {data[1]}.{data[2]}ID
            ORDER BY {data[1]}.{data[2]}Wins DESC
            LIMIT 10"""
        else:
            command = f"""SELECT playerInfo.playerID, playerInfo.username, 
            playerInfo.nationality, {data[1]}.{data[2]}Kills, 
            {data[1]}.{data[2]}Deaths, {data[1]}.{data[2]}KD, 
            {data[1]}.{data[2]}Wins, {data[1]}.{data[2]}Losses, {data[1]}.{data[2]}WL
            FROM {data[1]}
            LEFT OUTER JOIN playerInfo
            ON playerInfo.playerID = {data[1]}.{data[2]}ID
            WHERE playerInfo.continent = "{data[0]}"
            ORDER BY {data[1]}.{data[2]}Wins DESC
            LIMIT 10"""
        overall = []
        myCursor.execute(command)
        fetched = myCursor.fetchall()
        for row in fetched:
            overall.append(row)
        if len(overall) != 10:
            for i in range(0,10-len(overall)):
                overall.append(["","","","","","","","",""])
        if data[0] == "Global":
            command = f"""SELECT playerInfo.playerID, playerInfo.username, 
            playerInfo.nationality, {data[1]}.{data[2]}Kills, 
            {data[1]}.{data[2]}Deaths, {data[1]}.{data[2]}KD, 
            {data[1]}.{data[2]}Wins, {data[1]}.{data[2]}Losses, {data[1]}.{data[2]}WL,
            ROW_NUMBER() OVER (ORDER BY {data[1]}.{data[2]}Wins DESC)
            FROM {data[1]}
            LEFT OUTER JOIN playerInfo
            ON playerInfo.playerID = {data[1]}.{data[2]}ID
            WHERE {data[1]}.{data[2]}ID = "{data[3]}"
            ORDER BY {data[1]}.{data[2]}Wins DESC
            LIMIT 10"""
        else:
            command = f"""SELECT playerInfo.playerID, playerInfo.username, 
            playerInfo.nationality, {data[1]}.{data[2]}Kills, 
            {data[1]}.{data[2]}Deaths, {data[1]}.{data[2]}KD, 
            {data[1]}.{data[2]}Wins, {data[1]}.{data[2]}Losses, {data[1]}.{data[2]}WL
            ROW_NUMBER() OVER (ORDER BY {data[1]}.{data[2]}Wins DESC)
            FROM {data[1]}
            LEFT OUTER JOIN playerInfo
            ON playerInfo.playerID = {data[1]}.{data[2]}ID
            WHERE playerInfo.continent = "{data[0]}" AND {data[1]}.{data[2]}ID = "{data[3]}"
            ORDER BY {data[1]}.{data[2]}Wins DESC
            LIMIT 10"""
        myCursor.execute(command)
        fetched = myCursor.fetchall()
        for row in fetched:
            overall.append(row)
        return ["get",overall]

    def updateLeaderboard(data):
        commandList = [[data[4][0],data[4][1]],["overall","over"]]
        for i in range(0,len(commandList)):
            command = f"SELECT * FROM {commandList[i][0]} WHERE {commandList[i][1]}ID = {data[0]}"
            overall = []
            myCursor.execute(command)
            fetched = myCursor.fetchall()
            for row in fetched:
                overall.append(row)
            totalKills = overall[0][1] + data[1]
            totalDeaths = overall[0][2] + data[2]
            if totalDeaths == 0:
                totalKD = totalKills / 1
            else:
                totalKD = totalKills/totalDeaths
            if data[3]:
                totalWins = overall[0][4] + 1
                totalLosses = overall[0][5]
            else:
                totalWins = overall[0][4]
                totalLosses = overall[0][5] + 1
            if totalLosses == 0:
                totalWL = totalWins / 1
            else:
                totalWL = totalWins/totalDeaths
            command = f"""UPDATE {commandList[i][0]}
            SET {commandList[i][1]}Kills = {totalKills}, {commandList[i][1]}Deaths = {totalDeaths}, 
            {commandList[i][1]}KD = {totalKD}, {commandList[i][1]}Wins = {totalWins},
            {commandList[i][1]}Losses = {totalLosses}, {commandList[i][1]}WL = {totalWL}
            WHERE {commandList[i][1]}ID = {data[0]}"""
            myCursor.execute(command)
        playerInfoDB.commit()
        return ["update",True]
    def currentPlayerLeaderboard(data):
        overall = []
        searchList = [["overall","over"],["beserkr","bes"],["drengr","dre"],["sidasveinn","sid"]]
        for i in range(len(searchList)):
            command = f"""SELECT *
            FROM {searchList[i][0]}
            WHERE {searchList[i][1]}ID = "{data[0]}" """
            myCursor.execute(command)
            fetched = myCursor.fetchall()
            for row in fetched:
                overall.append(row)
        return["current",overall]


    if data[0] == "get":
        return(getLeaderboard(data[1]))
    elif data[0] == "update":
        return(updateLeaderboard(data[1]))
    elif data[0] == "current":
        return(currentPlayerLeaderboard(data[1]))
