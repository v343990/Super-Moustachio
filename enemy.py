import pygame

class Enemy:
    enemy_surf = pygame.image.load('Images/enemymoustache.png')
    enemy_surf = pygame.transform.scale(enemy_surf, (85, 50))  # Resize the image
    enemy_rect = enemy_surf.get_rect(center=(900, 600))
    health = 50
    damage = 10
    gravity = 1  # Strength of gravity
    vertical_velocity = 1  # Vertical velocity of the character
    jump_strength = -22.5  # Initial velocity for a jump
    speed = 3

    # Colours
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
