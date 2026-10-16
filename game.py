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

    plr = mapHandler.mapObject("player", pygame.image.load("fauna.png").convert_alpha(), {"spawnVec": pygame.Vector2(width/2, length/2), "sizeX": 50, "sizeY": 50, "center": pygame.Vector2((width+100)/2, (length+100)/2)})

    slideVec = pygame.Vector2(0, 0)
    tickHi = -1
    running = True
    while running:
        for i in enemyList: i.tickForward()
        tickHi += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    dragging = True
                    for key, val in mapHandler.objects.items():
                        if (val.rect.collidepoint(pygame.mouse.get_pos()) and val.dragable):
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
        if ((keys[pygame.K_UP] or keys[pygame.K_w]) and slideVec.y >= -5): slideVec = slideVec + pygame.Vector2(0, -2)
        if ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and slideVec.x >= -5): slideVec = slideVec + pygame.Vector2(-2, 0)
        if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and slideVec.x <= 5): slideVec = slideVec + pygame.Vector2(2, 0)
        if ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and slideVec.y <= 5): slideVec = slideVec + pygame.Vector2(0, 2)


        limiter = 0.25
        if slideVec.x > 0: slideVec = slideVec + pygame.Vector2(-limiter, 0)
        if slideVec.x < 0: slideVec = slideVec + pygame.Vector2(limiter, 0)
        if slideVec.y > 0: slideVec = slideVec + pygame.Vector2(0, -limiter)
        if slideVec.y < 0: slideVec = slideVec + pygame.Vector2(0, limiter)

        mapHandler.objects.get("player").rect.x += slideVec.x
        mapHandler.objects.get("player").rect.y += slideVec.y

                
        for i in enemyList: i.move()
        mapHandler.loadScreen(screen)
        pygame.display.flip()
        clock.tick(60)
    await asyncio.sleep(0)
asyncio.run(main())