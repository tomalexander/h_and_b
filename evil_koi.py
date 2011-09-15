import pygame
import math

class evil_koi(object):
    """the final boss"""
    def __init__(self, windowx):
        #pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.images = [pygame.image.load("img/evilkoiproxy.png"), pygame.image.load("img/evildragonproxy.png")]
        self.rect = self.images[0].get_rect()
        self.energy = 0
        #move evil koi to the middle of the screen
        self.rect.move_ip(250, 0)
        self.xvel = 35
        self.yvel = 35
        self.angle = 5*math.pi/4
        #CONTROL LOCKS
        self.shoot_cooldown = 0.75
        self.bad_projectiles = []
        #dragon mode activated
        self.dragon = False
        self.dragon_cooldown = 0.0
        self.dragon_prereq = 300
        #animation utilities
        self.frame = 0
        self.windowx = windowx
        self.checkpoint_left = False
        self.checkpoint_right = False
        
        
    def update(self, FrameRate):
        FrameRate = FrameRate/100
        self.automove(FrameRate)
        
    def automove(self, FrameRate):
        self.rect.move_ip(self.xvel*FrameRate*math.cos(self.angle), -self.yvel*FrameRate*math.sin(self.angle))
        
        if self.rect.left < 100:
            self.rect.left = 100
            self.xvel = -self.xvel
            #self.angle = -math.pi/4
            #self.angle = math.atan2(self.rect.centery-400, self.rect.centerx-300)
        elif self.rect.right > self.windowx - 180:
            self.rect.right = self.windowx - 180
            #self.angle = math.atan2(-self.rect.top, 300-self.rect.right)
            #self.angle = 3*math.pi/4
            self.xvel = -self.xvel
        if self.rect.top < 0:
            self.rect.top = 0
            self.yvel = -self.yvel
            #self.angle = math.atan2(200-self.rect.top, 100-self.rect.right)
            #self.angle = -3*math.pi/4
        elif self.rect.bottom > 400:
            self.rect.bottom = 400
            self.yvel = -self.yvel
            #self.angle = math.atan2(200-self.rect.bottom, 500-self.rect.left)
            #self.angle = math.pi/4

    def dragon_mode(self, FrameRate):
        pass
        

    def shoot(self, FrameRate):
        pass

    def draw(self, screen):
        """draws evil koi"""
        if not self.dragon:
            screen.blit(self.images[0], self.rect)
        else:
            screen.blit(self.images[1], self.rect)
        for projectile in self.bad_projectiles:
            projectile.draw(screen)
        