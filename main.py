import pygame,button,Variables,Entities,statsMap,math,random,EnemyController,time,resourceManager
pygame.init()
class GameController:
    def __init__(self,screenWidth,screenHeight,framerate):
        self.screen = pygame.display.set_mode((screenWidth,screenHeight))
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen)
        self.postGame = Endpage(self.screen)
        self.frameRate = framerate
        self.stage = 0
        self.frame = 0
        print(Variables.underlyingGrid.nodeHeight)
        print(Variables.underlyingGrid.nodeWidth)
    def setup(self):
        # A function called before each play of the game
        Variables.entities = [[],[]]
        Variables.castleObject = None
        Variables.money = 30
        Variables.score = 0
        Variables.castleObject = Entities.Physical(name="Castle",data=statsMap.statsMap["Castle"],pos=(250,250))
        self.game = Game(self.screen)
        self.game.wave = 0
        #only resset the frame on the setup
        self.frame = 0
        
        
    def run(self):
        self.setup()
        preGameRunning = True
        gameRunning = False
        postGameRunning = False
        running = True
        currentTick = 0
        prevTick = 0
        while running:
            #print(currentTick-prevTick)
            prevTick = currentTick
            self.frame+=1   
            running = self.handleEvents()# check for window closures
            if preGameRunning:# run the correct screen
                preGameRunning,play = self.menu.update() # returns 2 bools, one to control the screen one to play
                if not preGameRunning: 
                    # if the screen needs to change it will either be to the game or quit
                    if play: # moves to the game
                        gameRunning = True
                    else: # closes the game
                        running = False

            if gameRunning:
                gameRunning = self.game.update(self.frame)
            
            if postGameRunning:
                postGameRunning,replay  = self.postGame.update()
                if not postGameRunning: # if a button has been pressed
                    if replay:
                        #restart the program
                        self.setup()

                        gameRunning = True
                    else:
                        #close the program
                        running = False
            if not gameRunning and not preGameRunning and running:
                # run if no other windows are, but window has not been closed
                postGameRunning = True

            pygame.draw.circle(self.screen,(255,0,0),pygame.mouse.get_pos(),5) #red mopuse circle

            self.clock.tick(self.frameRate)
            currentTick = pygame.time.get_ticks()
            pygame.display.update()
        pygame.quit()
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True  

class Menu:
    def __init__(self,screen):
        self.screen = screen
        self.titleFont = pygame.font.SysFont("Consolas",40)
        self.dataFont = pygame.font.SysFont("Consolas",20)
        self.title = self.titleFont.render("MENU", True, (0,0,0))
        self.playButton = button.Button(text="  Play ",x=187,y=320,width=80,height=45,colour=(0,255,0))
        self.exitButton = button.Button(text="  Exit ",x=483,y=320,width=80,height=45,colour=(255,0,0))

        self.score = 0
        try:
            #try to open thehighscores file
            f = open("highscores.txt","r")
            self.score = int(f.readline())
            print("File found")
        except FileNotFoundError:
            #If no file can be found then a file is created
            f = open("highscores.txt","w")
            # a score is written in as 0
            f.write("0")
            print("File not found")
        except:
            print("File found but another error occured")
            #if any other error occurs, move on with score = 0
            pass
        f.close()
        print("Current Highscore:",self.score)
        #create the fonts and text objects for the screen
        self.highScoreText = self.dataFont.render(str(self.score),True,(0,0,0))
        self.highScoreTitle = self.dataFont.render(f"HIGHSCORE:",True,(0,0,0))
        self.highScorex = 375-(len(str(self.score))*5) # fonst size is 20 so instead of *20/2, *10

    def update(self):
        self.screen.fill((255,255,255))
        #draw title and buttons
        self.screen.blit(self.title,(330,100))
        self.playButton.draw(self.screen)
        self.exitButton.draw(self.screen)
        #get mouse data
        mousePos = pygame.mouse.get_pos()
        mouseClicked = pygame.mouse.get_pressed()[0]
        #check buttons
        #self.screen.blit()

        #draw the highscore text onto the menu
        self.screen.blit(self.highScoreTitle,(330,200))
        self.screen.blit(self.highScoreText,(self.highScorex,250))

        playPressed = self.playButton.checkClicked(mousePos,mouseClicked)[0]
        if playPressed:
            # False for menu running, true for play
            print("PLAY BUTTON PRESSED")
            return False,True
        exitPressed = self.exitButton.checkClicked(mousePos,mouseClicked)[0]
        if exitPressed:
            #False to close menu and False to close window
            print("EXIT BUTTON PRESSED")
            return False,False
        return True,False
    
