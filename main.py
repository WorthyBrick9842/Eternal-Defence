import pygame,button,Variables,Entities,statsMap,math,random,EnemyController,time
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
        print(Variables.underlyingGrid.widthPixels)
    def setup(self):
        # A function called before each play of the game
        Variables.entities = [[],[]]
        Variables.castleObject = None
        Variables.money = 15
        Variables.score = 0
        Variables.castleObject = Entities.Physical("Castle",(250,250))
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
        while running:
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
        print(self.replayButton.checkClicked(mousePos,mouseClicked)[0])
        playPressed = self.replayButton.checkClicked(mousePos,mouseClicked)[0]
        if playPressed:
            # False for menu running, true for play
            print("PLAY AGAIN BUTTON PRESSED")
            return False,True
        exitPressed  = self.exitButton.checkClicked(mousePos,mouseClicked)[0]
        if exitPressed:
            #False to close menu and False to close window
            print("EXIT BUTTON PRESSED")
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
        self.buttons = [[],[],[]]
        self.unitPlacementMode = False
        self.unitToPlace = None
        # self.spawnEnemies()
        self.EC = EnemyController.EnemyController()
        # create the unit buttons and distribute them
        self.buttons[0].append(button.Button("",545,150,75,75,"SwordsmanShop.png",(200,200,200),statsMap.statsMap["Swordsman"]
                                             ["cost"],name="Swordsman"))
        self.buttons[0].append(button.Button("",655,150,75,75,"ArcherShop.png",(200,200,200),statsMap.statsMap["Archer"]
                                             ["cost"],name = "Archer"))
        self.buttons[1].append(button.Button("",545,150,75,75,"ArcherTowerShop.png",(200,200,200),statsMap.statsMap["ArcherTower"]
                                             ["cost"],name = "ArcherTower"))        
        # create the shop tabs and add them to a list
        Gtab = button.Button(text="    Ground",x=520,y=75,width=77,height=25,value=0)
        Gtab.changeColour((150,150,150))
        Ttab = button.Button(text="     Tower" ,x=597,y=75,width=77,height=25,value=1)
        Ptab = button.Button(text="   Physical",x=674,y=75,width=78,height=25,value=2)
        self.tabs = [Gtab,Ttab,Ptab]
        self.tabNum = 0
        
        # unit placement graphics
        self.inBoundsSurface = pygame.surface.Surface((500,500),pygame.SRCALPHA)
        self.inBoundsCircle = pygame.draw.rect(self.inBoundsSurface,(255,100,100,125),pygame.Rect(0,0,500,500))
        self.inBoundsCircleOuter = pygame.draw.circle(self.inBoundsSurface,(255,255,255,0),(250,250),self.boundsRadius)
        self.inBoundsCircleInner = pygame.draw.circle(self.inBoundsSurface,(255,100,100,125),(250,250),50)
    def update(self,frame):
    

        if not Variables.entities[1]:
            st = time.time()
            self.EC.createWave(self.wave)
            self.wave +=1
            et = time.time()
            print("Time for wave creation: ",et-st)
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
            #################################################################################################################
            if buttonChecked and Variables.money >= buttonCost and not self.unitPlacementMode:
                self.unitToPlace = buttonName
                self.unitPlacementMode = True
                Variables.money -= buttonCost
                self.placeUnit(self.unitToPlace,mousepos,mouseClicked)

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
            # entity.findTarget()
            # entity.findPath()
            entity.update(frame)
            #see entities range
            #pygame.draw.circle(self.screen,(200,200,200),entity.rect.center,entity.visRange,2)
            #     pygame.draw.circle(self.screen,(255,0,255),Variables.underlyingGrid.getCellPos(step),5)
            
        
        if self.unitPlacementMode:
            self.screen.blit(self.inBoundsSurface,(0,0))
            self.placeUnit(self.unitToPlace,mousepos,mouseClicked)
        
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
        if mousestatus and self.inBounds(mousepos):# 
            #only placing ground units, would be a 'switch case' here for tower or physical
            if self.unitToPlace in ["Swordsman","Archer"]:
                Variables.entities[0].append(Entities.Ground(name=self.unitToPlace,data=statsMap.statsMap[self.unitToPlace],pos=mousepos))
            elif self.unitToPlace in ["ArcherTower"]:
                Variables.entities[0].append(Entities.Tower(name=self.unitToPlace,data=statsMap.statsMap[self.unitToPlace],pos=mousepos))
            print("placed trooper")
            self.unitPlacementMode = False

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
        # draw wavecount
        waveCount = self.dataFont.render("Wave: "+ str(self.wave),True,(0,0,0))
        self.screen.blit(waveCount,(190,20))

#MAKE CLASS BASED

g = GameController(750,520,60)
g.run()