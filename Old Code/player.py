import pygame

class Player:
    def __init__(self):
        self.player_surf = pygame.image.load('Images/playermoustache.png')
        self.player_surf = pygame.transform.scale(self.player_surf, (85, 50))  # Resize the image
        self.player_rect = self.player_surf.get_rect(center=(640, 400))
        self.health = 100 # Health of the player
        self.gravity = 1  # Strength of gravity
        self.vertical_velocity = 1  # Vertical velocity of the character
        self.jump_strength = -22.5  # Initial velocity for a jump
        self.speed = 10  # Speed of the character