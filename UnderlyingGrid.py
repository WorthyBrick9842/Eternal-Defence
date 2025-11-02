import math,heapq,random
class Node:
    def __init__(self,row,column):
        self.row = row
        self.col = column
        self.occupationType = None
        self.weight= 0
        # pathfinding variables
        self.fCost = math.inf
        self.gCost = math.inf
        self.parent = None
        self.occupant = None
    def updateOccupantType(self,newOccupantType):
        self.occupationType = newOccupantType
    def updateOccupant(self,newOccupant):
        self.occupant = newOccupant
    def updateWeight(self,newWeight):
        self.weight = newWeight
    def resetPathfinding(self):
        self.fCost = math.inf
        self.gCost = math.inf
        self.parent = None
    def __repr__(self):
        return f"({self.col},{self.row})"
        #return f"{self.weight}"
        #return f"{self.test}"
    def __lt__(self,other):
        if self.fCost != other.fCost:
            return self.fCost < other.fCost
        else:
            return self.gCost < other.gCost
        
class underlyingGrid:
    def __init__(self,widthCols,heightRows,xPos,yPos,widthPixels,heightPixels):
        self.pos = (xPos,yPos)
        self.widthCols = widthCols
        self.heightRows = heightRows
        self.widthPixels = widthPixels
        self.heightPixels = heightPixels
        self.nodeWidth = self.widthPixels // self.widthCols
        self.nodeHeight = self.heightPixels // self.heightRows
        self.grid = [[Node(i,j)for j in range(widthCols)]for i in range(heightRows)]

        self.nearby_squares= [(-1,-1),(-1,0),(-1,1),
                 ( 0,-1),       ( 0,1),
                 ( 1,-1),( 1,0),(+1,1)]
    def getCellPos(self,cellPos):
        # how many boxes in, + the offset, + half the box width
        posX = int((cellPos[0] * self.nodeWidth) + self.pos[0] + (0.5* self.nodeWidth))
        posY = int((cellPos[1] * self.nodeHeight)+ self.pos[1] + (0.5* self.nodeHeight))
        return (posX,posY)
    
    def findcell(self,pos):
        # find the x column by removing the offset (grid may only start at x=50) 
        # then caclualting how many squares can be fittedd
        xCol = int((pos[0] - self.pos[0]) / self.nodeWidth)
        yRow = int((pos[1]-self.pos[1]) / self.nodeHeight)
        #print(self.nodeWidth)
        try:
            cell = self.grid[yRow][xCol]
            return (cell.col,cell.row)
        except IndexError:
            print("Input location was out of bounds")
            print(pos)
            print(xCol,yRow)
            return "error"
    def updateCellType(self,cellPos,newType):
        #print(cellPos)
        self.grid[cellPos[1]][cellPos[0]].updateOccupantType(newType)
    def updateCellOccupant(self,cellPos,newOccupant):
        self.grid[cellPos[1]][cellPos[0]].updateOccupant(newOccupant)
    def updateCellWeight(self,cellPos,newWeight):
        self.grid[cellPos[1]][cellPos[0]].updateWeight(newWeight)
    def resetCell(self,cellPos):
        self.grid[cellPos[1]][cellPos[0]].updateOccupantType(None)
        self.grid[cellPos[1]][cellPos[0]].updateOccupant(None)
        self.grid[cellPos[1]][cellPos[0]].updateWeight(0)
    def get_nearby_nodes(self,openNodes,grid,currentNode):
        nearNodes = []
        for near_sqr in self.nearby_squares:
            try:
                adjNode = grid[currentNode.row+near_sqr[1]][currentNode.col+near_sqr[0]]
                if self.validSquare(currentNode,adjNode):
                    nearNodes.append(adjNode)
                    
                else:
                    pass
            except:
                IndexError 
        return nearNodes
    def validSquare(self,currNode,adjNode):
        if adjNode.col< len(self.grid[0]) and adjNode.row< len(self.grid):
            if self.getH(currNode,adjNode) <= 15:
                return True
        return False
    def getH(self,a,b):
        return round(math.sqrt((b.col-a.col)**2 +(b.row-a.row)**2)*10,5)
    def pathfind(self,startPos,endPos):
        openNodes = []
        start = self.grid[startPos[1]][startPos[0]]
        end = self.grid[endPos[1]][endPos[0]]

        heapq.heappush(openNodes,(0,start))
        start.fCost = self.getH(start,end)
        start.gCost = 0
        while len(openNodes) !=0:
            currentNode = heapq.heappop(openNodes)[1]
            if currentNode == end:
                break
            #get neighbousring nodes
            neighbours = []
            neighbours = self.get_nearby_nodes(openNodes,self.grid,currentNode)
            for neighbour in neighbours:
                possGCost = currentNode.gCost+self.getH(currentNode,neighbour)
                possGCost+=neighbour.weight#(possGCost*neighbour.walkable)
                if possGCost < (neighbour.gCost):
                    neighbour.parent = currentNode
                    neighbour.gCost = possGCost
                    neighbour.fCost = possGCost + self.getH(neighbour,end)
                    heapq.heappush(openNodes,(neighbour.fCost,neighbour))
        pathofNodes = []
        while currentNode != start:
            pathofNodes.append(currentNode)
            currentNode = currentNode.parent
        pathofNodes.reverse()
        # print(start,"->",end)
        # print(pathofNodes)
        for row in self.grid:
            for node in row:
                node.resetPathfinding()
        path = []
        for node in pathofNodes:
            path.append((node.col,node.row))
        return path
    def drawGrid(self):
        for row in self.grid:
            print(row)
            
# testGrid = underlyingGrid(widthCols=10,heightRows=10,xPixels=50,
#                           yPixels=50,widthPixels=100,heightPixels=100)
#
# testGrid.updateCell((5,5),newWeight= 10)
# testGrid.updateCell((5,6),newWeight= 10)
# testGrid.updateCell((6,5),newWeight= 10)
# testGrid.updateCell((6,6),newWeight= 10)
#testGrid.drawGrid()
# for i in range(10):
#     testGrid.pathfind([random.randint(0,9),random.randint(0,9)],
#                       [random.randint(0,9),random.randint(0,9)])
    #testGrid.drawGrid()
# # 150,150 should put us in 
# print("Valid test: ",testGrid.findcell(75,75))
# print("Valid test: ",testGrid.findcell(125,74))
# print("border test: ",testGrid.findcell(50,50))
# print("Border test: ",testGrid.findcell(150,150))
# print("Invalid test: ",testGrid.findcell(1500,1500))

