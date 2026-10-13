import pygame
import random
import math
import asyncio

# Things we should do:

# Not started:
# Generate maze
# Enemy class
# Enemy states: patrol, chase, attack, & death
# Enemy-player detection
# Player class/variables
# Player upgrades: sprinting, sliding, faster movement speed, shooting, larger collecting radius
# MacGuffin class
# Abiliy to collect MacGuffins
# Keep track of score, lives, & stamina
# Start, win & game over screen
# Make custom sprites if we want
# Share character assets w/ each other
# Make comments on everything [I don't actually remember if this is a requirement.]
# Make asyncio version to upload to web !!!!!!!!

# In progress:
# Projectile class
# Code player inputs

# Finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# Sprite configuration
projectile_image = pygame.image.load("PLACEHOLDER.png").convert_alpha()
projectile_image = pygame.transform.scale(projectile_image, (70, 70))


pygame.init()
WIDTH = 800
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Projectile class; add sweet and kind sprite
class Projectile:
    def __init__(self, position, r, color, direct, evil):
        self.position = position
        self.r = r
        self.color = color
        self.direct = direct
        self.evil = evil

    def draw(self):
        screen.blit(projectile_image, self.position)

# Player variables/later class if needed

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Register key inputs
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            """whatever"""
           
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            """whatever"""

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            """whatever"""
       
        if keys[pygame.K_SPACE]:
            """whatever"""

    pygame.display.flip()
    clock.tick(60)
pygame.quit()