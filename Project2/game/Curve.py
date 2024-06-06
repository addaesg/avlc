import pygame
from game.Point import Point, ControlPoints
import game.Color as Color
import numpy as np
import math
from game.Caption import Caption, BoxCaption
from game.LinearEquation import plu_solve
from game.Render import Aura


class MonomialInterpolatedCurve:
    def __init__(self, controlPoints, color=Color.WHITE, width=10, caption=BoxCaption(), sample_ratio=0.5):
        self.controlPoints = controlPoints
        self.color = color
        self.thickness = width
        self.samples = []
        self.dated = True
        self.caption = caption
        self.caption.add_caption("Monomial", self.color)
        self.render = Aura(self.samples, self.thickness)
        self.sample_ratio = sample_ratio
    ## Monomial Interpolation
    def calculate(self):
        numberOfPoints = len(self.controlPoints)
        if(numberOfPoints == 0):
            return
        exponents = np.arange(numberOfPoints, dtype=np.float64)
        matrix = np.zeros((numberOfPoints, numberOfPoints), dtype=np.float64)
        column_vector_Y = np.zeros(numberOfPoints, dtype=np.float64)
        for idx, p in enumerate(self.controlPoints):
            matrix[idx, :] = np.power(p.x, exponents)
            column_vector_Y[idx] = p.y
        
        self.samples.clear()
        self.controlPoints.sort(key=lambda p: p.x)
        try:
            coeficients = plu_solve(matrix, column_vector_Y)
            for x in np.arange(self.controlPoints[0].x, self.controlPoints[-1].x, self.sample_ratio, dtype=np.float64):
                y =  np.sum(np.power(x, exponents) * coeficients, dtype=np.float64)
                self.samples.append(Point(x, y, self.thickness, self.color))
            # for x in np.arange(0, 1200, self.sample_ratio, dtype=np.float64):
            #     y =  np.sum(np.power(x, exponents) * coeficients, dtype=np.float64)
            #     self.samples.append(Point(x, y, self.thickness, self.color))
        except:
            self.samples.clear()
            return 

    def draw(self, screen):
        self.calculate()
        self.render.draw(screen, self.samples)



## some other curves
## nice
class LagrangeCurve:
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
            

    


