import pygame
import math

class lady_koi(object):
    """the player's koi fish"""
    def __init__(self, windowx):
        #pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = pygame.image.load("img/koi_f.png")
        self.rect = self.image.get_rect()
        #move koi to the middle of the screen
        self.rect.move_ip(284, 0)
        self.xvel = 35
        self.yvel = 35
        self.windowx = windowx
		
    def update(self, FrameRate):
        """handles input"""
        FrameRate = FrameRate/100
        
        self.move(FrameRate)

   
    #MOVEMENT
    def move(self, FrameRate):
        if self.rect.bottom > 400:
            self.rect.move_ip(0, -self.yvel*FrameRate)
        
        
    def draw(self, screen):
        """draws koi"""
        screen.fill((255,255,255), self.rect)
        screen.blit(self.images[0], self.rect, pygame.Rect(32*(self.frame), 0, 32, 64))
        

