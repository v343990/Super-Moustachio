import pygame

class Player:
    player_surf = pygame.image.load('png-clipart-moustache-moustache-thumbnail.png')
    player_surf = pygame.transform.scale(player_surf, (85, 50))  # Resize the image
    player_rect = player_surf.get_rect(center=(640, 400))

    gravity = 1.1  # Strength of gravity
    vertical_velocity = 1  # Vertical velocity of the character
    jump_strength = -20  # Initial velocity for a jump
    speed = 10

    # Colours
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
