import pygame
import sys
import asyncio

width = 1280
length = 600

score = -1

objects = {}
Guff = pygame.sprite.Group()
notGuff = pygame.sprite.Group()
class mapObject(pygame.sprite.Sprite):
    def __init__(self, objName, image, objVerts):
        super().__init__()
        objects[objName] = self
        self.objVerts = objVerts
        self.image = pygame.transform.scale(image, (self.objVerts.get("sizeX"), self.objVerts.get("sizeY")))
        self.rect = self.image.get_rect()
        self.rect.x = self.objVerts.get("spawnVec").x
        self.rect.y = self.objVerts.get("spawnVec").y
        if (objName == "macGuff"): 
            Guff.add(self)
            global score
            score += 1
        elif (objName != "player" and objName != "macGuff"): notGuff.add(self)

def loadScreen(screen): 
    screen.fill((20, 24, 40))
    for key, val in objects.items(): 
        screen.blit(val.image, val.rect)
    font = pygame.font.SysFont("Arial", 32)
    surfScore = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(surfScore, (10, 10))
