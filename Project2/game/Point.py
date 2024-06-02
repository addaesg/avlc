import pygame
import game.Color as Color

class Point: 
    def __init__(self, x, y, size = 15, color=Color.CYAN):
        self.x = x
        self.y = y
        self.color = color 
        self.size_ = size

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size_)

    def distTo(self, point):
        return ((self.x - point.x)**2 + (self.y - point.y)**2)
    
    def pos(self):
        return (self.x, self.y)
    
    def move(self, point):
        self.x, self.y = point.pos()
    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"
    def isCloseTo(self, p, tolerance):
        return self.distTo(p) < self.size_**2 * tolerance


class ControlPoints: 
    def __init__(self, points, point_size=15, point_color=Color.CYAN):
        self.points = points
        self.point_size = point_size
        self.point_color = point_color
        self.selectedPoint = None
        self.pressing = False

    def draw(self, screen):
        for point in self.points:
            point.draw(screen)

    def addPoint(self, x, y):
        self.selectedPoint = Point(x, y, self.point_size , self.point_color)
        self.points.append(self.selectedPoint)

    def removePoint(self, point):
        self.points.remove(point)

    def move(self, point, pos):
        self.points[self.points.index(point)].move(pos)

    def getClosestPoint(self, p):
        dists = [p.distTo(point) for point in self.points]
        minDist = min(dists)
        point = self.points[dists.index(minDist)]
        if(p.isCloseTo(point, 3)):
            return point
        return None

    def handle_events(self, events):
        x, y = pygame.mouse.get_pos()
        mouse = Point(x, y)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pressing = True
                if(self.selectedPoint):
                    if(mouse.isCloseTo(self.selectedPoint, 3)):
                        continue
                    self.selectedPoint = None

                if(len(self.points) == 0):
                    self.addPoint(x, y)
                    continue 

                closestPoint = self.getClosestPoint(mouse)
                if(closestPoint):
                    self.selectedPoint = closestPoint
                else:
                    self.addPoint(x, y)  
            
            if event.type == pygame.MOUSEMOTION:
                if self.pressing and self.selectedPoint:
                    self.move(self.selectedPoint, mouse)

            if event.type == pygame.MOUSEBUTTONUP:
                self.pressing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.points = []
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    if self.selectedPoint:
                        self.removePoint(self.selectedPoint)
                        self.selectedPoint = None
                        self.pressing = False
