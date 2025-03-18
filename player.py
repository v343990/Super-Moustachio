import pygame

class Player:
    player_surf = pygame.image.load('Images/playermoustache.png')
    player_surf = pygame.transform.scale(player_surf, (85, 50))  # Resize the image
    player_rect = player_surf.get_rect(center=(640, 400))
    health = 100
    gravity = 1  # Strength of gravity
    vertical_velocity = 1  # Vertical velocity of the character
    jump_strength = -22.5  # Initial velocity for a jump
    speed = 10

