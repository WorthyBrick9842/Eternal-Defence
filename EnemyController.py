import random,math,Variables,statsMap,Entities
class EnemyController:
    def __init__(self):
        #skeleton not included as it is spawned by necromancer
        self.enemies = ["Goblin","Spear Orc","Dark Knight","Giant Ogre","Necromancer"]

    def newWave(self,waveNum):
        if (waveNum+1) %10 == 0 and waveNum !=-1:
            print("boss wave")
            self.bossWave()
        else:
            print("Normal wave")
            self.createWave(waveNum)

    def createWave(self,waveNum):
        # create a map of the weights for this round
        weightMap = {
            "Goblin" : max(10-waveNum,1),
            "Spear Orc" : max(8-waveNum,1),
            "Dark Knight" : max((waveNum-5)*0.7,0),
            "Giant Ogre" : max((waveNum-10)*0.7,0),
            "Necromancer" : max((waveNum-10)*0.2,0)            
        }
        total = sum(weightMap.values())

        weightMap = {k:v/total for k,v in weightMap.items()}
        numEnemies = waveNum + 4
        # numEnemies = 1
        #numEnemies = 1 ##########################################################################################################
        for i in range(numEnemies):
            point = random.randint(1,100)/100
            total = 0
            for name,weight in weightMap.items():
                total = total+weight
                if point < total:
                    self.spawnEnemy(name)
                    point = 2
                
                    

    def spawnEnemy(self,enemyName):
        angle = random.randint(0,355)
        # angle = 91
        # angle = math.radians(angle)
        
        x = int(250+(math.cos(angle)*240))
        y = int(250+(math.sin(angle)*240))
        Variables.entities[1].append(Entities.Ground(enemyName,statsMap.statsMap[enemyName],(x,y)))
    def bossWave(self):
        #choose a random enemy to use as a boss
        boss = random.choice(self.enemies)
        self.spawnEnemy(boss)

        print("creating a boss wave")
        #upgrade the stats of the enemy
        print("Old stats:",Variables.entities[1][0].health, Variables.entities[1][0].damage,Variables.entities[1][0].speed )
        Variables.entities[1][0].health = 10* Variables.entities[1][0].health
        Variables.entities[1][0].damage = 5* Variables.entities[1][0].damage
        Variables.entities[1][0].speed = round(0.75*Variables.entities[1][0].speed,2)
        print("New stats:",Variables.entities[1][0].health, Variables.entities[1][0].damage,Variables.entities[1][0].speed )
        
# EC= EnemyController()
# EC.createWave(1)