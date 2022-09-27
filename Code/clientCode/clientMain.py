import time

import pygame
import os
import sys
import socket
import threading
import threadHandler
import json
import clientNetwork
import mapDisplay
from mapFunctions import *
from clientConstants import *
from pygame.locals import *
import pygame_gui
from pygame_gui.elements import *
from pygame_gui.core import ObjectID
from player import Player

basePath = os.getcwd()[:-11]
load = pygame.image.load
path = os.path.join

pygame.init()

pygame.display.set_caption("Battle of the Nine Realms")
displayWidth = 900
displayHeight = 600
threadEnd = False
cancelBool = False
finishBool = False
threadReturn = ""
display = pygame.display.set_mode((displayWidth,displayHeight))
jsonPath = basePath+"\Graphics\startTheme.json"
manager = pygame_gui.UIManager((displayWidth,displayHeight),jsonPath)
clock = pygame.time.Clock()


def loadingScreen(gameRunning=True, forward=True):
    global threadEnd
    threadEnd = False
    frameCount = 8
    imageCount = 9
    screenCount = 0

    logoImages = [load(path(basePath + "\Graphics\Images", "LoadingLogo1.png")),
                  load(path(basePath + "\Graphics\Images", "LoadingLogo2.png")),
                  load(path(basePath + "\Graphics\Images", "LoadingLogo3.png")),
                  load(path(basePath + "\Graphics\Images", "LoadingLogo4.png")),
                  load(path(basePath + "\Graphics\Images", "LoadingLogo5.png")),
                  load(path(basePath + "\Graphics\Images", "LoadingLogo6.png")),
                  load(path(basePath + "\Graphics\Images", "LoadingLogo7.png")),
                  load(path(basePath + "\Graphics\Images", "LoadingLogo8.png")),
                  load(path(basePath + "\Graphics\Images", "LoadingLogo9.png"))]
    for i in range(0, len(logoImages)):
        logoImages[i] = pygame.transform.scale(logoImages[i], (100, 100))


    while gameRunning:
        if threadEnd:
            gameRunning = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameRunning = False
                    pygame.quit()
            elif event.type == pygame.QUIT:
                gameRunning = False
                pygame.quit()
            manager.process_events(event)

        display.fill((0, 0, 0))
        display.blit(logoImages[screenCount // frameCount], (750, 450))

        if forward:
            screenCount += 1
        else:
            screenCount -= 1
        if screenCount == (frameCount * imageCount) - 1:
            forward = False
        elif screenCount == 0:
            forward = True

        pygame.display.update()
        clock.tick(60)


class SurfaceObject(pygame.sprite.Sprite):
    def __init__(self,image,x,y,width,height,*groups):
        super().__init__(*groups)
        self.img = load(path(basePath+"\Graphics\Images",image))
        self.img = pygame.transform.scale(self.img,(width,height))
        self.originalImage = pygame.Surface((900,600),pygame.SRCALPHA, 32)
        self.originalImage = self.originalImage.convert_alpha()
        self.originalImage.blit(self.img,(x,y))
        self.image = self.originalImage
        self.rect = self.img.get_rect()
        
    def killObject(self):
        self.kill()


class StartButton(SurfaceObject):
    def __init__(self,image,x,y,width,height,*groups):
        super().__init__(image,x,y,width,height,*groups)

    def pressed(self,spriteGroup):
        for sprite in spriteGroup:
            sprite.killObject()


def StartScreen():
    loadingThread = threading.Thread(target=loadingScreen,
                                     args=(),
                                     daemon=True)
    loadingThread.start()
    backgroundImages = [load(path(basePath+"\Graphics\Images","StartScreen1.png")),
                        load(path(basePath+"\Graphics\Images","StartScreen2.png")),
                        load(path(basePath+"\Graphics\Images","StartScreen3.png")),
                        load(path(basePath+"\Graphics\Images","StartScreen4.png")),
                        load(path(basePath+"\Graphics\Images","StartScreen5.png")),
                        load(path(basePath+"\Graphics\Images","StartScreen6.png"))]
    for i in range(0,len(backgroundImages)):
        backgroundImages[i] = pygame.transform.scale(backgroundImages[i],(900,600))

    def start(backgroundImages,gameRunning = True,forward = True):
        global threadEnd
        frameCount = 8
        imageCount = 6
        screenCount = 0

        startButton = UIButton(relative_rect=pygame.Rect((150,450),(600,100)),
                               text="Start",
                               manager=manager)

        logo = UIImage(relative_rect=pygame.Rect((175,25),bigLogoSize),
                       image_surface=load(path(basePath+"\Graphics\Images","LogoAndTitle.png")),
                       manager=manager)

        #logo = SurfaceObject("LogoAndTitle.png", 175, 50, 550, 400, startGroup)
        #startButton = StartButton("StartButton.png", 150, 450, 600, 100, startGroup)

        while gameRunning:
            timeDelta = clock.tick(60)/1000
            for event in pygame.event.get():
                keypressMouse = pygame.mouse.get_pressed()
                keypressKey = pygame.key.get_pressed()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        gameRunning = False
                        pygame.quit()
                elif event.type == pygame.QUIT:
                    gameRunning = False
                    pygame.quit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == startButton:
                        gameRunning = False
                manager.process_events(event)

            manager.update(timeDelta)

            display.blit(backgroundImages[screenCount//frameCount],(0,0))
            if forward:
                screenCount += 1
            else:
                screenCount -= 1
            if screenCount == (frameCount * imageCount)-1:
                forward = False
            elif screenCount == 0:
                forward = True

            threadEnd = True
            loadingThread.join()
            manager.draw_ui(display)
            pygame.display.update()
            clock.tick(60)
        logIn(backgroundImages)

    def logIn(backgroundImages,gameRunning = True,forward = True):
        manager.clear_and_reset()
        frameCount = 8
        imageCount = 6
        screenCount = 0

        logInChoice = UIButton(relative_rect=pygame.Rect((150,150),(600,100)),
                               text="Log In",
                               manager=manager)
        registerChoice = UIButton(relative_rect=pygame.Rect((150, 350), (600, 100)),
                                  text="Register",
                                  manager=manager)
        logInFinal = UIButton(relative_rect=pygame.Rect((150, 450), (600, 100)),
                                 text="Log In",
                                 manager=manager,
                                 visible=True)
        usernameEntry = UITextEntryLine(relative_rect=pygame.Rect((150, 50), (600, 50)),
                                        manager=manager)
        passwordEntry = UITextEntryLine(relative_rect=pygame.Rect((150, 150), (600, 50)),
                                        manager=manager)
        passwordEntry.set_text_hidden()
        nationalityEntry = UITextEntryLine(relative_rect=pygame.Rect((150, 250), (600, 50)),
                                           manager=manager)
        continentEntry = UITextEntryLine(relative_rect=pygame.Rect((150, 350), (600, 50)),
                                         manager=manager)
        registerFinal = UIButton(relative_rect=pygame.Rect((150, 450), (600, 100)),
                                 text="Register",
                                 manager=manager,
                                 visible=True)
        logInFinal.hide()
        registerFinal.hide()
        usernameEntry.hide()
        passwordEntry.hide()
        nationalityEntry.hide()
        continentEntry.hide()

        while gameRunning:
            timeDelta = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        gameRunning = False
                        pygame.quit()
                elif event.type == pygame.QUIT:
                    gameRunning = False
                    pygame.quit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == logInChoice:
                        logInChoice.hide()
                        registerChoice.hide()
                        logInFinal.show()
                        usernameEntry.show()
                        passwordEntry.show()
                    elif event.ui_element == registerChoice:
                        logInChoice.hide()
                        registerChoice.hide()
                        registerFinal.show()
                        usernameEntry.show()
                        passwordEntry.show()
                        continentEntry.show()
                        nationalityEntry.show()
                    elif event.ui_element == logInFinal:
                        username = usernameEntry.get_text()
                        password = passwordEntry.get_text()
                        mainNetwork = clientNetwork.mainNetwork("logIn",(username,password))
                        if mainNetwork.logInBool == True:
                            print("Success")
                            preGame(mainNetwork)
                        elif mainNetwork.logInBool == False and mainNetwork.id != "connectionError":
                            print("Failure")
                        else:
                            print("Error")

                    elif event.ui_element == registerFinal:
                        username = usernameEntry.get_text()
                        password = passwordEntry.get_text()
                        nationality = nationalityEntry.get_text()
                        continent = continentEntry.get_text()
                        mainNetwork = clientNetwork.mainNetwork("register", (username, password, nationality, continent))
                        if mainNetwork.logInBool == True:
                            print("Success")
                            preGame(mainNetwork)
                        elif mainNetwork.logInBool == False and mainNetwork.id != "connectionError":
                            print("Failure")
                        else:
                            print("Error")


                manager.process_events(event)

            manager.update(timeDelta)
            display.blit(backgroundImages[screenCount // frameCount], (0, 0))
            if forward:
                screenCount += 1
            else:
                screenCount -= 1
            if screenCount == (frameCount * imageCount)-1:
                forward = False
            elif screenCount == 0:
                forward = True

            manager.draw_ui(display)
            pygame.display.update()
            clock.tick(60)

    start(backgroundImages)

def preGame(mainNetwork):

    playerID = mainNetwork.id
    loadingThread = threading.Thread(target=loadingScreen,
                                     args=(),
                                     daemon=True)
    loadingThread.start()
    backgroundImages = [load(path(basePath + "\Graphics\Images", "StartScreen1.png")),
                        load(path(basePath + "\Graphics\Images", "StartScreen2.png")),
                        load(path(basePath + "\Graphics\Images", "StartScreen3.png")),
                        load(path(basePath + "\Graphics\Images", "StartScreen4.png")),
                        load(path(basePath + "\Graphics\Images", "StartScreen5.png")),
                        load(path(basePath + "\Graphics\Images", "StartScreen6.png"))]
    for i in range(0, len(backgroundImages)):
        backgroundImages[i] = pygame.transform.scale(backgroundImages[i], (900, 600))

    def start(backgroundImages,gameRunning = True,forward = True):

        global finishBool, threadReturn, threadEnd, matchThread, cancelBool
        manager.clear_and_reset()
        frameCount = 8
        imageCount = 6
        screenCount = 0

        homeButton = UIButton(relative_rect=pygame.Rect((125, 25), (200, 75)),
                               text="Home",
                               manager=manager,
                               object_id=ObjectID(class_id="@tabButton",
                                                  object_id=""))
        leaderboardButton = UIButton(relative_rect=pygame.Rect((350, 25), (200, 75)),
                                     text="Leaderboards",
                                     manager=manager,
                                     object_id=ObjectID(class_id="@tabButton",
                                                        object_id=""))
        statsButton = UIButton(relative_rect=pygame.Rect((575, 25), (200, 75)),
                                     text="Progression",
                                     manager=manager,
                                     object_id=ObjectID(class_id="@tabButton",
                                                        object_id=""))
        matchSearchButton = UIButton(relative_rect=pygame.Rect((200, 450), (500, 100)),
                                     text="Search For Match",
                                     manager=manager)
        cancelMatchButton = UIButton(relative_rect=pygame.Rect((200, 450), (500, 100)),
                                     text="Cancel Matchmaking",
                                     manager=manager)
        leaderboardRefreshButton = UIButton(relative_rect=pygame.Rect((725, 500), (150, 50)),
                                     text="Refresh",
                                     manager=manager,
                                     object_id=ObjectID(class_id="",
                                                        object_id="#refreshButton"))
        leaderboardTypeDropdown = UIDropDownMenu(["Overall","Beserkr","Drengr","Sidasveinn"],
                                             "Overall",
                                             relative_rect=pygame.Rect((725, 150), (150, 50)),
                                             manager=manager)
        leaderboardContinentDropdown = UIDropDownMenu(["Global", "Europe", "North America",
                                                  "South America","Asia","Australia","Africa"],
                                                 "Global",
                                                 relative_rect=pygame.Rect((725, 300), (150, 50)),
                                                 manager=manager)
        leaderboardLines = []
        for i in range(0, 12):
            yPlace = 150 + (35 * i)
            singleLine = []
            singleLine.append(UITextBox(html_text="ABCDEF",
                                        relative_rect=pygame.Rect((25, yPlace), (79, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="ABCDEFGHIJKLMNOPQRST",
                                        relative_rect=pygame.Rect((104, yPlace), (125, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647",
                                        relative_rect=pygame.Rect((229, yPlace), (60, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647",
                                        relative_rect=pygame.Rect((289, yPlace), (60, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647.0",
                                        relative_rect=pygame.Rect((349, yPlace), (68, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647",
                                        relative_rect=pygame.Rect((417, yPlace), (60, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647",
                                        relative_rect=pygame.Rect((477, yPlace), (60, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647.0",
                                        relative_rect=pygame.Rect((537, yPlace), (68, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="ABCDEFGHIJKLMNOPQRST",
                                        relative_rect=pygame.Rect((605, yPlace), (100, 35)),
                                        manager=manager))
            leaderboardLines.append(singleLine)
            for i in range(0,9):
                singleLine[i].hide()

        playerStats = []
        order = ["Overall","Beserkr","Drengr","Sidasveinn"]
        for i in range(0, 4):
            yPlace = 150 + (100 * i)
            singleLine = []
            singleLine.append(UITextBox(html_text=order[i],
                                        relative_rect=pygame.Rect((129, yPlace), (100, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647",
                                        relative_rect=pygame.Rect((229, yPlace), (60, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647",
                                        relative_rect=pygame.Rect((289, yPlace), (60, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647.0",
                                        relative_rect=pygame.Rect((349, yPlace), (68, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647",
                                        relative_rect=pygame.Rect((417, yPlace), (60, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647",
                                        relative_rect=pygame.Rect((477, yPlace), (60, 35)),
                                        manager=manager))
            singleLine.append(UITextBox(html_text="2147483647.0",
                                        relative_rect=pygame.Rect((537, yPlace), (68, 35)),
                                        manager=manager))
            playerStats.append(singleLine)
            for i in range(0, 7):
                singleLine[i].hide()


        logoImg = load(path(basePath + "\Graphics\Images", "LogoOnly.png"))
        logo = UIImage(relative_rect=pygame.Rect((25, 25), smallLogoSize),
                       image_surface=logoImg,
                       manager=manager)

        leaderboardRefreshButton.visible=False
        leaderboardTypeDropdown.hide()
        leaderboardContinentDropdown.hide()
        cancelMatchButton.hide()


        while gameRunning:
            timeDelta = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        gameRunning = False
                        pygame.quit()
                elif event.type == pygame.QUIT:
                    gameRunning = False
                    pygame.quit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == homeButton:
                        matchSearchButton.visible = True
                        leaderboardRefreshButton.visible = False
                        leaderboardTypeDropdown.hide()
                        leaderboardContinentDropdown.hide()
                        for i in range(0, 12):
                            for j in range(0, 9):
                                leaderboardLines[i][j].hide()
                        for i in range(0, 4):
                            for j in range(0, 7):
                                playerStats[i][j].hide()
                    if event.ui_element == leaderboardButton:
                        matchSearchButton.visible = False
                        leaderboardRefreshButton.visible = True
                        leaderboardTypeDropdown.show()
                        leaderboardContinentDropdown.show()
                        for i in range(0, 4):
                            for j in range(0, 7):
                                playerStats[i][j].hide()
                        table = leaderboardTypeDropdown.selected_option
                        continent = leaderboardContinentDropdown.selected_option
                        tablePrefix = "over"
                        if table == "overall":
                            tablePrefix = "over"
                        elif table == "sidasveinn":
                            tablePrefix = "sid"
                        elif table == "beserkr":
                            tablePrefix = "bes"
                        elif table == "drengr":
                            tablePrefix = "dre"
                        commandList = ["get",[continent,table,tablePrefix,playerID]]
                        result = mainNetwork.send(commandList)
                        result = result[1]
                        for i in range(0, 12):
                            if i == 0:
                                leaderboardLines[i][0].html_text = "Placement"
                                leaderboardLines[i][1].html_text = "Username"
                                leaderboardLines[i][2].html_text = "Kills"
                                leaderboardLines[i][3].html_text = "Deaths"
                                leaderboardLines[i][4].html_text = "KD Ratio"
                                leaderboardLines[i][5].html_text = "Wins"
                                leaderboardLines[i][6].html_text = "Losses"
                                leaderboardLines[i][7].html_text = "WL Ratio"
                                leaderboardLines[i][8].html_text = "Country"
                            else:
                                data = result[i-1]
                                leaderboardLines[i][0].html_text = f"{i}"
                                leaderboardLines[i][1].html_text = f"{data[1]}"
                                leaderboardLines[i][2].html_text = f"{data[3]}"
                                leaderboardLines[i][3].html_text = f"{data[4]}"
                                leaderboardLines[i][4].html_text = f"{data[5]}"
                                leaderboardLines[i][5].html_text = f"{data[6]}"
                                leaderboardLines[i][6].html_text = f"{data[7]}"
                                leaderboardLines[i][7].html_text = f"{data[8]}"
                                leaderboardLines[i][8].html_text = f"{data[2]}"

                        data = result[10]
                        leaderboardLines[11][0].html_text = f"{data[9]}"
                        leaderboardLines[11][1].html_text = f"{data[1]}"
                        leaderboardLines[11][2].html_text = f"{data[3]}"
                        leaderboardLines[11][3].html_text = f"{data[4]}"
                        leaderboardLines[11][4].html_text = f"{data[5]}"
                        leaderboardLines[11][5].html_text = f"{data[6]}"
                        leaderboardLines[11][6].html_text = f"{data[7]}"
                        leaderboardLines[11][7].html_text = f"{data[8]}"
                        leaderboardLines[11][8].html_text = f"{data[2]}"

                        for i in range(0, 12):
                            for j in range(0, 9):
                                leaderboardLines[i][j].rebuild()
                                leaderboardLines[i][j].show()

                    if event.ui_element == statsButton:
                        matchSearchButton.visible = False
                        leaderboardRefreshButton.visible = False
                        leaderboardTypeDropdown.hide()
                        leaderboardContinentDropdown.hide()
                        for i in range(0, 12):
                            for j in range(0, 9):
                                leaderboardLines[i][j].hide()
                        commandList = ["current", [playerID]]
                        result = mainNetwork.send(commandList)
                        result = result[1]
                        for i in range(1, 5):
                            j = i - 1
                            data = result[j]
                            playerStats[j][1].html_text = f"{data[1]}"
                            playerStats[j][2].html_text = f"{data[2]}"
                            playerStats[j][3].html_text = f"{data[3]}"
                            playerStats[j][4].html_text = f"{data[4]}"
                            playerStats[j][5].html_text = f"{data[5]}"
                            playerStats[j][6].html_text = f"{data[6]}"
                        for i in range(0, 4):
                            for j in range(0, 7):
                                playerStats[i][j].rebuild()
                                playerStats[i][j].show()

                    if event.ui_element == leaderboardRefreshButton:
                        table = leaderboardTypeDropdown.selected_option
                        continent = leaderboardContinentDropdown.selected_option
                        tablePrefix = "over"
                        if table.lower() == "overall":
                            tablePrefix = "over"
                        elif table.lower() == "sidasveinn":
                            tablePrefix = "sid"
                        elif table.lower() == "beserkr":
                            tablePrefix = "bes"
                        elif table.lower() == "drengr":
                            tablePrefix = "dre"
                        commandList = ["get", [continent, table, tablePrefix,playerID]]
                        result = mainNetwork.send(commandList)
                        result = result[1]
                        for i in range(0, 11):
                            if i == 0:
                                leaderboardLines[i][0].html_text = "Placement"
                                leaderboardLines[i][1].html_text = "Username"
                                leaderboardLines[i][2].html_text = "Kills"
                                leaderboardLines[i][3].html_text = "Deaths"
                                leaderboardLines[i][4].html_text = "KD Ratio"
                                leaderboardLines[i][5].html_text = "Wins"
                                leaderboardLines[i][6].html_text = "Losses"
                                leaderboardLines[i][7].html_text = "WL Ratio"
                                leaderboardLines[i][8].html_text = "Country"
                            else:
                                data = result[i - 1]
                                leaderboardLines[i][0].html_text = f"{i}"
                                leaderboardLines[i][1].html_text = f"{data[1]}"
                                leaderboardLines[i][2].html_text = f"{data[3]}"
                                leaderboardLines[i][3].html_text = f"{data[4]}"
                                leaderboardLines[i][4].html_text = f"{data[5]}"
                                leaderboardLines[i][5].html_text = f"{data[6]}"
                                leaderboardLines[i][6].html_text = f"{data[7]}"
                                leaderboardLines[i][7].html_text = f"{data[8]}"
                                leaderboardLines[i][8].html_text = f"{data[2]}"
                        data = result[10]
                        leaderboardLines[11][0].html_text = f"{data[9]}"
                        leaderboardLines[11][1].html_text = f"{data[1]}"
                        leaderboardLines[11][2].html_text = f"{data[3]}"
                        leaderboardLines[11][3].html_text = f"{data[4]}"
                        leaderboardLines[11][4].html_text = f"{data[5]}"
                        leaderboardLines[11][5].html_text = f"{data[6]}"
                        leaderboardLines[11][6].html_text = f"{data[7]}"
                        leaderboardLines[11][7].html_text = f"{data[8]}"
                        leaderboardLines[11][8].html_text = f"{data[2]}"
                        for i in range(0, 12):
                            for j in range(0, 9):
                                leaderboardLines[i][j].rebuild()
                                leaderboardLines[i][j].show()
                    if event.ui_element == matchSearchButton:
                        cancelBool = False
                        finishBool = False
                        matchSearchButton.hide()
                        cancelMatchButton.show()
                        def matchmaking(threadReturn):
                            global finishBool, cancelBool
                            gameNetwork = clientNetwork.gameNetwork(mainNetwork.id)
                            startTime = time.time()
                            while not finishBool:
                                playerCount = gameNetwork.getPlayerCount()
                                totalPassed = time.time() - startTime
                                print(playerCount)
                                if playerCount == 2:
                                    output = ["Start",gameNetwork]
                                    threadReturn.enque(output)
                                    finishBool = True
                                elif totalPassed >= 60 or cancelBool == True:
                                    #gameNetwork.client.close()
                                    output = ["Cancel",None]
                                    threadReturn.enque(output)
                                    finishBool = True



                        threadReturn = threadHandler.ThreadReturn()
                        matchThread = threading.Thread(target=matchmaking,
                                                       args=(threadReturn,),
                                                       daemon=True)
                        matchThread.start()

                    if event.ui_element == cancelMatchButton:
                        cancelBool = True
                        matchSearchButton.show()
                        cancelMatchButton.hide()



                manager.process_events(event)
            if finishBool:
                finishBool = False
                matchThread.join()
                output = threadReturn.deque()
                print(output)
                matchState = output[0]
                gameNetwork = output[1]
                print(matchState)
                print(gameNetwork)
                if matchState == "Start":
                    game(mainNetwork, gameNetwork, manager)
                else:
                    matchSearchButton.show()
                    cancelMatchButton.hide()

            manager.update(timeDelta)
            display.blit(backgroundImages[screenCount // frameCount], (0, 0))
            if forward:
                screenCount += 1
            else:
                screenCount -= 1
            if screenCount == (frameCount * imageCount)-1:
                forward = False
            elif screenCount == 0:
                forward = True

            threadEnd = True
            loadingThread.join()
            manager.draw_ui(display)
            pygame.display.update()
            clock.tick(60)

    start(backgroundImages)

def game(mainNetwork,gameNetwork,manager):
    manager.clear_and_reset()
    def redrawWindow(window, player, player2,gameMap):
        mapDisplay.drawMap(gameMap)
        player.draw(window)
        player2.draw(window)
        pygame.display.update()

    run = True
    p = gameNetwork.getP()
    clock = pygame.time.Clock()
    gameMap = CellularAutomataMap(60,60,0.4)
    print(-1)
    gameMap.map = gameNetwork.getMap()
    print(0)
    while run:
        print(1)
        p2 = gameNetwork.send(p)
        print(2)

        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(display, p, p2, gameMap)
StartScreen()
