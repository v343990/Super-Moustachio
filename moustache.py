import pygame
import pygame.locals
from player import Player
from pygame.locals import *
from enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.width, self.height = 1280, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Moustache Display')

        # Player setup (imported from player.py)
        self.player = Player()
        self.player_surf = self.player.player_surf
        self.player_rect = self.player.player_rect
        self.speed = self.player.speed
        self.gravity = self.player.gravity
        self.vertical_velocity = self.player.vertical_velocity
        self.jump_strength = self.player.jump_strength
        self.ground_level = self.height
        self.player_health = self.player.health

        # Enemy setup (imported from enemy.py)
        self.enemy = Enemy()
        self.enemy_surf = self.enemy.enemy_surf
        self.enemy_rect = self.enemy.enemy_rect
        self.enemy_speed = self.enemy.speed
        self.enemy_health = self.enemy.health
        self.enemy_vertical_velocity = self.enemy.vertical_velocity
        self.enemy_jump_strength = self.enemy.jump_strength
        self.enemy_gravity = self.enemy.gravity
        self.enemy_ground_level = self.height

        # UI Setup
        self.text_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
        self.healthDisp = self.text_font.render(f"Player Health: {self.player_health}", True, (20, 20, 20))
        
        # Bullets setup
        self.bullets = []
        self.bullet_speed = 10
        self.bullet_width, self.bullet_height = 10, 5

        # Health Pickup setup
        self.healthPickup = [pygame.Rect(250, 775, 25, 25)]
        
        # Platform setup
        self.platforms = [
            pygame.Rect(200, 600, 200, 10),
            pygame.Rect(500, 500, 200, 10),
            pygame.Rect(800, 400, 200, 10)
        ]
        self.run = True

    # Event handling
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x = event.pos[0]
                    direction = 'left' if mouse_x < self.player_rect.centerx else 'right'
                    bullet_rect = pygame.Rect(self.player_rect.centerx, self.player_rect.centery, self.bullet_width, self.bullet_height)
                    self.bullets.append((bullet_rect, direction, (0, 0, 0)))  # Black bullets for mouse click
            elif event.type == pygame.KEYDOWN:
                if event.key == K_s:  # 's' key
                    bullet_rect = pygame.Rect(self.player_rect.centerx, self.player_rect.bottom, self.bullet_height, self.bullet_width)
                    self.bullets.append((bullet_rect, 'down', (139, 69, 19)))  # Brown bullets for 's' key
                    self.vertical_velocity = self.jump_strength + 5

    # Player movement
    def update_player(self):
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.player_rect.x -= self.speed  # Move left
        if keys[K_d]:
            self.player_rect.x += self.speed  # Move right
        if keys[K_SPACE] and (self.player_rect.bottom >= self.ground_level or self.on_platform):
            self.vertical_velocity = self.jump_strength  # Jump

        # Gravity checks
        self.vertical_velocity += self.gravity  # Apply gravity
        self.player_rect.y += self.vertical_velocity
        self.on_platform = False

        # Collision checks with platforms
        for platform in self.platforms:
            if self.player_rect.colliderect(platform) and self.vertical_velocity >= 0:
                self.player_rect.bottom = platform.top  # Move the player to the top of the platform
                self.vertical_velocity = 0  # Stop the player from falling
                self.on_platform = True  # Boolean which allows the player to stop falling through platform
        if self.player_rect.bottom >= self.ground_level and not self.on_platform:
            self.player_rect.bottom = self.ground_level  # Stop the player from falling through the