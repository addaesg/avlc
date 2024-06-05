import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from game.Point import Point, ControlPoints
from game.Caption import BoxCaption
from game.Window import Window
from game.Curve import BezierCurve, InterpolatedCurve, MonomialInterpolatedCurve
import game.Color as Color
from sys import exit
import numpy as np