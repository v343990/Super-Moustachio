import pygame
import pygame.locals
from player import Player
from pygame.locals import *


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
            if self.player_rect.colliderect(platform) and self.vertical_velocity >= 0: # If the player collides with a platform and is falling
                self.player_rect.bottom = platform.top  # Move the player to the top of the platform
                self.vertical_velocity = 0 # Stop the player from falling
                self.on_platform = True # Boolean which allows the player to stop falling through platform
        if self.player_rect.bottom >= self.ground_level and not self.on_platform:
            self.player_rect.bottom = self.ground_level # Stop the player from falling through the ground
            self.vertical_velocity = 0
        self.player_rect.x = max(0, min(self.player_rect.x, self.width - self.player_rect.width)) # Keep the player in bounds


    # Drawing everything
    def draw(self):
        self.screen.fill((255, 255, 255)) # Fill white background
       
        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 0, 0), platform) # Draw the platforms in platforms array
       
        self.screen.blit(self.player_surf, self.player_rect) # Draw the player


        pygame.display.flip()


    # Main game loop
    def run_game(self):
        while self.run:
            self.handle_events() # Handle events
            self.update_player() # Update player position
            self.draw()  # Draw everything
            self.fpsClock.tick(self.fps) # Cap the frame rate / physics updates


# Run the game
if __name__ == "__main__":
    game = Game()
    game.run_game()
