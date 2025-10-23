import math,statsMap,pygame,Variables,resourceManager
grid = []

class Entity:
    def __init__(self, name,data ,pos):
        # define the key Variables mostly from the statsMap data structure
        self.texture = resourceManager.load_image(name+".png")
        self.rect = self.texture.get_rect()
        self.name = name
        self.type = data["type"]
        self.pos =  [pos[0],pos[1]]
        self.rect.center = self.pos
        #print(name+"jpg")
        self.timeOfLastAtk = 0
        self.health = data["health"]
        self.damage = data["damage"]
        self.range = data["range"]
        self.atkState = False
        self.target = None
        self.lastTicks = 0
        
        self.cellPos = Variables.underlyingGrid.findcell(self.rect.center)
        Variables.underlyingGrid.updateCellType(self.cellPos,self.type)
        Variables.underlyingGrid.updateCellWeight(self.cellPos,1)
        # self.money  = money - data["cost"]
    def destroy(self):
        if self.type =="unit":
            Variables.entities[0].remove(self)
        else:
            Variables.entities[1].remove(self)
    def draw(self,screen):
        screen.blit(self.texture,(self.rect.topleft))
    def changeState(self):
        self.atkState = not self.atkState
    def upgrade(self,upgradeValue):
        self.health = self.health + (self.health * upgradeValue)
        self.damage = self.damage + (self.damage * upgradeValue)
        # cannot edit statsmap from here as every entity would increase the value
    def __repr__(self):
        return f"{self.name}, {self.pos}, {self.cellPos}"
class Tower(Entity):
    def __init__(self,name,data,pos):
        super().__init__(name,data,pos)  
        self.fireRate = data["atkspeed"]
        self.AOE = 10
    def findTarget(self):
        # find the closest enemy to the defence unit
        # as it is a tower, I do not need to check if it is an enemy
        closest = math.inf
        targets = Variables.entities[1]
        for entity in targets:
            #calcualte the distance to the target
            distance = (self.pos[0]-entity.pos[0])**2 + (self.pos[1]-entity.pos[1])**2
            if distance < closest:
                self.target = entity
                closest = distance

    def Attack(self):
        # the tower can only be a unit, so anything it kills will drop money
        # check the range against the distance
        distance = math.sqrt((self.pos[0]-self.target.pos[0])**2+(self.pos[1]-self.target.pos[1])**2)
        if distance < self.range:
            if self.target.health <= self.damage:
                self.changeState()
                # add the enemies max health to the score
                score = score + statsMap.statsMap[self.target.name]["health"]
                self.target = None
            self.target.takeDamage(self.damage)
        else:
            self.changeState()
    def update(self,ticks):
        # only attack if the elapsed time is > fireRate
        if self.atkState and (ticks-self.lastTicks) >= self.fireRate:
            self.Attack()
        elif self.target ==None:
            self.findTarget()

