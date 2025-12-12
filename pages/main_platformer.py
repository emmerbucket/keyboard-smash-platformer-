import pygame
import os

backgrounds = []
bg_files = ['orangetree.png', 'mountains.png', 'snowyhouse.png', 'library.png', 'christmasbackground1.png', 'christmasbackground2.png']

for bg_file in bg_files:
    bg_image = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'images', bg_file))
    bg_image = pygame.transform.scale(bg_image, (800, 600))
    backgrounds.append(bg_image)

current_bg_index = 0
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
            self.on_ground = False
        
        def changespeed(self, x, y):
            self.change_x += x
            self.change_y += y
        
        def update(self):
            self.rect.x += self.change_x
            self.rect.y += self.change_y

player = Player(200, 200)

class Floor():
     def __init__(self, y=GAME_HEIGHT - 75, width=GAME_WIDTH, height=75):
        super().__init__()

        floor_img = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'images', 'Tileable pixel art wood.png'))
        self.image = pygame.transform.scale(floor_img, (width, height))

        self.rect = self.image.get_rect(topleft=(0, y))

        self.change_x = 0
        self.change_y = 0

floor = None

class Block():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = pygame.Surface([self.width, self.height])
        floor_img = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'images', 'jdirt.png'))
        self.image = pygame.transform.scale(floor_img, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

level1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

blocklist = []
for y in range(len(level1)):
    for x in range(len(level1[y])):
        if level1[y][x] == 1:
            blocklist.append(Block(x * 32, y * 32))

def draw():
    window.blit(backgrounds[current_bg_index], (0, 0))
    for block in blocklist:
        window.blit(block.image, block.rect)
    window.blit(player.image, player.rect)
    if floor:
        window.blit(floor.image, floor.rect)

vel = 1
jumpCount = 0
jumpMax = 15


while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_SPACE and player.on_ground:
            player.change_y = -15
            player.on_ground = False

    keys = pygame.key.get_pressed()

    player.change_x = 0

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.change_x = 1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.change_x = -1
    
    player.change_y += 1 
    if player.change_y > 12:
        player.change_y = 12

    player.rect.x += player.change_x
    player.rect.y += player.change_y
    
    player.on_ground = False

    if floor and player.rect.colliderect(floor.rect):
        if player.change_y > 0:
            player.rect.bottom = floor.rect.top
            player.change_y = 0
            player.on_ground = True
        elif player.change_y < 0:
            player.rect.top = floor.rect.bottom
            player.change_y = 0

    # horizontal collision
    for block in blocklist:
        if player.rect.colliderect(block.rect):
            if player.change_x > 0:
                player.rect.right = block.rect.left
                break
            elif player.change_x < 0:
                player.rect.left = block.rect.right
                break

    # vertical collision
    for block in blocklist:
        if player.rect.colliderect(block.rect):
            if player.change_y > 0:
                player.rect.bottom = block.rect.top
                player.change_y = 0
                player.on_ground = True
                break
            elif player.change_y < 0:
                player.rect.top = block.rect.bottom
                player.change_y = 0
                break

    draw()

    pygame.display.update()
    clock.tick(24)