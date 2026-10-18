import pygame
import sys
import asyncio

width = 1280
length = 600

score = 0

objects = []
mapCols = pygame.sprite.Group()
trueWall = pygame.sprite.Group()
class mapObject(pygame.sprite.Sprite):
    def __init__(self, objName, image, objVerts):
        super().__init__()
        self.objName = objName
        self.objVerts = objVerts
        if self.objName == "wall": trueWall.add(self)

        self.dragable = objName == "drag"
        if self.dragable: self.objName = "wall"
        
        if self.objName == "wall": mapCols.add(self)
        self.image = pygame.transform.scale(image, (self.objVerts.get("sizeX"), self.objVerts.get("sizeY")))
        self.rect = self.image.get_rect()
        self.rect.x = self.objVerts.get("spawnVec").x
        self.rect.y = self.objVerts.get("spawnVec").y
        objects.append(self)

def checkCols():
    for value in objects:
        touch = []
        if value.dragable: touch = pygame.sprite.spritecollide(value, trueWall, False)
        elif value.objName == "player": touch = pygame.sprite.spritecollide(value, mapCols, False)
        for block in touch:
            if (block.objName == "wall"):
                if (value.rect.top > block.rect.centery - (block.rect.height/2)) and (block.rect.right - 1 > value.rect.centerx > block.rect.left + 1): value.rect.top = block.rect.bottom
                elif (value.rect.bottom < block.rect.centery + (block.rect.height/2)) and (block.rect.right - 1 > value.rect.centerx > block.rect.left + 1):  value.rect.bottom = block.rect.top
                elif (value.rect.right < block.rect.centerx + (block.rect.width/2)) and (block.rect.bottom - 1 > value.rect.centery > block.rect.top + 1):  value.rect.right = block.rect.left
                elif (value.rect.left > block.rect.centerx - (block.rect.width/2)) and (block.rect.bottom - 1 > value.rect.centery > block.rect.top + 1):  value.rect.left = block.rect.right

def specialBounds():
    for val in objects:
        if (val.dragable):
            if val.rect.x > val.objVerts.get("maxX"): val.rect.x = val.objVerts.get("maxX")
            if val.rect.x < val.objVerts.get("minX"): val.rect.x = val.objVerts.get("minX") 
            if val.rect.y > val.objVerts.get("maxY"): val.rect.y = val.objVerts.get("maxY")
            if val.rect.y < val.objVerts.get("minY"): val.rect.y = val.objVerts.get("minY")

def genMap():
    mapObject("drag", pygame.image.load("wall.png").convert_alpha(), {"spawnVec": pygame.Vector2(200, 250), "sizeX":50, "sizeY": 75, "minX": 100, "maxX": 200, "minY": 100, "maxY":200})
    mapObject("wall", pygame.image.load("wall.png").convert_alpha(), {"spawnVec": pygame.Vector2(0, length-100), "sizeX":width, "sizeY": 100})
    mapObject("wall", pygame.image.load("wall.png").convert_alpha(), {"spawnVec": pygame.Vector2(0, 0), "sizeX":width, "sizeY": 100})
    
def loadScreen(screen): 
    checkCols()
    specialBounds()
    screen.fill((20, 24, 40))
    for val in objects: 
        if val.rect.x > width: val.rect.x = 0
        if val.rect.x < 0: val.rect.x = width 
        if val.rect.y > length: val.rect.y = 0
        if val.rect.y < 0: val.rect.y = length
        screen.blit(val.image, val.rect)
    font = pygame.font.SysFont("Arial", 32)
    surfScore = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(surfScore, (10, 10))