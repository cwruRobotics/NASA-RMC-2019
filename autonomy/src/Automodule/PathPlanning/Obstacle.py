#!/usr/bin/env python


import math

class Obstacle:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius


    def getCenter(self):
        return [self.center_x, self.center_y]


    def getRadius(self):
        return self.radius


    def setRadius(self, radius):
        self.radius = radius


    def setCenter(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y


    def mergeIfEqual(self, other, maximum_overlap):
        distance_x = self.center_x - other.center_x
        distance_y = self.center_y - other.center_y
        distance = math.sqrt(math.pow(distance_x, 2) + math.pow(distance_y, 2))
        sum_radius = self.radius + other.radius
        if (sum_radius - distance) >= maximum_overlap * distance:
            self.center_x = (self.center_x + other.center_x) / 2
            self.center_y = (self.center_y + other.center_y) / 2
            self.radius = distance / 2