class Endpage:
    def __init__(self,screen):
        self.screen = screen
        self.titleFont = pygame.font.SysFont("Consolas",40)
        self.dataFont = pygame.font.SysFont("Consolas",25)
        self.title = self.titleFont.render("GAME OVER", True, (0,0,0))
        print("Checking the score",Variables.score)
        self.scoreText = None 
        self.replayButton = button.Button(text=" Replay ",x=187,y=320,width=100,height=45,colour=(0,255,0))
        self.exitButton = button.Button(text="  Exit ",x=483,y=320,width=80,height=45,colour=(255,0,0))
    def update(self):
        if self.scoreText == None:
            self.scoreText = self.dataFont.render(f"Score:{str(Variables.score)}",True,(0,0,0))
        #clear the screen
        self.screen.fill((255,255,255))
        #draw title and buttons
        self.screen.blit(self.title,(275,100))
        self.screen.blit(self.scoreText,(300,250))
        self.replayButton.draw(self.screen)
        self.exitButton.draw(self.screen)
        #get mouse data
        mousePos = pygame.mouse.get_pos()
        mouseClicked = pygame.mouse.get_pressed()[0]
        #check buttons
        playPressed = self.replayButton.checkClicked(mousePos,mouseClicked)[0]
        if playPressed:
            # False for menu running, true for play
            return False,True
        exitPressed  = self.exitButton.checkClicked(mousePos,mouseClicked)[0]
        if exitPressed:
            #False to close menu and False to close window
            return False,False
        return True,False
