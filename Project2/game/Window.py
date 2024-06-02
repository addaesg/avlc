import pygame
import game.Color as Color

class Window:

    def __init__(self, width, height, title, background=Color.BLACK):
        self.width = width
        self.height = height
        self.title = title
        self.isOpen_ = True
        self.background = background
        pygame.init()
        self.screen_ = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption(self.title)
    
    def is_open(self):
        return self.isOpen_

    def screen(self):
        return self.screen_
    
    def draw(self, thing):
        thing.draw(self.screen())

    def clear(self):
        self.screen_.fill(self.background)

    def update(self):
        if(not self.is_open()):
            self.close()
            return
        pygame.display.update()
        self.clear()

    def close(self):
        self.isOpen_ = False
        pygame.quit()
        exit()

    def pool_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.isOpen_ = False
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   self.isOpen_ = False
        return events
        