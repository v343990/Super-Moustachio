import pygame

class Enemy:
    def __init__(self):
        self.enemy_surf = pygame.image.load('Images/enemymoustache.png')
        self.enemy_surf = pygame.transform.scale(self.enemy_surf, (85, 50))  # Resize the image
        self.enemy_rect = self.enemy_surf.get_rect(center=(900, 600))
        self.health = 50 # Health of the enemy
        self.damage = 10 # Damage of the enemy
        self.gravity = 1  # Strength of gravity
        self.vertical_velocity = 1  # Vertical velocity of the character
        self.jump_strength = -22.5  # Initial velocity for a jump
        self.speed = 5 # Speed of the character

    # Colours
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
