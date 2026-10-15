import pygame
import sys
import math
import mapHandler
import asyncio

class drone:
    blacklistZone = []
    def updateBlacklistZone():
        for i in mapHandler.notGuff:
            drone.blacklistZone.clear()
            drone.blacklistZone.append({"xLeft": i.rect.left, "XRight": i.rect.right, "yTop": i.rect.top, "yBottom": i.rect.bottom})


    def __init__(self):
        self.size = pygame.Vector2(100, 100)
        self.image = pygame.transform.scale(pygame.image.load("rienriengoaway.png").convert_alpha(), (self.size.x, self.size.y)) 
        self.status = "Idle"
        self.position = pygame.Vector2(500, 300)
        self.rotation = 0 # we use this to figure out where rien is looking aka the direction he's moving and stuff

        self.cachingSystem = {}  
        self.truePath = {}
        self.active = {}

    def tickMove(self): # special function marked with "tick[NAME]" used to run everything parallel as i am working on figuring out proper coroutines
        if (not self.status == "Idle"):    
            print("hi") # replace this with looping through the truePath dictionary, start by reading the first 3 characters and keep going by every next 3 characters
    

    def buildNewPath(self, target):
        self.status = "Idle"
        self.truePath.clear()
        self.cachingSystem.clear()
        self.cachingSystem["T1-"] = {"position": self.position, "goal": target, "locked": True, "success": False}
        self.cachingSystem["F1-"] = {"position": self.position, "goal": target, "locked": False, "success": False}

        self.tickFind(self)
        # working on some code 
        # essentially trying to create a "SUCCESS" marked as true meeting up with a "SUCCESS" marked as false
        # the true success starts at the end location and goes outwards to the start, vice versa for the false success
        # once the false and true success are made, the path has successfully been found!


    def tickFind(self):  # special function marked with "tick[NAME]" used to run everything parallel as i am working on figuring out proper coroutines
        carryK, carryV = 0, 0
        for key, val in list(self.active.items()):
            print("hi")
        self.status = "Moving"