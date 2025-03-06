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
        
        # Screen and level dimensions
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 800
        self.LEVEL_WIDTH, self.LEVEL_HEIGHT = 2560, 1600  # Larger level size
        
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Moustache Display')

        # Camera system
        class Camera:
            def __init__(self, width, height):
                self.camera = pygame.Rect(0, 0, width, height)
                self.width = width
                self.height = height

            def apply(self, entity):
                return entity.move(self.camera.topleft)

            def update(self, target):
                x = -target.x + self.width // 2
                y = -target.y + self.height // 2

                # Limit scrolling to level edges
                x = min(0, x)  # Left
                y = min(0, y)  # Top
                x = max(-(self.LEVEL_WIDTH - self.SCREEN_WIDTH), x)  # Right
                y = max(-(self.LEVEL_HEIGHT - self.SCREEN_HEIGHT), y)  # Bottom
                
                self.camera = pygame.Rect(x, y, self.LEVEL_WIDTH, self.LEVEL_HEIGHT)

        self.camera = Camera(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Player setup (using level coordinates)
        self.player = Player()
        self.player_surf = self.player.player_surf
        self.player_rect = self.player.player_rect
        self.player_rect.center = (self.LEVEL_WIDTH//2, self.LEVEL_HEIGHT//2)  # Start at level center
        self.speed = self.player.speed
        self.gravity = self.player.gravity
        self.vertical_velocity = self.player.vertical_velocity
        self.jump_strength = self.player.jump_strength
        self.ground_level = self.LEVEL_HEIGHT  # Use level height for ground
        self.player_health = self.player.health

        # Enemy setup (using level coordinates)
        self.enemy_defeated = False
        self.enemy = Enemy()
        self.enemy_surf = self.enemy.enemy_surf
        self.enemy_rect = self.enemy.enemy_rect
        self.enemy_rect.topleft = (self.LEVEL_WIDTH - 200, self.LEVEL_HEIGHT - 100)
        self.enemy_speed = self.enemy.speed
        self.enemy_health = self.enemy.health
        self.enemy_vertical_velocity = self.enemy.vertical_velocity
        self.enemy_jump_strength = self.enemy.jump_strength
        self.enemy_gravity = self.enemy.gravity
        self.enemy_ground_level = self.LEVEL_HEIGHT
        self.enemy_jump_delay = 1000
        self.enemy_last_jump_time = 0
        self.enemy_damage_delay = 1000
        self.enemy_last_damage_time = 0

        # UI Setup
        self.text_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
        
        # Bullets setup
        self.bullets = []
        self.bullet_speed = 10
        self.bullet_width, self.bullet_height = 10, 5

        # Health Pickup setup (level coordinates)
        self.healthPickup = [
            pygame.Rect(250, self.LEVEL_HEIGHT - 25, 25, 25)
        ]
        
        # Platform setup (level coordinates)
        self.platforms = [
            pygame.Rect(200, 600, 200, 10),
            pygame.Rect(500, 500, 200, 10),
            pygame.Rect(800, 400, 200, 10),
            pygame.Rect(1500, 600, 200, 10),
            pygame.Rect(1800, 500, 200, 10),
            pygame.Rect(2100, 400, 200, 10)
        ]
        self.run = True


    # Modified draw method with camera offsets
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.healthDisp = self.text_font.render(f"+{self.player_health}", True, (20,20,20))
        
        # Apply camera offset to UI elements
        screen_health_pos = self.healthDisp.get_rect(topleft=(10, 10))
        self.screen.blit(self.healthDisp, screen_health_pos)
        
        # Draw Platforms with camera offset
        for platform in self.platforms:
            adjusted_platform = platform.move(self.camera.camera.topleft)
            pygame.draw.rect(self.screen, (0, 0, 0), adjusted_platform)
        
        # Draw Bullets with camera offset
        for bullet, direction, color in self.bullets:
            adjusted_bullet = bullet.move(self.camera.camera.topleft)
            pygame.draw.rect(self.screen, color, adjusted_bullet)
        
        # Draw Health Pickups with camera offset
        for health in self.healthPickup:
            adjusted_health = health.move(self.camera.camera.topleft)
            pygame.draw.rect(self.screen, (240, 0, 0), adjusted_health)
        
        # Draw Player with camera offset
        adjusted_player = self.player_rect.move(self.camera.camera.topleft)
        self.screen.blit(self.player_surf, adjusted_player)
        
        # Flash effect
        if self.is_Flashing and (pygame.time.get_ticks() - self.flash_start_time < self.flash_duration):
            self.screen.blit(self.flash_surface, adjusted_player)

        # Draw Enemy with camera offset
        if not self.enemy_defeated:
            adjusted_enemy = self.enemy_rect.move(self.camera.camera.topleft)
            self.screen.blit(self.enemy_surf, adjusted_enemy)

        pygame.display.flip()

    # Modified update_player method with level boundaries
    def update_player(self):
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.player_rect.x -= self.speed
        if keys[K_d]:
            self.player_rect.x += self.speed
            
        # Keep player within level bounds
        self.player_rect.x = max(0, min(self.player_rect.x, self.LEVEL_WIDTH - self.player_rect.width))
        

    # Modified run_game method with camera updates
    def run_game(self):
        while self.run:
            time = pygame.time.get_ticks()
            self.handle_events()
            self.update_player()
            self.update_enemy(time)
            self.update_bullets()
            self.health_pickup()
            self.camera.update(self.player_rect)  # Update camera position
            self.draw()
            self.fpsClock.tick(self.fps)
