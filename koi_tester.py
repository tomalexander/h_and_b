#testing for koi
import sys
import pygame
from player import player

class Game(object):
    def __init__(self):
        """initializes the game"""
        pygame.init()
        self.screen = pygame.display.set_mode((675, 800))
        self.clock = pygame.time.Clock()
        self.player = player()
        self.FrameRate = 1
        self.SCREENRECT = pygame.Rect(0, 0, 675, 800)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_UP:
                    self.player.moving[0] = True
                if event.key == pygame.K_DOWN:
                    self.player.moving[1] = True
                if event.key == pygame.K_LEFT:
                    self.player.moving[2] = True
                if event.key == pygame.K_RIGHT:
                    self.player.moving[3] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.player.moving[0] = False
                if event.key == pygame.K_DOWN:
                    self.player.moving[1] = False
                if event.key == pygame.K_LEFT:
                    self.player.moving[2] = False
                if event.key == pygame.K_RIGHT:
                    self.player.moving[3] = False

    def update(self):
        self.player.update(self.FrameRate)

    def draw(self):
        background = pygame.Surface(self.SCREENRECT.size).convert()
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        self.player.draw(self.screen)
    

g = Game()
while True:
    g.clock.tick(30) #sets framerate
    g.process_events()
    g.update()
    g.draw()
    pygame.display.flip() #prints to screen