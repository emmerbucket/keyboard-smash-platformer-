import pygame
import os

backgrounds = []
bg_files = ['christmasbackground1.png', 'christmasbackground2.png', 'library.png', 'mountains.png', 'orangetree.png']

for bg_file in bg_files:
    bg_image = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'images', bg_file))
    bg_image = pygame.transform.scale(bg_image, (800, 600))
    backgrounds.append(bg_image)

current_bg_index = 4
walls = []
player = []
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
     def __init__(self, y=GAME_HEIGHT - 75, width=GAME_WIDTH, height=75):
        super().__init__()

        floor_img = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'images', 'Tileable pixel art wood.png'))
        self.image = pygame.transform.scale(floor_img, (width, height))

        self.rect = self.image.get_rect(topleft=(0, y))

        self.change_x = 0
        self.change_y = 0

player = Player(200, 200)
floor = Floor()

def draw():
    window.blit(backgrounds[current_bg_index], (0, 0))
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

