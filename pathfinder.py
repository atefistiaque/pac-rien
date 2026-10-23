import pygame
import sys
import math
import mapHandler
import asyncio

class drone:
    blacklistZone = []
    tempBlacklistZone = []
    def updateBlacklistZone():
        drone.tempBlacklistZone.clear()
        for i in mapHandler.mapCols:
            if (i.dragable):
                drone.tempBlacklistZone.append({"xMin": i.rect.left, "xMax": i.rect.right, "yMin": i.rect.top, "yMax": i.rect.bottom})
                
    def setupBlacklist():
        for i in mapHandler.mapCols:
            if (not i.dragable):
                drone.blacklistZone.append({"xMin": i.rect.left, "xMax": i.rect.right, "yMin": i.rect.top, "yMax": i.rect.bottom})
        drone.updateBlacklistZone()

    def checkIfBlacklisted(vec2):
        for val in drone.blacklistZone:
            if (val.get("xMin") < vec2.x < val.get("xMax") and val.get("yMin") < vec2.y < val.get("yMax")): return True
        for val in drone.tempBlacklistZone:
            if (val.get("xMin") < vec2.x < val.get("xMax") and val.get("yMin") < vec2.y < val.get("yMax")): return True
        return False


    def __init__(self):
        self.size = pygame.Vector2(50, 50)
        self.image = pygame.transform.scale(pygame.image.load("rienriengoaway.png").convert_alpha(), (self.size.x, self.size.y)) 
        self.status = "Idle"
        self.position = pygame.Vector2(640, 300)
        self.rotation = 0 # we use this to figure out where rien is looking aka the direction he's moving and stuff
        self.target = pygame.Vector2(self.position.x, self.position.y)

        self.cachingSystem = {}  
        self.truePath = []

    def displayPaths(self, surface):
        for key, val in self.cachingSystem.items():
            surface.set_at((int(val.get("position").x), int(val.get("position").y)), (10, 50, 10))


    def tickMove(self): # special function marked with "tick[NAME]" used to run everything parallel as i am working on figuring out proper coroutines
        if (self.status == "Moving"):
            print("try move")
            if (len(self.truePath) > 0):
                self.position = self.position + self.truePath[0]
                print("moved", self.truePath[0])
                del self.truePath[0]
            else:
                self.target = self.position
                self.status = "Idle"
                print("done moving")

    def buildNewPath(self, target): #reminder that target should be a Vector2
        self.status = "Idle"
        self.target = target
        self.truePath.clear()
        self.cachingSystem.clear()
        self.cachingSystem[f"({self.position.x + self.size.x/2}, {self.position.y + self.size.y/2})"] = {"name": f"A1-", "position": self.position, "success": False, "locked":False, "previousList": {}}
        self.cachingSystem[f"({target.x}, {target.y})"] = {"name": f"C1-", "position": target, "success": True, "locked": False, "previousList": {}}

    def finality(self, originPath, fixPath):
        print("protocol 3")
        first = self.cachingSystem.get(originPath).get("name")[3:]
        last = self.cachingSystem.get(fixPath).get("name")
        for i in range(len(last), 6, -3):
            pulled = last[i-3:i]
            if pulled[0] == "N": first = f"{first}S1-"
            elif pulled[0] == "E": first = f"{first}W1-"
            elif pulled[0] == "S": first = f"{first}N1-"
            elif pulled[0] == "W": first = f"{first}E1-"

        lastPos = self.position.copy()
        for i in range(len(first), 3, -3):
            if pulled[0] == "N": lastPos = lastPos + pygame.Vector2(0, -1)
            elif pulled[0] == "E": lastPos = lastPos + pygame.Vector2(1, 0)
            elif pulled[0] == "S": lastPos = lastPos + pygame.Vector2(0, 1)
            elif pulled[0] == "W": lastPos = lastPos + pygame.Vector2(-1, 0)
            self.truePath.append(lastPos)
        self.status = "Moving"
        print("finalized")

    
    def tickFind(self):  # special function marked with "tick[NAME]" used to run everything parallel as i am working on figuring out proper coroutines
        if (self.status == "Idle" and self.target != self.position):
            discovery = {}
            for key, val in self.cachingSystem.items():
                if not self.cachingSystem[key].get("locked"):
                    currLoc = val.get("position")
                    finding = [ # (newLoc, newKey, newName)
                        (currLoc + pygame.Vector2(0, -1), f'({currLoc.x}, {currLoc.y-1})',  f'{val.get("name")}N1-'), #NEVER
                        (currLoc + pygame.Vector2(1, 0), f'({currLoc.x+1}, {currLoc.y})',  f'{val.get("name")}E1-'), #EAT
                        (currLoc + pygame.Vector2(0, 1), f'({currLoc.x}, {currLoc.y+1})',  f'{val.get("name")}S1-'), #SOGGY
                        (currLoc + pygame.Vector2(-1, 0), f'({currLoc.x-1}, {currLoc.y})',  f'{val.get("name")}W1-') #WAFFLES
                    ]


                    for (newLoc, newKey, newName) in finding:
                        if (not drone.checkIfBlacklisted(newLoc)):
                            if (newKey in self.cachingSystem and self.cachingSystem[newKey].get("success") and not val.get("success")):
                                self.finality(key, newKey)
                            if (not newKey in self.cachingSystem):
                                print("finding")
                                discovery[newName] = {"name": newName, "position": newLoc, "success": val.get("success"), "locked": False, "previousList": val.get("previousList", {}) | {f'{currLoc.x}, {currLoc.y}': True}}
                                print(discovery.get(newName))
                self.cachingSystem[key]["locked"] = True
            self.cachingSystem = self.cachingSystem | discovery