import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from game.Point import Point, ControlPoints
from game.Window import Window
from game.Curve import BezierCurve
import game.Color as Color
from sys import exit
import numpy as np


def main():
    (width, height) = (800, 600)
    backgroundColor = Color.BLACK
    window = Window(width, height, "Curvinha Fellas", backgroundColor)

    controlPoints = ControlPoints([], 11, Color.BLUE)
    bezierCurve = BezierCurve(controlPoints.points, Color.CYAN, 6, 10000)

    while window.is_open():
        events = window.pool_events()
        controlPoints.handle_events(events)
        
        window.draw(controlPoints)
        window.draw(bezierCurve)
        window.update()    
    

if __name__ == "__main__":
    main()