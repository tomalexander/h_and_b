#debris.py
import random
import pygame
import math

class debris(object):
    """the debris class"""
    def __init__(self, x, ang):
        self.image = pygame.image.load("img/debrisproxy.png")
        self.scale = random.randrange(1, 5)
        pygame.transform.scale(self.image, (self.scale*self.image.get_rect().width, self.scale*self.image.get_rect().height))
        self.rect = self.image.get_rect()
        self.type = "debris"
        #spawn debris at the top of the river
        self.rect.move_ip(x, 0)
        self.angle = ang
        self.xvel = 60
        self.yvel = 60 #should be fine now

    def update(self, FrameRate):
        """updates debris"""
        FrameRate = FrameRate/100
        return self.move(FrameRate)
    
    def displace(self, bubble_rect):
        self.angle=-math.atan2(self.rect.centery-bubble_rect.centery, self.rect.centerx - bubble_rect.centerx)
        if self.yvel > -20:
            self.yvel -=20
        
        
    def move(self, FrameRate):
        """moves debris along its trajectory"""
        
        if self.yvel < 60:
            self.yvel += 5
        self.rect.move_ip(math.cos(self.angle)*self.xvel*FrameRate, -math.sin(self.angle)*self.yvel*FrameRate)

        #bounce off of the sides of the river
        if self.rect.left < 100:
            self.angle += math.pi/2
        elif self.rect.right > 500:
            self.angle += math.pi/2
        
        #elif self.rect.top < 0:
        #    return False
        return True

    def draw(self, screen):
        """draws the bullet"""
        screen.blit(self.image, self.rect)

class rock(debris):
    """unbreakable type debris"""
    def __init__(self, x, ang):
        debris.__init__(self, x, ang)
        #reset image, scale, and rect
        self.image = pygame.image.load("img/unbreakable.png")
        self.scale = random.randrange(1, 5)
        pygame.transform.scale(self.image, (self.scale*self.image.get_rect().width, self.scale*self.image.get_rect().height))
        self.rect = self.image.get_rect()
        self.type == "rock"
        self.xvel = 50
        self.yvel = 50
        
    