class Game:
    def __init__(self,screen):
        self.screen = screen
        self.boundsRadius = 200
        self.money = 150
        self.score = 0
        self.wave = 10
        self.coords = []
        self.dataFont = pygame.font.SysFont("Consolas",25)
        #2d lists to store shop data
        self.buttons = [[],[],[]]
        self.unitCosts = [[],[],[]]

        self.unitPlacementMode = False
        self.unitToPlace = None
        self.placementCount = 0
        self.prevMousePressed = False
        #housekeeping variables
        self.groundDefenceNames = ["Swordsman","Archer"]
        self.towerDefenceNames = ["ArcherTower"]
        self.physicalDefenceNames = ["Wall"]
        # self.spawnEnemies()
        self.EC = EnemyController.EnemyController()
        #create a defence button then the defence cost to go beneath it
        self.buttons[0].append(button.Button("",545,150,75,75,"SwordsmanShop.png",(200,200,200),statsMap.statsMap["Swordsman"]
                                             ["cost"],name="Swordsman"))
        self.unitCosts[0].append([self.dataFont.render(str(statsMap.statsMap["Swordsman"]["cost"]),True,(0,0,0)),(565,225)])

        self.buttons[0].append(button.Button("",655,150,75,75,"ArcherShop.png",(200,200,200),statsMap.statsMap["Archer"]
                                             ["cost"],name = "Archer"))
        self.unitCosts[0].append([self.dataFont.render(str(statsMap.statsMap["Archer"]["cost"]),True,(0,0,0)),(675,225)])

        self.buttons[1].append(button.Button("",545,150,75,75,"ArcherTowerShop.png",(200,200,200),statsMap.statsMap["ArcherTower"]
                                             ["cost"],name = "ArcherTower"))      
        self.unitCosts[1].append([self.dataFont.render(str(statsMap.statsMap["ArcherTower"]["cost"]),True,(0,0,0)),(565,225)])

        self.buttons[2].append(button.Button("",545,150,75,75,"WallShop.png",(200,200,200),statsMap.statsMap["Wall"]
                                             ["cost"],name = "Wall"))  
        self.unitCosts[2].append([self.dataFont.render(str(statsMap.statsMap["Wall"]["cost"]),True,(0,0,0)),(565,225)])

        self.buttons[0].append(button.Button("",545,150,25,25,"UpgradeIcon.png",(200,200,200),50,name="SwordsmanUpgrade")) 
        self.buttons[0].append(button.Button("",655,150,25,25,"UpgradeIcon.png",(200,200,200),50,name="ArcherUpgrade")) 
        self.buttons[1].append(button.Button("",545,150,25,25,"UpgradeIcon.png",(200,200,200),50,name="ArcherTowerUpgrade")) 
        self.buttons[2].append(button.Button("",545,150,25,25,"UpgradeIcon.png",(200,200,200),50,name="WallUpgradeUpgrade")) 

        # create the shop tabs and add them to a list
        Gtab = button.Button(text="    Ground",x=520,y=75,width=77,height=25,value=0)
        Gtab.changeColour((150,150,150))
        Ttab = button.Button(text="     Tower" ,x=597,y=75,width=77,height=25,value=1)
        Ptab = button.Button(text="   Physical",x=674,y=75,width=78,height=25,value=2)
        self.tabs = [Gtab,Ttab,Ptab]
        self.tabNum = 0
        
        self.moneyCoin = resourceManager.load_image("goldCoin.png")
        # unit placement graphics
        self.inBoundsSurface = pygame.surface.Surface((500,500),pygame.SRCALPHA)
        self.inBoundsCircle = pygame.draw.rect(self.inBoundsSurface,(255,100,100,125),pygame.Rect(0,0,500,500))
        self.inBoundsCircleOuter = pygame.draw.circle(self.inBoundsSurface,(255,255,255,0),(250,250),self.boundsRadius)
        self.inBoundsCircleInner = pygame.draw.circle(self.inBoundsSurface,(255,100,100,125),(250,250),50)
        self.exitPlacementModeButton = button.Button(x =450,y=0,width = 50,height = 50, 
                                                     fileName="exitUnitPlacement.png",border=False)
        self.exitPlacementModeButton.draw(self.inBoundsSurface)

        #unit upgrade 
        self.upgradeButton = button.Button(" Upgrade",565,400,150,65,colour=(0,255,0))

    def update(self,frame):
    

        if not Variables.entities[1]:
            self.EC.newWave(self.wave)
            self.wave +=1
            for defence in Variables.entities[0]:
                defence.reset()
        self.screen.fill((220,220,220))
        #fetch mouse data
        mousepos = pygame.mouse.get_pos()
        mouseClicked = pygame.mouse.get_pressed()[0]
        # draw background
        pygame.draw.line(self.screen,(50,50,50),(520,0),(520,550)) # shop divider
        pygame.draw.circle(self.screen,(220,255,220),(250,250),245)# game board
        Variables.castleObject.draw(self.screen)
        # draw data 
        self.drawData()
        # manage tabs
        for tab in self.tabs:
            tab.draw(self.screen)
            
            switchedTab,tabNum,tabName = tab.checkClicked(mousepos,mouseClicked)
            if switchedTab:
                self.tabs[self.tabNum].changeColour((200,200,200))
                self.tabNum = tabNum
                self.tabs[self.tabNum].changeColour((150,150,150))

        #button logic, draw the button and check if it has been pressed
        for b in self.buttons[self.tabNum]:
            b.draw(self.screen)
            buttonChecked,buttonCost,buttonName = b.checkClicked(mousepos,mouseClicked)
            
            if buttonChecked:
                self.unitToPlace = buttonName
                self.unitPlacementMode = True
                self.placeUnit(self.unitToPlace,mousepos,mouseClicked)

        #go through the costs and draw them to the screen
        for cost in self.unitCosts[self.tabNum]:
            #draw the coin
            self.screen.blit(self.moneyCoin,(cost[1][0]-20,cost[1][1]+5))
            # draw the text
            self.screen.blit(cost[0],cost[1])

        #draw entities
        for entity in Variables.entities[1]: # [1] signifies the enemies
            entity.draw(self.screen)
            entity.update(frame)
            #pygame.draw.circle(self.screen,(200,200,200),entity.rect.center,entity.visRange,2)
            # for step in entity.path:
            #     pygame.draw.circle(self.screen,(0,0,255),Variables.underlyingGrid.getCellPos(step),5)
            
            #entity.update()
        for entity in Variables.entities[0]:
            entity.draw(self.screen)
            entity.update(frame)
            #see entities range
            #pygame.draw.circle(self.screen,(200,200,200),entity.rect.center,entity.visRange,2)
            #     pygame.draw.circle(self.screen,(255,0,255),Variables.underlyingGrid.getCellPos(step),5)
        # see underlying grid nodes
        # for row in Variables.underlyingGrid.grid:
        #     for node in row:
        #         if node.occupant== None:
        #             col = (100,100,100)
        #         else:
        #             if node.occupant.name == "Wall":
        #                 col = (100,100,255)
        #             else:
        #                 col = (100,100,100)
        #         pygame.draw.circle(self.screen,col,Variables.underlyingGrid.getCellPos([node.col,node.row]),radius= 5)


        if self.unitPlacementMode:
            if "Upgrade" in self.unitToPlace:
                self.upgradeButton.draw(self.screen)
            else:
                self.screen.blit(self.inBoundsSurface,(0,0))
            
            #check the previous state of the mouse was unpressed
            if mouseClicked and not self.prevMousePressed:
                self.placeUnit(self.unitToPlace,mousepos,mouseClicked)
                self.prevMousePressed = True
            #set previous state of mouse to unpressed when it released
            if not mouseClicked and self.prevMousePressed:
                self.prevMousePressed = False
            #exit placement mode at the press of the button
            if self.exitPlacementModeButton.checkClicked(mousepos,mouseClicked)[0]:
                self.unitPlacementMode = False
        
        if Variables.castleObject == None:
            # read the previous highscore
            f = open("highscores.txt","r")
            prevHighscore = f.readline()

            print(prevHighscore)
            f.close()
            # compare the current score to the highscore
            if int(prevHighscore) < Variables.score:
                # overwrite the highscore with the current score
                f = open("highscores.txt","w")
                f.write(str(Variables.score))
                f.close()
                print("Highscore Overwritten")
            else:
                print("Highscore not overwridden")
            
            #signal end of main game
            return False
        

        # draw mouse circle last to overlay on top of everything
        # for coord in self.coords:
        #     pygame.draw.circle(self.screen,(255,0,0),coord,5)
        return True
        
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def placeUnit(self,type,mousepos,mousestatus):
        
        cost = statsMap.statsMap[self.unitToPlace]["cost"]
        #check the player has the money
        if Variables.money<cost:
            print("ran out of money")
            self.unitToPlace = None
            self.unitPlacementMode = False
            return
        else:#
            # check if an upgrade has been seleted
            if "Upgrade" in self.unitToPlace and self.upgradeButton.checkClicked(mousepos,mousestatus)[0]:
                #take the money for the upgrade
                Variables.money -= statsMap.statsMap[self.unitToPlace]["cost"]
                # put upgrades here
                #remove the last 7 letters ("Upgrade") from the unit to place to leave just the name of the defece
                unitToUpgrade = self.unitToPlace[:-7]
                #Upgrades are arbitary and need to be changed/balanced
                print(statsMap.statsMap[unitToUpgrade]["health"])
                statsMap.statsMap[unitToUpgrade]["health"] = int(statsMap.statsMap[unitToUpgrade]["health"]*1.5)
                print(statsMap.statsMap[unitToUpgrade]["damage"])
                statsMap.statsMap[unitToUpgrade]["damage"] = int(statsMap.statsMap[unitToUpgrade]["damage"]*1.5)
                print(statsMap.statsMap[unitToUpgrade]["speed"])
                statsMap.statsMap[unitToUpgrade]["speed"] = round((statsMap.statsMap[unitToUpgrade]["speed"]*1.5),1)
                print(statsMap.statsMap[unitToUpgrade])

                self.unitToPlace = None
                self.unitPlacementMode = False
            #check the mouse is in bounds
            elif mousestatus and self.inBounds(mousepos):# 
                if self.unitToPlace in self.groundDefenceNames: # add other ground units here
                    Variables.entities[0].append(Entities.Ground(name=self.unitToPlace,data=statsMap.statsMap[self.unitToPlace],pos=mousepos))

                elif self.unitToPlace in self.towerDefenceNames: # add other towers here
                    Variables.entities[0].append(Entities.Tower(name=self.unitToPlace,data=statsMap.statsMap[self.unitToPlace],pos=mousepos))

                elif self.unitToPlace in self.physicalDefenceNames: # add other physical defences here
                    Variables.entities[0].append(Entities.Physical(name=self.unitToPlace,data=statsMap.statsMap[self.unitToPlace],pos=mousepos))

                Variables.money -= cost
            
            
            

    def inBounds(self,pos):
        if 50<math.sqrt((250-pos[0])**2 + (250-pos[1])**2) < self.boundsRadius:
            return True
        else:return False
    def drawData(self):
        # draw the "Shop"
        self.dataFont.set_bold(True)
        shopTitle = self.dataFont.render("SHOP",True,(0,0,0))
        self.dataFont.set_bold(False)
        self.screen.blit(shopTitle,(525,10))
        #draw money count
        moneyCount = self.dataFont.render("Money: "+ str(Variables.money),True,(0,0,0))
        self.screen.blit(moneyCount,(525,40))
        #draw the gold coin before the money
        self.screen.blit(self.moneyCoin,(608,45))
        # draw wavecount
        waveCount = self.dataFont.render("Wave: "+ str(self.wave),True,(0,0,0))
        self.screen.blit(waveCount,(190,20))

#MAKE CLASS BASED

g = GameController(750,520,60)
g.run()