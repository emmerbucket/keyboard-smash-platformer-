import pygame
import os

backgrounds = []
bg_files = ['orangetree.png', 'mountains2.png', 'snowyhouse.png', 'library.png', 'christmasbackground1.png', 'christmasbackground2.png', 'congrats.png']
block_images = ['jdirt.png', 'rocks.png', 'woodlog.png', 'tiles.png', 'better wood floor.png', 'better wood floor.png', 'better wood floor.png']
hazard_images = ['spike.png']
portal_images = ['portal.png']

for bg_file in bg_files:
    bg_image = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'images', bg_file))
    bg_image = pygame.transform.scale(bg_image, (800, 600))
    backgrounds.append(bg_image)

current_bg_index = 0
player = []

GAME_WIDTH = 800
GAME_HEIGHT = 600
dash_timer = 0
dash_lengte = 8 

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT ))
pygame.display.set_caption("Journey")
clock = pygame.time.Clock()

menu = "menu"
game = "game"

game_state = menu

font_big = pygame.font.SysFont("Comic Sans", 72)
font_small = pygame.font.SysFont("Comic Sans", 36)

def draw_menu():
    #change menu bg here
    window.fill((20, 100, 60))

    title = font_big.render("Journey", True, (255, 255, 255))
    start_text = font_small.render("Press ENTER to Start", True, (200, 200, 200))
    quit_text = font_small.render("Press ESC to Quit", True, (200, 200, 200))

    window.blit(title, (GAME_WIDTH // 2 - title.get_width() // 2, 180))
    window.blit(start_text, (GAME_WIDTH // 2 - start_text.get_width() // 2, 300))
    window.blit(quit_text, (GAME_WIDTH // 2 - quit_text.get_width() // 2, 350))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Animation setup
        self.animations = {"idle": [], "run": [], "jump": []}
        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 0.2

        # Load animations
        for state in self.animations.keys():
            folder = os.path.join("player", state)
            if os.path.exists(folder):
                for file in sorted(os.listdir(folder)):
                    if file.endswith(".png"):
                        path = os.path.join(folder, file)
                        image = pygame.image.load(path).convert_alpha()
                        self.animations[state].append(image)

        # Make sure we have at least one frame for each animation
        for state in self.animations:
            if len(self.animations[state]) == 0:
                # Create a placeholder if no frames
                surf = pygame.Surface((15, 15), pygame.SRCALPHA)
                surf.fill((255, 0, 255))
                self.animations[state].append(surf)

        # Set initial image and rect
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Physics
        self.change_x = 0
        self.change_y = 0
        self.on_ground = False

    def update(self, blocks):
        self.handle_movement()
        self.apply_gravity()
        self.horizontal_collisions(blocks)
        self.vertical_collisions(blocks)
        self.update_animation()

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        self.change_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.change_x = -5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.change_x = 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.change_y = -15
            self.on_ground = False

        self.rect.x += self.change_x

    def apply_gravity(self):
        if not self.on_ground:
            self.change_y += 1
            if self.change_y > 12:
                self.change_y = 12
        self.rect.y += self.change_y

    def horizontal_collisions(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    self.rect.left = block.rect.right

    def vertical_collisions(self, blocks):
        self.on_ground = False
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                    self.change_y = 0
                    self.on_ground = True
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                    self.change_y = 0

    def update_animation(self):
        # Determine state
        if not self.on_ground:
            self.state = "jump"
        elif self.change_x != 0:
            self.state = "run"
        else:
            self.state = "idle"

        # Update frame
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.state]):
            self.frame_index = 0
        self.image = self.animations[self.state][int(self.frame_index)]

    def update_animation(self):
        if not self.on_ground:
            self.state = "jump"
        elif self.change_x != 0:
            self.state = "run"
        else:
            self.state = "idle"

        self.frame += 0.2
        if self.frame >= len(self.animations[self.state]):
            self.frame = 0

        self.image = self.animations[self.state][int(self.frame)]
        
        def changespeed(self, x, y):
            self.change_x += x
            self.change_y += y
        
        def update(self):
            self.rect.x += self.change_x
            self.rect.y += self.change_y
        
player = Player(200, 200)
facing_left = False
facing_right = True
dash_available = True

class Block():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = pygame.Surface([self.width, self.height])
        floor_img = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'images', block_images[level_index]))
        self.image = pygame.transform.scale(floor_img, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

class Hazard():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = pygame.Surface([self.width, self.height])
        hazard_img = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'images', hazard_images[0]))
        self.image = pygame.transform.scale(hazard_img, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # code for the hitbox of a hazard
        pad_x = 6
        hit_w = self.width - pad_x * 2
        hit_h = int(self.height / 2)
        hit_x = self.x + pad_x
        hit_y = self.y + (self.height - hit_h)
        self.hitbox = pygame.Rect(hit_x, hit_y, hit_w, hit_h)

class Portal():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = pygame.Surface([self.width, self.height])
        portal_img = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'images', portal_images[0]))
        self.image = pygame.transform.scale(portal_img, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

level1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

level2 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,2,2,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,0,0,1,1,1,1,1,1,1,1,1,0,2,0,0,2,0,0,0,0],
    [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,1,2,0,1,0,0,0,0],
    [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1,0,0,0,0],
    [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,1,0,1,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0],
    [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,0,1,0,2,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,0,0,0,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0],
    [0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,3,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1,0,0,0,0,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

level3 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,2,2,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,1,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,0],
    [0,0,0,0,0,2,2,0,0,1,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,1,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,1,0,0,3,0,0,1,2,2,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,2,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,0,2,0,0,0,0,0,0,0],
    [0,2,0,0,0,0,0,0,0,1,0,2,0,0,0,0,0,1,1,1,0,2,2,2,0],
    [0,1,1,1,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,1,1,1,2,2,2,2,2,2,2],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

level4 = [
    [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [2,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,2,2,2,0],
    [1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0],
    [0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,3,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

level5 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,2,3,2,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [2,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,2,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,2,2],
    [0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0],
    [0,0,0,0,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,2,2,2],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

level6 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,2,0,0,0,2,2,2,2,0,0,0,2,0,2,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,0,1,1,1,1,0,1,1,1,1,1,0,2,0,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0],
    [0,0,0,2,0,2,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,2,0,0,2,0,1,0,0,0,0,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,2,0,2,0,2,2],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,1,1,0,1,1],
    [0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,2],
    [0,0,0,0,2,0,2,0,0,0,0,0,0,1,2,0,0,0,0,0,0,1,1,1,1],
    [0,0,0,1,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,3,0],
    [0,2,0,2,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1],
    [0,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,1,2,2,2,0,0,0,1,2,2,2,2,2,2,2,2,2,2,2],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

level7 = [
    [0,0,0,0,1,1,1,1,1,0,0,1,1,1,0,0,1,0,0,0,1,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,1,1,0,0,1,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,1,0,0,1,1,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,0,0,1,1,1,0,0,1,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0],
    [0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,0,0,1,1,1,0],
    [0,1,0,1,0,0,1,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,1,0],
    [0,1,1,1,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,0,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

levels = [level1, level2, level3, level4, level5, level6, level7]
level_index = 0

def load_level(new_level_index):
    global blocklist, hazardlist, portallist,  current_level_index, current_bg_index, level_index
    level_index = new_level_index
    current_level_index = new_level_index
    current_bg_index = new_level_index

    blocklist = []
    hazardlist = []
    portallist = []
    level = levels[level_index]
    block_img = block_images[level_index]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 1:
                blocklist.append(Block(x * 32, y * 32))
            elif level[y][x] == 2:
                hazardlist.append(Hazard(x * 32, y * 32,))
            elif level[y][x] == 3:
                portallist.append(Portal(x * 32, y * 32))

    player.rect.x = 50
    player.rect.y = 550
    player.change_y = 0

def draw():
    window.blit(backgrounds[current_bg_index], (0, 0))
    for block in blocklist:
        window.blit(block.image, block.rect)
    for hazard in hazardlist:
        window.blit(hazard.image, hazard.rect)
    for portal in portallist:
        window.blit(portal.image, portal.rect)
    window.blit(player.image, player.rect)

vel = 1
jumpCount = 0
jumpMax = 15

blocklist = []
hazardlist = []
load_level(level_index)

level_index = 0

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
        
        if game_state == menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    load_level(0)        
                    game_state = game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        elif game_state == game:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.on_ground:
                    player.change_y = -15
                    player.on_ground = False
  
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                      if any(player.rect.colliderect(portal.rect) for portal in portallist):
                        level_index = (level_index + 1) % len(levels)
                        load_level(level_index)

    keys = pygame.key.get_pressed() 
    player.change_x = 0

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.change_x = -5
        facing_left = True
        facing_right = False

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.change_x = 5
        facing_left = False
        facing_right = True

    if keys[pygame.K_LSHIFT] and dash_timer == 0 and dash_available and not player.on_ground:
        dash_timer = dash_lengte
        player.change_y = 0
        dash_available = False

    player.on_ground = False

    if dash_timer > 0:
        if facing_left:
            player.change_x = -20
        elif facing_right:
            player.change_x = 20
        dash_timer -= 1

    # houdt player horizontaal in window
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > GAME_WIDTH:
        player.rect.right = GAME_WIDTH

    # window vertical borders (expres geen top border)
    if player.rect.bottom > GAME_HEIGHT:
        player.rect.bottom = GAME_HEIGHT
        player.change_y = 0
        player.on_ground = True
        dash_available = True


    # DASH start
    if keys[pygame.K_LSHIFT] and dash_timer == 0 and dash_available and not player.on_ground:
        dash_timer = dash_lengte
        player.change_y = 0
        dash_available = False

    # DASH handling (overrides horizontal speed while active)
    if dash_timer > 0:
        if facing_left:
            player.change_x = -20
        elif facing_right:
            player.change_x = 20
        dash_timer -= 1
    else:
        # apply gravity only when not dashing
        if not player.on_ground:
            player.change_y += 1
            if player.change_y > 12:
                player.change_y = 12

    # horizontal collisions
    player.rect.x += player.change_x

    for block in blocklist:
        if player.rect.colliderect(block.rect):
            if player.change_x > 0:
                player.rect.right = block.rect.left
            elif player.change_x < 0:
                player.rect.left = block.rect.right
            player.change_x = 0

    # vertical collisions
    player.rect.y += player.change_y

    
    for block in blocklist:
        if player.rect.colliderect(block.rect):
            if player.change_y > 0:
                player.change_y = 0
                player.rect.bottom = block.rect.top
                player.on_ground = True
                dash_available = True
                break
            elif player.change_y < 0:
                player.rect.top = block.rect.bottom
                player.change_y = 0
                break
            player.change_y = 0
            break

        
        for hazard in hazardlist:
            if player.rect.colliderect(hazard.hitbox):
                    player.rect.x = 50
                    player.rect.y = 550
                    player.change_y = 0
                    break

    if game_state == menu:
        draw_menu()
    elif game_state == game:
        draw()

    pygame.display.update()
    clock.tick(24)