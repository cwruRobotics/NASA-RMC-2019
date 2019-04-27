#!/usr/bin/env python

import heapq as h
import math
from PathPlanning import Grid, Path

def create_path(start, end, areana_width, arena_height, obstacles):
    grid = Grid(start, end, areana_width, arena_height)
    for obs in obstacles:
        grid.addObstacle(obs)

    for i in range(grid.row_size):
        for j in range(grid.col_size):
            v = grid.getVertex(i, j)
            neighbors = grid.getNeighbors(i, j)
            for neighbor in neighbors:
                v.addNeighbor(neighbor)

    grid_start_coord = grid.getGridCoordinates(start.getX(), start.getY())
    grid_end_coord = grid.getGridCoordinates(end.getX(), end.getY())

    return thetaStar(grid_start_coord, grid_end_coord, grid)

def thetaStar(start, end, grid):
    startVertex = grid.getVertex(int(start[0]), int(start[1]))
    startVertex.setDistance(0)
    endVertex = grid.getVertex(int(end[0]), int(end[1]))
    updateHeuristic(endVertex, grid)

    print str(startVertex)
    print str(endVertex)

    openList = []
    closedList = []

    h.heappush(openList, startVertex)
    while len(openList) != 0:
        currentVertex = h.heappop(openList)
        if currentVertex == endVertex:
            return postProcess(reconstructPath(currentVertex), grid)

        closedList.append(currentVertex)
        currentCoordinate = grid.getGridCoordinates(currentVertex.getX(), currentVertex.getY())

        for neighbor in grid.getNeighbors(currentCoordinate[0], currentCoordinate[1]):
            if neighbor not in closedList:
                temp = currentVertex.getDistance() + currentVertex.distanceTo(neighbor)
                if temp < neighbor.getDistance():
                    neighbor.setDistance(temp)
                    neighbor.setParent(currentVertex)
                    if neighbor in openList:
                        h.heapify(openList)
                    else:
                        h.heappush(openList, neighbor)
                if neighbor not in openList:
                    h.heappush(openList, neighbor)
    print 'could not find the path'
    return None

def reconstructPath(v, acc=None):
    if acc is None:
        acc = []
    acc.insert(0, v)
    if v.getParent() is None:
        return Path(acc)
    else:
        return reconstructPath(v.getParent(), acc)

def updateHeuristic(end, grid):
    for i in range(grid.row_size):
        for j in range(grid.col_size):
            v = grid.getVertex(i, j)
            v.setHeuristic(v.distanceTo(end))

def postProcess(path, grid):
    length = len(path)
    done = False
    print str(len(path))
    while not done:
        path = postProcess_iter(path, grid)
        if len(path) == length:
            done = True
        else:
            length = len(path)
    print str(len(path))
    done = False
    length = len(path)
    while not done:
        path = remove_adjacents(path, math.sqrt(grid.unit_width ** 2 + grid.unit_height ** 2))
        if len(path) == length:
            done = True
        else:
            length = len(path)
    print str(len(path))
    done = False
    length = len(path)
    while not done:
        path = postProcess_iter(path, grid)
        if len(path) == length:
            done = True
        else:
            length = len(path)
    return path

def remove_adjacents(path, unit_dist):
    current = 0
    done = False
    while not done:
        pos = path.path[current]
        if current + 1 < len(path):
            if pos.distanceTo(path.path[current + 1]) <= unit_dist:
                if current + 2 < len(path):
                    path.path[current + 2].setParent(pos)
                    path.delete(path.path[current + 1])
                else:
                    path.path[current - 1].setParent(path.path[current + 1])
                    path.delete(pos)
                    done = True
            else:
                current += 1
        else:
            done = True
    return path

def postProcess_iter(path, grid):
    current = 0
    done = False
    while not done:
        if len(path.path) >= current + 3:
            if not checkBlocked(path.path[current], path.path[current + 2], grid):
                path.path[current + 2].setParent(path.path[current])
                path.delete(path.path[current + 1])
            else:
                current += 1
        else:
            done = True

    return path

def checkBlocked(p1, p2, grid):
    v1 = grid.getGridCoordinates(p1.getX(), p1.getY())
    v2 = grid.getGridCoordinates(p2.getX(), p2.getY())
    for i in range(int(min(v1[0], v2[0])), int(max(v1[0], v2[0])) + 1):
        for j in range(int(min(v1[1], v2[1])), int(max(v1[1], v2[1])) + 1):
            if grid.blocked(i, j):
                return True
    return False

