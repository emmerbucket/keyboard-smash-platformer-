import pygame
import os

background = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'images', 'christmasbackground1.png'))
background = pygame.transform.scale(background, (800, 600))
walls = []
player = []
floor = []
levelcount = 0

GAME_WIDTH = 800
GAME_HEIGHT = 600

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT ))
pygame.display.set_caption("Keyboard Smash")
clock = pygame.time.Clock()

class Player():
        def __init__(self, x, y):
            super().__init__()

            self.image = pygame.Surface([15, 15])
            self.image.fill(color=(255, 255, 255))

            self.rect = self.image.get_rect(topleft=(x, y))

            self.change_x = 0
            self.change_y = 0
        
        def changespeed(self, x, y):
            self.change_x += x
            self.change_y += y
        
        def update(self):
            self.rect.x += self.change_x

class Floor():
     def __init__(self, y=GAME_HEIGHT - 100, width=GAME_WIDTH, height=75):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color=(123, 228, 229))

        self.rect = self.image.get_rect(topleft=(0, y))

        self.change_x = 0
        self.change_y = 0

player = Player(200, 200)
floor = Floor()

def draw():
    window.blit(background, (0, 0))
    if floor:
        window.blit(floor.image, floor.rect)
    window.blit(player.image, player.rect)


while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
    
    player.update()
    draw()

    pygame.display.update()
    clock.tick(24)

