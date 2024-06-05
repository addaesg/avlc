import pygame
import game.Color as Color
import numpy as np
import math

class Caption:
    def __init__(self, text, position, size, color=Color.WHITE):
        self.text = text
        self.position = position
        self.color = color
        self.size = size 

    def draw(self, screen):
        ## draw a small filled square to the left of the caption text with the same color as the caption and scaled to the font size
        pygame.draw.rect(screen, self.color, (self.position[0] - self.size, self.position[1] - self.size/4, self.size, self.size))
        ## draw the caption text
        font = pygame.font.Font(None, self.size)
        text = font.render(self.text, True, self.color)
        screen.blit(text, self.position)
        ## create a white 1pixel aura around the text and the square
        pygame.draw.rect(screen, Color.WHITE, (self.position[0] - self.size, self.position[1] - self.size/4, self.size, self.size), 1)
        text = font.render(self.text, True, Color.WHITE)
        screen.blit(text, self.position)
        
        




class BoxCaption:
    def __init__(self, font_size=20):
        self.captions = []
        self.font_size = font_size
    
    def add_caption(self, text, color=Color.WHITE):
        ## position the caption below the lowest caption
        position = (50, 50 + 50*len(self.captions))
        self.captions.append(Caption(text, position, self.font_size, color))

    def draw(self, screen):
        for i, caption in enumerate(self.captions):
            caption.draw(screen)