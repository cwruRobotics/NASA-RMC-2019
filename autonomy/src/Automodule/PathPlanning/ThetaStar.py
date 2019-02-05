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

def reconstruct_path(vertex):
    total_path = {vertex}
    if vertex.getParent() != vertex:
        total_path.push(reconstruct_path(vertex.getParent()))
    else:
        return total_path

def line_of_sight(vertex, vertexTwo):
    x0 = vertex.getPosition().getX_Pos()
    x1 = vertexTwo.getPosition().getX_Pos()
    y0 = vertex.getPosition().getY_Pos()
    y1 = vertexTwo.getPosition().getY_Pos()
    dy = y1 - y0
    dx = x1 - x0
    f = 0
    sx = 0
    sy = 0
    if dy < 0:
        dy = -dy
        sy = -1
    else:
        sy = 1
    if dx < 0:
        dx = -dx
        sx = -1
    else:
        sx = 1
    if dx >= dy:
        while x0 != x1:
            f += dy
            if f >= dx:
                if grid:
                    return False
                y0 += sy
                f -= dx
            if f != 0 & grid:
                return False
            if dy == 0 & grid:
                return False
            x0 += sx
    else:
        while y0 != y1:
            f += dx
            if f >= dy:
                if grid:
                    return False
                x0 += sx
                f -= dy
            if f != 0 & grid:
                return False
            if dx == 0 & grid:
                return False
            y0 += sy
    return True
