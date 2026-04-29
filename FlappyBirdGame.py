import pygame
from pygame.locals import *
import random

# Initiates PyGame module
pygame.init()

#text
# Set screen dimensions
screen_width = 800
screen_height = 900

# Creates the game screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')


# Main game Loop
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    pygame.display.update()

# Quits PyGame
pygame.quit()
