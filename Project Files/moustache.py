import sys
import pygame
from pygame.locals import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
width, height = 1280, 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Moustache Display')

# Load image

player_surf = pygame.image.load('png-clipart-moustache-moustache-thumbnail.png').convert_alpha()


player_rect = player_surf.get_rect(center=(640, 400))

# Colours
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

gravity = 0.5  # Strength of gravity
vertical_velocity = 0  # Vertical velocity of the character
jump_strength = -10  # Initial velocity for a jump
speed = 10
ground_level = height  # Ground level

# Game Loop
run = True
while run:

    screen.fill((0,0,0))


    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            sys.exit()
    
    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] or keys[K_a]:
        player_rect.x -= speed
    if keys[K_RIGHT] or keys[K_d]:
        player_rect.x += speed

    # Jumping
    if keys[K_SPACE] and player_rect.bottom >= ground_level:
        vertical_velocity = jump_strength

    # Apply gravity
    vertical_velocity += gravity
    player_rect.y += vertical_velocity

    # Prevent falling below ground level
    if player_rect.bottom >= ground_level:
        player_rect.bottom = ground_level
        vertical_velocity = 0

    # Keeps player inside bounds
    player_rect.x = max(0, min(player_rect.x, width - player_rect.width))

    screen.blit(player_surf, player_rect)
    
    # Update display
    pygame.display.flip()
    fpsClock.tick(fps)
