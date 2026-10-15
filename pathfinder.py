import pygame
import sys
import math
import mapHandler
import asyncio


cachingSystem = {}  
thisDrone = 0
path = []
blacklistParts = []
class drone:
    def __init__(self):
        self.size = pygame.Vector2(60, 60)
        self.image = pygame.transform.scale(pygame.image.load("assets/droneShip.png").convert_alpha(), (self.size.x, self.size.y)) 
        self.idle = True
        self.position = pygame.Vector2(500, 300)
        self.rotation = 0
        global thisDrone
        thisDrone = self

    def move(self):
        global path
        if (not self.idle):    
            if (len(path) > 1):
                myNode = path[1]
                oldNode = path[0]
                if not (myNode.get("start").x -5 < (self.position).x and myNode.get("start").x + 5 > (self.position).x and myNode.get("start").y + 5 > (self.position).y and myNode.get("start").y - 5 < (self.position).y):
                    self.position = self.position + oldNode.get("moveVec")
                    print(oldNode)
                else:
                    del path[0]
            if len(path) == 1:
                myNode = path[0].get("goal")
                if not (myNode.x -5 < (self.position).x and myNode.x + 5 > (self.position).x and myNode.y + 5 > (self.position).y and myNode.y - 5 < (self.position).y):
                    self.position = self.position + path[0].get("moveVec")
                    print(path[0])
                else:
                    self.idle = True
                    path.clear()
            

    def buildNewPath(self, target):
        global path
        global cachingSystem
        self.idle = True
        path.clear()
        cachingSystem.clear()

        for i in mapHandler.notGuff:
            print("hi")

        cachingSystem["T1-"] = {"position": self.position, "goal": target, "name": "T1-", "locked": False, "success": False, "type": "goal"}

    def tickForward(self): 
        global path
        global cachingSystem
        carryK, carryV = 0, 0
        for key, val in list(cachingSystem.items()):
            if (not val.get("locked")):


                    
                if (val.get("goal").x - 20 < val.get("current").x and val.get("current").x < val.get("goal").x + 20) and (val.get("goal").y - 20 < val.get("current").y and val.get("current").y < val.get("goal").y + 20):
                    val["locked"] = True
                    val["success"] = True
                    carryK = key
                    carryV = val
                    break
    
        if carryV != 0:
            if carryV.get("success"):
                for i in range(3, len(carryK)+1, 3):
                    sendToList = cachingSystem.get(carryK[0:i])
                    path.append(sendToList)
                self.idle = False
                cachingSystem.clear()