import random,math,Variables,statsMap,Entities
class EnemyController:
    def __init__(self):
        #skeleton not included as it is spawned by necromancer
        self.enemies = ["Goblin","Spear Orc","Dark Knight","Giant Ogre","Necromancer"]
    def newWave(self,waveNum):
        if waveNum %10 == 0:
            self.bossWave()
        else:
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
#        angle = math.radians(angle)
        
        x = int(250+(math.cos(angle)*240))
        y = int(250+(math.sin(angle)*240))
        Variables.entities[1].append(Entities.Ground(enemyName,statsMap.statsMap[enemyName],(x,y)))
    def bossWave(waveNum):
        pass
# EC= EnemyController()
# EC.createWave(1)