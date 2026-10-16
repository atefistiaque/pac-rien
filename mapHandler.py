import pygame
import sys
import asyncio

width = 1280
length = 600

score = 0

objects = {}
class mapObject(pygame.sprite.Sprite):
    def __init__(self, objName, image, objVerts):
        super().__init__()
        objects[objName] = self
        self.objVerts = objVerts
        self.dragable = objName == "rien"
        self.image = pygame.transform.scale(image, (self.objVerts.get("sizeX"), self.objVerts.get("sizeY")))
        self.rect = self.image.get_rect()
        self.rect.x = self.objVerts.get("spawnVec").x
        self.rect.y = self.objVerts.get("spawnVec").y
        self.objName = objName

def loadScreen(screen): 
    screen.fill((20, 24, 40))
    for key, val in objects.items(): 
        if val.rect.x > width: val.rect.x = 0
        if val.rect.x < 0: val.rect.x = width 
        if val.rect.y > length: val.rect.y = 0
        if val.rect.y < 0: val.rect.y = length
        screen.blit(val.image, val.rect)
    font = pygame.font.SysFont("Arial", 32)
    surfScore = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(surfScore, (10, 10))