import pygame
from game.Point import Point, ControlPoints
import game.Color as Color
import numpy as np
import math
from game.Caption import Caption, BoxCaption
from game.LinearEquation import linear_solve
from game.Render import Aura

class InterpolatedCurve:
    def __init__(self, controlPoints, color=Color.WHITE, width=10, caption=BoxCaption()):
        self.controlPoints = controlPoints
        self.color = color
        self.thickness = width
        self.samples = []
        self.dated = True
        self.render = Aura(self.samples, self.thickness)
        caption.add_caption("Lagrange", self.color)

    ## Lagrange Interpolation
    def calculate(self):
        self.samples.clear()
        n = len(self.controlPoints) - 1
        for t in np.arange(0, n, 0.005):
            sample = np.zeros(2, float)
            for i in range(n+1):
                control = self.controlPoints[i]
                control = np.array([control.x, control.y])
                p = [1, 1]
                for j in range(n+1):
                    if i != j:
                        p[0] *= t - j
                        p[1] *= i - j
                idk = p[0]/p[1]
                sample += np.dot(control, idk)
            sample = sample.astype(int)
            self.samples.append(Point(sample[0], sample[1], self.thickness, self.color))

    def draw(self, screen):
        self.calculate()
        self.render.draw(screen, self.samples)



class MonomialInterpolatedCurve:
    def __init__(self, controlPoints, color=Color.WHITE, width=10, caption=BoxCaption()):
        self.controlPoints = controlPoints
        self.color = color
        self.thickness = width
        self.samples = []
        self.dated = True
        self.caption = caption
        self.caption.add_caption("Monomial", self.color)
        self.render = Aura(self.samples, self.thickness)

    ## Monomial Interpolation
    def calculate(self):
        numberOfPoints = len(self.controlPoints)
        if(numberOfPoints == 0):
            return
        exponents = np.arange(numberOfPoints)
        matrix = np.zeros((numberOfPoints, numberOfPoints))
        column_vector_Y = np.zeros(numberOfPoints)
        for idx, p in enumerate(self.controlPoints):
            matrix[idx, :] = np.power(p.x, exponents)
            column_vector_Y[idx] = p.y
        
        coeficients = linear_solve(matrix, column_vector_Y.transpose())
        # Determine the range for interpolation
        x_min = min(p.x for p in self.controlPoints)
        x_max = max(p.x for p in self.controlPoints)
        
        # Create a range of x values for interpolation
        x_values = np.linspace(x_min, x_max, num=1000)  # Change '100' to desired number of interpolation points
        
        # Evaluate the polynomial at each x value
        y_values = np.zeros_like(x_values)
        self.samples = []
        for i, x in enumerate(x_values):
            y_values[i] = sum(coeficients[j] * x**j for j in range(numberOfPoints))
            self.samples.append(Point(x, y_values[i], self.thickness, self.color))
        

    def draw(self, screen):
        self.calculate()
        self.render.draw(screen, self.samples)

class BezierCurve:
    def __init__(self, controlPoints, color=Color.WHITE, width=10, caption=BoxCaption()):
        self.controlPoints = controlPoints
        self.color = color
        self.thickness = width
        self.samples = []
        self.dated = True
        self.caption = caption
        self.caption.add_caption("Bezier", self.color)
        self.render = Aura(self.samples, self.thickness)


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
        self.render.draw(screen, self.samples)

        for i in range(1, len(self.controlPoints)):
            pygame.draw.line(screen, Color.WHITE , self.controlPoints[i-1].pos(), 
                             self.controlPoints[i].pos(), self.controlPoints[i].size_ + 1)
    


        for i in range(1, len(self.controlPoints)):
            pygame.draw.line(screen, self.color , self.controlPoints[i-1].pos(), 
                             self.controlPoints[i].pos(), self.controlPoints[i].size_ - 1)
            

    


