import pygame
import os

pygame.init()

bg = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'images', 'mountains.png'))
screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("use arrows")

movex = 0

class player:

    def __init__(self ,x, y):
        self.x = x
        self.y = y
        self.image = pygame.Surface([112,112])
        self.width = 112
        self.height = 112
        self.velocity = 0
        self.falling = False
        self.onGround = False

    def jump(self):
        if(self.onGround == False):
            return

        self.velocity = 8
        self.onGround = False

    def detectCollisions(self,x1,y1,w1,h1,x2,y2,w2,h2):
        if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2):
            return True
        elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2):
            return True
        elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2):
            return True
        elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2):
            return True    
        else:
            return False

    def update(self, gravity, blockList):
        if (self.velocity < 0):
            self.falling = True

        collision = False
        blockX,blockY =  0,0
        for block in blockList:

            collision = self.detectCollisions(self.x, self.y, self.width, self.height, block.x, block.y, block.width, block.height )
            if collision == True:
                blockx = block.x
                blocky = block.y
                break

        if(collision == True):
            if self.falling == True:
                self.falling = False
                self.onGround = True
                self.velocity = 0
                self.y = blocky - self.height

        if (self.onGround == False):
            self.velocity += gravity
        self.y -= self.velocity

    def render(self,screen):
        screen.blit(self.image,(self.x,self.y))

class Block:
    def __init__ (self, x, y):
       self.x = x
       self.y = y
       self.width = 32
       self.height = 32

    def render(self,screen):
        pygame.draw.rect(screen,(9,203,27),(self.x, self.y, self.width, self.height))

gravity = -0.5

black = (0,0,0)
white = (255,255,255)
blue = (50,60,200)

clock = pygame.time.Clock()

player = player(0,0)

# 25 colums and 19 rows
level1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

blockList = []

for y in range (0,len(level1)):
    for x in range (0,len(level1[y])):
        if (level1[y][x] == 1):
            blockList.append(Block(x*32, y*32))

gameloop = True

while gameloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False

        if(event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_RIGHT):
                movex = 5
            elif(event.key == pygame.K_LEFT):
                movex = -5
            elif (event.key == pygame.K_UP):
                player.jump()

        if(event.type == pygame.KEYUP):
            if (event.key == pygame.K_RIGHT):
                movex = 0
            elif(event.key == pygame.K_LEFT):
                movex = 0

    screen.fill(white)
    screen.blit(bg,(0,0))

    for block in blockList:
        block.render(screen)
    player.x += movex

    player.update(gravity, blockList)
    player.render(screen)
    clock.tick(60)

    pygame.display.update()

pygame.quit()