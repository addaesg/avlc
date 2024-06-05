import pygame
from game.Point import Point, ControlPoints
import game.Color as Color
import numpy as np
import math
from game.Caption import Caption, BoxCaption
from game.LinearEquation import linear_solve


class Aura:
    def __init__(self, points, thickness=1, color=Color.WHITE):
        self.points = points
        self.color = color
        self.thickness = max([thickness + 1, thickness + thickness/3])

    def draw(self, screen, samples):
        for point in samples:
            pygame.draw.circle(screen, self.color, point.pos(), self.thickness) 
        for point in samples:
            point.draw(screen)