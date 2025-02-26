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
        self.healthDisp = self.text_font.render(f"+{self.player_health}",True,(20,20,20))
        
        # Bullets setup
        self.bullets = []
        self.bullet_speed = 10
        self.bullet_width, self.bullet_height = 10, 5

        # Health Pickup setup
        self.healthPickup = [
            pygame.Rect(250, 775, 25, 25)
        ]
        
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
                    if mouse_x < self.player_rect.centerx:
                        direction = 'left'
                    else:
                        direction = 'right'
                    bullet_rect = pygame.Rect(self.player_rect.centerx, self.player_rect.centery, self.bullet_width, self.bullet_height)
                    self.bullets.append((bullet_rect, direction, (0, 0, 0)))  # Black bullets for mouse click
            elif event.type == pygame.KEYDOWN:
                if event.key == K_s:  # 's' key
                    bullet_rect = pygame.Rect(self.player_rect.centerx, self.player_rect.bottom, self.bullet_height, self.bullet_width)
                    self.bullets.append((bullet_rect, 'down', (139, 69, 19)))  # Brown bullets for 's' key
                    self.vertical_velocity = self.jump_strength + 5

    # Player movement
    def update_player(self):

        # Key handling
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.player_rect.x -= self.speed # Move left
        if keys[K_d]:
            self.player_rect.x += self.speed # Move right
        if keys[K_SPACE] and (self.player_rect.bottom >= self.ground_level or self.on_platform):
            self.vertical_velocity = self.jump_strength # Jump ahoy!

        # Gravity checks
        self.vertical_velocity += self.gravity # Apply gravity
        self.player_rect.y += self.vertical_velocity
        self.on_platform = False

        # Collision checks with platforms
        for platform in self.platforms:
            if self.player_rect.colliderect(platform) and self.vertical_velocity >= 0:
                self.player_rect.bottom = platform.top  # Move the player to the top of the platform
                self.vertical_velocity = 0 # Stop the player from falling
                self.on_platform = True # Boolean which allows the player to stop falling through platform
        if self.player_rect.bottom >= self.ground_level and not self.on_platform:
            self.player_rect.bottom = self.ground_level # Stop the player from falling through the ground
            self.vertical_velocity = 0
        self.player_rect.x = max(0, min(self.player_rect.x, self.width - self.player_rect.width))

        # Collision checks with health pickups
        for health in self.healthPickup[:]: # Copy the list to avoid modifying it while iterating
            if self.player_rect.colliderect(health): # If the player collides with a health pickup
                self.healthPickup.remove(health) # Remove the health pickup
                self.player_health += 10 # Increase player health by 10
                self.healthDisp = self.text_font.render(f"+{self.player_health}",True,(20,20,20))


    def update_enemy(self):

    # Gravity checks
        self.enemy_vertical_velocity += self.enemy_gravity  # Apply gravity
        self.enemy_rect.y += self.enemy_vertical_velocity
        self.enemy_on_platform = False

    # Collision checks with platforms
        for platform in self.platforms:
            if self.enemy_rect.colliderect(platform) and self.enemy_vertical_velocity >= 0:
                self.enemy_rect.bottom = platform.top  # Move the enemy to the top of the platform
                self.enemy_vertical_velocity = 0  # Stop the enemy from falling
                self.enemy_on_platform = True  # Boolean which allows the enemy to stop falling through platform

            if self.enemy_rect.bottom >= self.enemy_ground_level and not self.enemy_on_platform:
                self.enemy_rect.bottom = self.enemy_ground_level  # Stop the enemy from falling through the ground
                self.enemy_vertical_velocity = 0



    # Bullet handling
    def update_bullets(self):
        for bullet, direction, color in self.bullets[:]: # Copy the list to avoid modifying it while iterating
            pygame.draw.rect(self.screen, color, bullet) # Draw the bullet
            
            if direction == 'right':
                bullet.x += self.bullet_speed # Move the bullet to the right
                if bullet.x > self.width:
                    self.bullets.remove((bullet, direction, color))
            
            elif direction == 'left':
                bullet.x -= self.bullet_speed # Move the bullet to the left
                if bullet.x < 0:
                    self.bullets.remove((bullet, direction, color)) # Remove the bullet if it goes off-screen
            
            elif direction == 'down':
                bullet.y += self.bullet_speed  # Move the bullet downwards
                
                if bullet.y > self.height:
                    self.bullets.remove((bullet, direction, color)) # Remove the bullet if it goes off-screen
                else:
                    for platform in self.platforms:
                        if bullet.colliderect(platform):
                            bullet.y = platform.top - self.bullet_height # Place the bullet on top of the platform
                            break
            
            pygame.draw.rect(self.screen, color, bullet) # Draw the bullet again

    # Drawing everything
    def draw(self):
        self.screen.fill((255, 255, 255)) # Fill white background
        self.screen.blit(self.healthDisp,(10,10)) # Display health
        
        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 0, 0), platform) # Draw the platforms in platforms array
        
        for bullet, direction, color in self.bullets:
            pygame.draw.rect(self.screen, color, bullet) # Draw the bullets in bullet array
        
        for health in self.healthPickup:
            pygame.draw.rect(self.screen, (240, 0, 0), health) # Draw the health pickups in the array
        
        self.screen.blit(self.player_surf, self.player_rect) # Draw the player
        self.screen.blit(self.enemy_surf, self.enemy_rect) # Draw the enemy

        pygame.display.flip()

    # Main game loop
    def run_game(self):
        while self.run:
            self.handle_events() # Handle events
            self.update_player() # Update player position
            self.update_enemy() # Update enemy position
            self.update_bullets() # Update bullets
            self.draw()  # Draw everything
            self.fpsClock.tick(self.fps) # Cap the frame rate / physics updates

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run_game()