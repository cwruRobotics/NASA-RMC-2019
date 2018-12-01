
class Vertex:
    def __init__(self, parent, startDistance, endDistance, visibleNeighbors, location):
        self.parent = parent
        self.startDistance = startDistance
        self.endDistance = endDistance
        self.visibleNeighbors = visibleNeighbors
        self.location = location


    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def getStartDistance(self):
        return self.startDistance

    def setStartDistance(self, startDistance):
        self.startDistance = startDistance

    def getEndDistance(self):
        return self.endDistance

    def setEndDistance(self, endDistance):
        self.endDistance = endDistance

    def getVisibleNeighbors(self):
        return self.visibleNeighbors

    def removeNeighbor(self, vertex):
        self.visibleNeighbors.remove(vertex)
        
    def addNeighbor(self, vertex):
        self.visibleNeighbors.append(vertex)

    def __eq__(self, vertex):
        return self.location == vertex.location

    def getLocation(self):
        return self.location


