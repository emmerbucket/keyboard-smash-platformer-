import pygame

GAME_WIDTH = 800
GAME_HEIGHT = 600

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT ))
pygame.display.set_caption("Keyboard Smash")
clock = pygame.time.Clock()

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(24)

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
