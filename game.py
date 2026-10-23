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

    dragging = False
    moving = pygame.Vector2(0,0)
    shift = pygame.Vector2(0,0)


    mapHandler.genMap()
    plr = mapHandler.mapObject("player", pygame.image.load("fauna.png").convert_alpha(), {"spawnVec": pygame.Vector2(width/2, length/2), "sizeX": 50, "sizeY": 50})
    

    pathfinder.drone.setupBlacklist()

    newDrone = pathfinder.drone()
    slideVec = pygame.Vector2(0, 0)
    tickHi = 0
    running = True
    while running:
        newDrone.tickFind()
        if (tickHi % 4 == 0):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.button == 1):
                        dragging = True
                        for val in mapHandler.objects:
                            if (val.rect.collidepoint(pygame.mouse.get_pos()) and val.dragable):
                                moving = val.rect
                                break
                        vec2 = pygame.Vector2(pygame.mouse.get_pos())
                        shift = pygame.Vector2(val.rect.x - vec2.x, val.rect.y - vec2.y)
                    elif (event.button == 3): 
                        x, y = event.pos
                        print(x, " ", y)
                        pathfinder.drone.updateBlacklistZone()
                        newDrone.buildNewPath(pygame.Vector2(x, y))
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        dragging = False
                        shift, moving = pygame.Vector2(0,0), pygame.Vector2(0,0)
                if event.type == pygame.MOUSEMOTION:
                    if (dragging == True):
                        vec2 = pygame.Vector2(pygame.mouse.get_pos())
                        moving.x = vec2.x + shift.x
                        moving.y = vec2.y + shift.y

            maxSpeed = 2
            keys = pygame.key.get_pressed()
            if ((keys[pygame.K_UP] or keys[pygame.K_w]) and slideVec.y >= -maxSpeed): slideVec = slideVec + pygame.Vector2(0, -2)
            if ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and slideVec.x >= -maxSpeed): slideVec = slideVec + pygame.Vector2(-2, 0)
            if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and slideVec.x <= maxSpeed): slideVec = slideVec + pygame.Vector2(2, 0)
            if ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and slideVec.y <= maxSpeed): slideVec = slideVec + pygame.Vector2(0, 2)

            limiter = 0.25
            if slideVec.x > 0: slideVec = slideVec + pygame.Vector2(-limiter, 0)
            if slideVec.x < 0: slideVec = slideVec + pygame.Vector2(limiter, 0)
            if slideVec.y > 0: slideVec = slideVec + pygame.Vector2(0, -limiter)
            if slideVec.y < 0: slideVec = slideVec + pygame.Vector2(0, limiter)

            plr.rect.x += slideVec.x
            plr.rect.y += slideVec.y

            
            newDrone.tickMove()
            mapHandler.loadScreen(screen)
            newDrone.displayPaths(screen)
            screen.blit(newDrone.image, (newDrone.position - pygame.Vector2(newDrone.size.x/2, newDrone.size.y/2)))
            pygame.display.flip()

    clock.tick(120)
    tickHi += 1
    await asyncio.sleep(0)
asyncio.run(main())