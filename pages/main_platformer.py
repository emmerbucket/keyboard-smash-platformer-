import pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Keyboard Smash"


class Player():
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        self.change_x = 0
        self.change_y = 0
    
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y
    
    def update(self):
        self.rect.x += self.change_x
