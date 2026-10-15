import pygame
import sys
import asyncio
import random
import mapHandler
import pathfinder

async def main():
    pygame.init()

    clock = pygame.time.Clock()

    width = 1280
    length = 600
    screen = pygame.display.set_mode((width, length))
    pygame.display.set_caption("Pac-Rien")

    enemyList = []
    dragging = False
    moving = pygame.Vector2(0,0)
    shift = pygame.Vector2(0,0)


    tickHi = -1
    playerGrav = 0
    grounded = False
    running = True
    while running:
        for i in enemyList:
            i.tickForward()
        tickHi += 1
        if (tickHi % 4 == 0):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        dragging = True
                        for key, val in mapHandler.objects.items():
                            if (val.rect.collidepoint(pygame.mouse.get_pos())):
                                moving = val.rect
                                break
                        vec2 = pygame.Vector2(pygame.mouse.get_pos())
                        shift = pygame.Vector2(val.rect.x - vec2.x, val.rect.y - vec2.y)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        dragging = False
                        shift, moving = pygame.Vector2(0,0), pygame.Vector2(0,0)
                if event.type == pygame.MOUSEMOTION:
                    if (dragging == True):
                        vec2 = pygame.Vector2(pygame.mouse.get_pos())
                        moving.x = vec2.x + shift.x
                        moving.y = vec2.y + shift.y


            keys = pygame.key.get_pressed()
                
            mapHandler.loadScreen(screen)
            for i in enemyList: 
                i.move()
                screen.blit(i.image, i.position)
            pygame.display.flip()
            clock.tick(240)
        await asyncio.sleep(0)
asyncio.run(main())