class Ground(Entity):
    def __init__(self,name,data,pos):
        #print("Name: ",name,"Data: ",data,"Pos: ",pos)
        super().__init__(name,data,pos) 
        self.idle = True
        self.speed = statsMap.statsMap[name]["speed"]
        self.directionVec = []
        self.atkSpeed = statsMap.statsMap[name]["atkspeed"]
        self.visRange = statsMap.statsMap[name]["visibleRange"]
        self.path = []
        self.pathCount = 0
        self.pathRefresh = 3
    def getDistance(self,target):
        return math.sqrt((self.pos[0]-target.rect.center[0])**2+(self.pos[1]-target.rect.center[1])**2)
    def move(self):
        #position is stored in the array [x,y]
        #direction is soted in the array [dx,dy]
        
        self.pos[0] += self.directionVec[0]
        self.pos[1] += self.directionVec[1]
        self.rect.centerx = int(self.pos[0])
        self.rect.centery = int(self.pos[1])
        if Variables.underlyingGrid.findcell(self.rect.center) == self.path[0]:
            print(self,"Node reached")
            self.path.pop(0)
            if len(self.path) >0:
                self.getDirection()
            else:
                self.idle = True
        if Variables.underlyingGrid.findcell(self.rect.center) != self.cellPos:
            # print(self.cellPos)
            Variables.underlyingGrid.updateCellType([self.cellPos[0],self.cellPos[1]],"empty")
            Variables.underlyingGrid.updateCellWeight([self.cellPos[0],self.cellPos[1]],0)

            self.cellPos = Variables.underlyingGrid.findcell(self.rect.center)

            Variables.underlyingGrid.updateCellType([self.cellPos[0],self.cellPos[1]],self.type)
            Variables.underlyingGrid.updateCellWeight([self.cellPos[0],self.cellPos[1]],1)

    def findTarget(self):
        closest = 0
        if self.type == "enemy":
            self.target = Variables.castleObject 
        else:
            possTargets = Variables.entities[1]
            # if len(possTargets) == 0:
            #     self.idle = True
            # else:
            #     self.idle = False
            for possTarget in possTargets:
                distance = self.getDistance(possTarget)
                if distance < closest or closest == 0:
                    closest = distance
                    self.target = possTarget
            if closest > self.visRange:
                self.target = None
        #print("Target: ",self.target)
    def findPath(self):
        if not self.path:
            self.path = Variables.underlyingGrid.pathfind(self.cellPos,self.target.cellPos)
            # for step in path:
            #     self.path.append(Variables.underlyingGrid.getCellPos(step))
            if self.path:
                self.getDirection()
        #print(self.name,":",self.path)

    def getDirection(self):
        # #get directions to the next path location
        nextStep = Variables.underlyingGrid.getCellPos(self.path[0])
        dx = nextStep[0]-self.rect.centerx
        dy = nextStep[1]-self.rect.centery
        self.directionVec = [(nextStep[0]-self.rect.center[0]),(nextStep[1]-self.rect.center[1])]

        if dx !=0:
            angle = math.fabs(math.atan(dy / dx))#
        else:
            angle = math.pi/2 # makes the x 0 and the y 1

        if (dx > 0):
            self.directionVec[0] = self.speed * math.cos(angle)
        else:
            self.directionVec[0] = -self.speed * math.cos(angle)
        if (dy > 0):
            self.directionVec[1] = self.speed * math.sin(angle)
        else:
            self.directionVec[1] = -self.speed * math.sin(angle)
    def TakeDamage(self,damage,attacker):
        if self.type in ["Goblin","Spear Orc"]:
            print(f"{self.name} is taking damage")
        self.health -= damage
        if self.health<= 0:
            if self.type == "unit":
                Variables.entities[0].remove(self)
            else:
                try:
                    Variables.entities[1].remove(self)
                    Variables.money += statsMap.statsMap[self.name]["health"]
                    Variables.score += statsMap.statsMap[self.name]["health"]
                except ValueError:
                    print("there was a value error")
                    pass

        else:
            if self.target != attacker:
                self.target = attacker
                self.atkState = True
        
    def Attack(self,frame):
        ################################################################################################################################
        #frame resets to 0 after 3600 frames
        #need to reset counter then as well
        #if the time of the last attack is greater than the frame (3550 -> 10)
        timeSinceLastAtk = (frame - self.timeOfLastAtk)/60

        if self.timeOfLastAtk > frame:
            # wait till frame is what the next attack time would have been -3600
            if frame > (self.timeOfLastAtk+(self.atkSpeed*60)-3600):
                timeSinceLastAtk = frame
        if timeSinceLastAtk<0: 
            self.timeOfLastAtk = 0


        if timeSinceLastAtk > self.atkSpeed: # does not constantly attack
            if self.name == "Archer":print(f"archer is shooting at {self.target}")
            if self.target.health <= self.damage: # will this attack kill the target
                self.atkState = False
                self.target.TakeDamage(self.damage,self)
                self.target = None 
                self.idle = True
                self.path = []
            else:
                self.target.TakeDamage(self.damage,self)
            self.timeOfLastAtk = frame
    def update(self,frame):
        self.pathCount +=1
        #print(self,self.target,self.idle)
        #checks to make sure that the target still exists
        if self.target == None: 
            self.idle = True
        elif self.target not in Variables.entities[1] and self.target != Variables.castleObject:
                self.idle = True
        if  self.idle:
            self.findTarget()
            if self.target != None:
                self.findPath()
                self.idle = False

        elif self.atkState:
            #if self.name == "Archer":print(f"{self.name} has {self.target.name} as a target")
            distToTarget = self.getDistance(self.target)
            if distToTarget <= self.range:
                self.Attack(frame)########################################################
            else:
                self.atkState = False
            # if self.target == None:
            #     self.idle = True
        else:
            
            if self.target == None:
                self.idle = True
            else:
                # check to change states
                distToTarget = self.getDistance(self.target) 
                if distToTarget < self.range:
                    self.atkState = True
                # if there is a target then move to it
                #print("testing:",self,self.target,self.idle)

                if self.pathCount >= self.pathRefresh or len(self.path) == 0:
                    self.path = []
                    self.findPath()
                    self.pathCount = 0
                if self.path:
                    self.move()

    def reset(self):
        self.path = []
        self.target = None
        self.idle = False
class necromancer(Ground):
    def __init__(self,name,data,pos):
        super().__init__(name,data,pos)
        self.spawnRate = statsMap.statsMap[self.name]["spawn number"]
    def spawnDead(self):
        for i in range(1,5):
            Variables.entities.append(Ground("skelleton"),statsMap.statsMap["Skeleton"],self.pos)
            #     try:
            #     self.target.TakeDamage(self.damage,self)
            # except AttributeError:
            #     self.target = None
class Physical(Entity):
    def __init__(self,name,pos):
        super().__init__(name,statsMap.statsMap[name],pos)
        self.resistance = statsMap.statsMap[name]["resistance"]
        self.damageState = 4
        self.maxHealth = statsMap.statsMap[name]["health"]
        # self.cell = grid.findCell(pos[0],pos[1])
        # grid[self.cell[0]][self.cell[1]].updateType()
    def TakeDamage(self,dmg,attacker):
        # if health is a multiple of 0.25* maxheaalth, change Skins
        self.health -= dmg
        if self.health <= 0:
            if self == Variables.castleObject:
                Variables.castleObject = None
            else:
                self.destroy()
        else:
            if (self.health / self.maxHealth) < (0.25*self.damageState) and self.damageState >0:
                self.damageState -=1
                # CHANGE TEXTURE
                newTexture = "castle "+str(self.damageState)+".png"
                self.texture = resourceManager.load_image(newTexture).convert_alpha()
                #self.texture = pygame.image.load().convert_alpha()
            self.Attack(attacker)
    def Attack(self,attacker):
        attacker.TakeDamage(attacker.health,self)
    def changeTexture(self,newTexture):
        self.texture = newTexture


# t = Tower("Swordsman",statsMap.statsMap["Swordsman"],(0,0))
# a1 = Tower("Archer",statsMap.statsMap["Archer"],(10,50))
# a2 = Tower("Archer",statsMap.statsMap["Archer"],(10,10))
# a3 = Tower("Archer",statsMap.statsMap["Archer"],(50,50))
# t.upgrade(1.5)
# t.findTarget()

# print(Variables.entities) 