import pygame
import sys
import math
import mapHandler
import asyncio

width = 1280
length = 600
differ = 20

class drone:
    blacklistZone = []
    tempBlacklistZone = []
    def updateBlacklistZone():
        drone.tempBlacklistZone.clear()
        for i in mapHandler.mapCols:
            if (i.dragable):
                drone.tempBlacklistZone.append({"xMin": i.rect.left - differ, "xMax": i.rect.right + differ, "yMin": i.rect.top - differ, "yMax": i.rect.bottom + differ})
                
    def setupBlacklist():
        for i in mapHandler.mapCols:
            if (not i.dragable):
                drone.blacklistZone.append({"xMin": i.rect.left - differ, "xMax": i.rect.right + differ, "yMin": i.rect.top - differ, "yMax": i.rect.bottom + differ})
        drone.updateBlacklistZone()

    def checkIfBlacklisted(vec2):
        for val in drone.blacklistZone:
            if (val.get("xMin") <= vec2.x <= val.get("xMax") and val.get("yMin") <= vec2.y <= val.get("yMax")): return True
        for val in drone.tempBlacklistZone:
            if (val.get("xMin") <= vec2.x <= val.get("xMax") and val.get("yMin") <= vec2.y <= val.get("yMax")): return True
        return False #not (0 <= vec2.x <= width and 0 <= vec2.y <= length)


    def __init__(self):
        self.size = pygame.Vector2(60, 60)
        self.image = pygame.transform.scale(pygame.image.load("rienriengoaway.png").convert_alpha(), (self.size.x, self.size.y)) 
        self.status = "Idle"
        self.position = pygame.Vector2(640, 300)
        self.rotation = 0 # we use this to figure out where rien is looking aka the direction he's moving and stuff
        self.target = pygame.Vector2(self.position.x, self.position.y)
        self.ticks = 0
        self.cachingSystem = {}
        self.truePath = []

    def displayPaths(self, surface):
        if self.status == "Idle":
            for key, val in self.cachingSystem.items():
                my_rect = pygame.Rect(int(val.get("position").x)-10, int(val.get("position").y)-10, 6, 6)
                pygame.draw.rect(surface, (255, 0, 0), my_rect)
        elif self.status == "Moving":
            for val in self.truePath:
                my_rect = pygame.Rect(int(val.x)-10, int(val.y)-10, 6, 6)
                pygame.draw.rect(surface, (0, 255, 0), my_rect)
        

    def findCenter(self, vec2):
        for i in range(0, width+1, differ):
            for j in range(0, length+1, differ):
                if (i <= vec2.x <= i+differ and j <= vec2.y <= j+differ):
                    return pygame.Vector2(i+(differ/2), j+(differ/2))
        return vec2
          

    def tickMove(self): # special function marked with "tick[NAME]" used to run everything parallel as i am working on figuring out proper coroutines
        if (self.status == "Moving"):
            if (len(self.truePath) > 0):
                next = self.truePath[0]
                if ((next - (self.position + self.size/2)).length() > 0):
                    self.position = self.position + (next - (self.position + self.size/2)).normalize()
                print("moved", next)
                hibye1 = 2
                if (next.x - hibye1 <= (self.position.x + self.size.x/2) <= next.x + hibye1 and next.y - hibye1 <= (self.position.y + self.size.y/2) <= next.y + hibye1): 
                #if (next.x == self.position.x and next.y == self.position.y): 
                    del self.truePath[0]
            else:
                self.target = self.position
                self.status = "Idle"
                print("done moving")

    def buildNewPath(self, target): #reminder that target should be a Vector2
        self.burnDOWN(target)

        startVec = self.findCenter(pygame.Vector2(self.position.x + self.size.x/2, self.position.y + self.size.y/2))
        endVec = self.findCenter(pygame.Vector2(target.x, target.y))
        
        self.cachingSystem[f"({startVec.x}, {startVec.y})"] = {"name": f"A20", "position": startVec, "success": False, "locked": False}
        self.cachingSystem[f"({endVec.x}, {endVec.y})"] = {"name": f"C20", "position": endVec, "success": True, "locked": False}

    def finality(self, originPath, fixPath):
        first = self.cachingSystem.get(originPath).get("name")[3:]
        last = self.cachingSystem.get(fixPath).get("name")
        for i in range(len(last), 3, -3):
            pulled = last[i-3:i]
            if pulled[0] == "N": first = f"{first}S20"
            elif pulled[0] == "E": first = f"{first}W20"
            elif pulled[0] == "S": first = f"{first}N20"
            elif pulled[0] == "W": first = f"{first}E20"

        lastPos = pygame.Vector2(self.position.x + self.size.x/2, self.position.y + self.size.y/2)
        for i in range(0, len(first)-2, 3):
            pulled = first[i:i+3]
            if pulled[0] == "N": lastPos = lastPos + pygame.Vector2(0, -differ)
            elif pulled[0] == "E": lastPos = lastPos + pygame.Vector2(differ, 0)
            elif pulled[0] == "S": lastPos = lastPos + pygame.Vector2(0, differ)
            elif pulled[0] == "W": lastPos = lastPos + pygame.Vector2(-differ, 0)
            self.truePath.append(lastPos)

        self.truePath.append(self.target)
        print(self.truePath)
        self.status = "Moving"

    def burnDOWN(self, target):
        self.status = "Idle"
        self.target = target
        self.truePath.clear()
        self.cachingSystem.clear()
        self.ticks = 0

    def burnout(self, nowVal, newLock):
        for key, val in self.cachingSystem.items():
            if ((nowVal.get("success") != val.get("success")) and newLock == val.get("position")):
                return (True, key)
        return (False, "nil")
    
    def tickFind(self):  # special function marked with "tick[NAME]" used to run everything parallel as i am working on figuring out proper coroutines
        max = 999999999
        if (self.ticks >= max): self.burnDOWN(self.position)
        if (self.status == "Idle" and self.target != self.position and self.ticks <= max):
            discovery = {}
            safe = True
            for key, val in self.cachingSystem.items():
                if not self.cachingSystem[key].get("locked") and safe:
                    currLoc = self.findCenter(val.get("position"))
                    finding = [ # (newLoc, newKey, newName)
                        (currLoc + pygame.Vector2(0, -differ), f'({currLoc.x}, {currLoc.y-differ})',  f'{val.get("name")}N20'), #NEVER
                        (currLoc + pygame.Vector2(differ, 0), f'({currLoc.x+differ}, {currLoc.y})',  f'{val.get("name")}E20'), #EAT
                        (currLoc + pygame.Vector2(0, differ), f'({currLoc.x}, {currLoc.y+differ})',  f'{val.get("name")}S20'), #SOGGY
                        (currLoc + pygame.Vector2(-differ, 0), f'({currLoc.x-differ}, {currLoc.y})',  f'{val.get("name")}W20') #WAFFLES
                    ]

                    for (newLoc, newKey, newName) in finding:
                        if (not drone.checkIfBlacklisted(newLoc)):
                            (good, jK) = self.burnout(val, newLoc)
                            if (good):
                                self.finality(key, jK)
                                safe = False
                                break
                            if (not newKey in self.cachingSystem and not newKey in discovery):
                                discovery[newKey] = {"name": newName, "position": newLoc, "success": val.get("success"), "locked": False}
                                self.ticks = self.ticks + 1
                            else:
                                print("blacklisted")
                self.cachingSystem[key]["locked"] = True
            self.cachingSystem = self.cachingSystem | discovery