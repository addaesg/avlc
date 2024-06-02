import pygame
from game.Point import Point, ControlPoints
import game.Color as Color
import numpy as np
import math

class BezierCurve:
    def __init__(self, controlPoints, color=Color.WHITE, width=10, samples=10000):
        self.controlPoints = controlPoints
        self.color = color
        self.thickness = width
        self.samples = []
        self.sampleCount = samples
        self.dated = True
    
    def calculate(self):
        self.samples = []
        n = len(self.controlPoints) - 1
        for t in np.arange(0, 1, 0.001):
            sample = np.zeros(2)
            for i in range(n + 1):
                control = self.controlPoints[i]
                control = np.array([control.x, control.y])
                idk = (math.factorial(n)/(math.factorial(i)*math.factorial(n-i))) *((1-t)**(n-i))*(t**i)
                sample += np.dot(idk, control)
            sample = sample.astype(int)
            self.samples.append(Point(sample[0], sample[1], self.thickness, self.color))

    def draw(self, screen):
        self.calculate()
        for point in self.samples:
            point.draw(screen)
        for i in range(1, len(self.controlPoints)):
            pygame.draw.line(screen, Color.BLUE, self.controlPoints[i-1].pos(), self.controlPoints[i].pos(), self.thickness)



