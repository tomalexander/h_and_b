#testing for koi
import sys
import pygame
from player import player
from debris import debris
import math
import random

class Game(object):
    def __init__(self):
        """initializes the game"""
        pygame.init()
        self.screen = pygame.display.set_mode((675, 800))
        self.clock = pygame.time.Clock()
        self.player = player()
        self.FrameRate = 1
        self.SCREENRECT = pygame.Rect(0, 0, 675, 800)
        self.debris = False
        self.debris_list = []

    def process_events(self):
        for event in pygame.event.get():
            #PRESSING KEYS
            if event.type == pygame.KEYDOWN:
            #movement
                if event.key == pygame.K_h:
                    self.debris = True
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_w:
                    self.player.moving[0] = True
                if event.key == pygame.K_s:
                    self.player.moving[1] = True
                if event.key == pygame.K_a:
                    self.player.moving[2] = True
                if event.key == pygame.K_d:
                    self.player.moving[3] = True
            #abilities
                if event.key == pygame.K_q:
                    self.player.barrel[0] = True
                if event.key == pygame.K_e:
                    self.player.barrel[1] = True
                if event.key == pygame.K_SPACE:
                    self.player.shoot = True
                if event.key == pygame.K_r:
                    self.player.dragon = True
            #RELEASING KEYS
            if event.type == pygame.KEYUP:
            #movement
                if event.key == pygame.K_h:
                    self.debris = False
                if event.key == pygame.K_w:
                    self.player.moving[0] = False
                if event.key == pygame.K_s:
                    self.player.moving[1] = False
                if event.key == pygame.K_a:
                    self.player.moving[2] = False
                if event.key == pygame.K_d:
                    self.player.moving[3] = False
            #abilities
                if event.key == pygame.K_q:
                    self.player.barrel[0] = False
                if event.key == pygame.K_e:
                    self.player.barrel[1] = False
                if event.key == pygame.K_SPACE:
                    self.player.shoot = False

    def update(self):
        FrameRate = float(self.clock.tick(60))
        self.player.update(FrameRate)
        if self.debris == True:
            new_debris = debris(random.randrange(0, 600), -math.pi/2)
            self.debris_list.append(new_debris)
        for thing in self.debris_list:
            thing.update(FrameRate)

    def draw(self):
        background = pygame.Surface(self.SCREENRECT.size).convert()
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        for thing in self.debris_list:
            thing.draw(self.screen)
        self.player.draw(self.screen)
    

g = Game()
while True:
    g.clock.tick(30) #sets framerate
    g.process_events()
    g.update()
    g.draw()
    pygame.display.flip() #prints to screen