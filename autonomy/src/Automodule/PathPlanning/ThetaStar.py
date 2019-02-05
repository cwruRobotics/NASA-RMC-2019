from collections import deque
import math

def aStar(start, end):
    openList = [start]
    start.setStartDistance(0)
    start.setEndDistance(start.getPosition().distanceTo(end.getPosition()))
    closedList = []
    while openList.__len__() > 0:
        bestDist = openList[0].getStartDistance() + openList[0].getEndDistance()
        bestIndex = 0
        # find next vertex to try
        for i in range (1, openList.__len__()):
            if (openList[i].getStartDistance() + openList[i].getEndDistance()) < bestDist:
                bestDist = openList[i].getStartDistance() + openList[i].getEndDistance()
                bestIndex = i
        if openList[bestIndex] == end:
            # reached end, need to create path then exit
            path = deque()
            node = openList[bestIndex]
            while node is not None:
                path.appendleft(node.getPosition)
                node = node.getParent()
            return
        # add neighbors of best looking vertex if they aren't in the closed list
        for node in openList[bestIndex].getVisibleNeighbors:
            # iterate through closed list to check if node has already been considered
            inClosed = False
            for nodeTwo in closedList:
                if node == nodeTwo:
                    inClosed = True
            tempScore = openList[bestIndex].getStartDistance() + node.getPosition().distanceTo()(openList[bestIndex].getPosition())
            tempScore += node.getPosition().distanceTo(end.getPosition())
            inOpen = False
            # iterate through open list to check if node can be reached in a better way
            for nodeTwo in openList:
                if node == nodeTwo:
                    inOpen = True
                    if tempScore < nodeTwo.getStartDistance() + nodeTwo.getEndDistance():
                        nodeTwo.setParent(openList[bestIndex])
                        node.setStartDistance(node.getParent().getStartDistance() + node.getPosition().distanceTo(
                            node.getParent().getPosition()))
                        node.setEndDistance(node.getPosition().distanceTo(end.getPosition()))
            # if node is new, add it to the open set
            if not inClosed and not inOpen:
                node.setParent(openList[bestIndex])
                node.setStartDistance(node.getParent().getStartDistance() + node.getPosition().distanceTo(node.getParent().getPosition()))
                node.setEndDistance(node.getPosition().distanceTo(end.getPosition()))
                openList.append(node)
        closedList.append(openList[bestIndex])
        openList.remove(openList[bestIndex])

def thetaStar(start, goal):
    start.setStartDistance(0)
    start.setParent(start)
    open = {}
    open.insert(start, start.getStartDistance() + start.getEndDistance())
    closed = {}
    while open != 0:
        s = open.pop()
        if s == goal:
            return reconstruct_path(s)
        closed.push(s)
        for neighbor in s.getVisibleNeighbors():
            if neighbor != 0:
                if neighbor == open:
                    neighbor.setStartDistance(math.inf)
            neighbor.setParent(None)
            update_vertex(s, neighbor)
    return None

def update_vertex(vertex, neighbor):
    if line_of_sight(vertex.getParent(), neighbor):
        if vertex.getParent().getStartDistance() + vertex.getParent().getPosition().distanceTo(neighbor.getPosition()) < neighbor.getStartDistance():
            neighbor.setStartDistance(vertex.getParent.getStartDistance() + vertex.getParent().getPosition().distanceTo(neighbor.getPosition()))
            neighbor.setParent(vertex.getParent())
            if neighbor in open:
                open.remove(neighbor)
            open.insert(neighbor, neighbor.getStartDistance() + neighbor.getEndDistance())
    else:
        if vertex.getStartDistance() + vertex.getPosition().distanceTo(neighbor.getPosition()) < neighbor.getStartDistance():
            neighbor.setStartDistance(vertex.getStartDistance() + vertex.getPosition().distanceTo(neighbor.getPosition()))
            neighbor.setParent(vertex)
            if neighbor in open:
                open.remove(neighbor)
            open.insert(neighbor, neighbor.getStartDistance() + neighbor.getEndDistance())

def reconstruct_path(s):
    total_path = {s}
    if s.getParent() != s:
        total_path.push(reconstruct_path(s.getParent()))
    else:
        return total_path

def line_of_sight(vertex, vertexTwo):

