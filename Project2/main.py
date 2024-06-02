import pygame
from game.Point import Point, ControlPoints
from game.Window import Window
import game.Color as Color
from sys import exit
import numpy as np


def main():
    (width, height) = (800, 600)
    backgroundColor = Color.BLACK
    pygame.init()
    window = Window(width, height, "Curvinha Fellas")

    controlPoints = ControlPoints([], 11, Color.CYAN)

    while window.is_open():
        events = window.pool_events()
        controlPoints.handle_events(events)
        window.draw(controlPoints)
        
        window.update()    

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()