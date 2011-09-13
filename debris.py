#debris.py
import random
import pygame
import math

class debris(object):
    """the debris class"""
    def __init__(self, x, ang):
        self.image = pygame.image.load("img/debris1proxy.png")
        self.scale = random.randrange(1, 5)
        pygame.transform.scale(self.image, (self.scale*self.image.get_rect().width, self.scale*self.image.get_rect().height))
        self.rect = self.image.get_rect()
        #spawn debris at the top of the river
        self.rect.move_ip(x, 0)
        self.angle = ang
        self.xvel = 70
        self.yvel = 70

    def update(self, FrameRate):
        """updates debris"""
        return self.move(FrameRate)
        
    def move(self, FrameRate):
        """moves debris along its trajectory"""
        #self.rect.move_ip(self.xvel*math.cos(self.angle)*FrameRate, self.yvel*math.sin(self.angle)*FrameRate)
        self.rect.move_ip(0, self.yvel*FrameRate)
        if self.rect.left < 0:
            return False
        elif self.rect.right > 600:
            return False
        elif self.rect.top < 0:
            return False
        return True
        
    def collide(self, enemies):
        """collision detection - takes a list of enemy rects"""
        pass

    def draw(self, screen):
        """draws the bullet"""
        screen.blit(self.image, self.rect)
