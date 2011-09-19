import pygame
import math
from bullet import bullet
from bullet import fireball

class evil_koi(object):
    """the final boss"""
    def __init__(self, windowx):
        self.images = [pygame.image.load("img/evilkoiproxy.png"), pygame.image.load("img/evildragonproxy.png")]
        self.rect = self.images[0].get_rect()
        self.energy = 0
        #move evil koi to the middle of the screen
        self.rect.x = 250
        self.xvel = 35
        self.yvel = 35
        self.angle = 5*math.pi/4
        #CONTROL LOCKS
        self.shoot_cooldown = 0.75
        self.bad_projectiles = []
        #dragon mode activated
        self.dragon = False
        #animation utilities
        self.frame = 0
        self.windowx = windowx
        #boss battle flags
        self.health = 100
        self.retreated = False
        self.chargecooldown = 1.0
        self.strafedir = False
        
        
    def update(self, FrameRate):
        FrameRate = FrameRate/100
        
        #first boss stage
        if self.health > 60:
            self.automove(FrameRate)
            self.shoot(FrameRate)
        #second boss stage
        elif self.health > 30:
            self.dragon = True
            self.xvel = 70
            self.yvel = 70
            if not self.retreated:
                self.retreat(FrameRate)
            else:
                if self.chargecooldown > 0:
                    self.chargecooldown -= FrameRate
                    self.strafe(FrameRate)
                    self.shoot(FrameRate)
                else:    
                    self.charge(FrameRate)
        #third boss stage
        else:
            pass
        
        #update bullets        
        for i, projectile in enumerate(self.bad_projectiles):
            if not projectile.update(FrameRate):
                self.projectiles.pop(i)
        
        return self.bad_projectiles

    def strafe(self, FrameRate):
        if self.strafedir:
            self.rect.move_ip(self.xvel*FrameRate, 0)
        else:
            self.rect.move_ip(-self.xvel*FrameRate, 0)
        
        if self.rect.left < 100:
            self.rect.left = 100
            self.strafedir = True
        elif self.rect.right > 500:
            self.rect.right = 500
            self.strafedir = False
        
        
    def charge(self, FrameRate):
        self.rect.move_ip(0, self.yvel*2*FrameRate)
        
        if self.rect.bottom >= 800:
            self.chargecooldown = 5.0
            self.rect.bottom = 800
            self.retreated = False
        
    
    def retreat(self, FrameRate):
        #self.angle = math.atan2(self.rect.centery - 0, self.rect.centerx - 300)
        #self.rect.move_ip(self.xvel*FrameRate*math.cos(self.angle), -self.yvel*FrameRate*math.sin(self.angle))
        self.rect.move_ip(0, -self.yvel*FrameRate)
        
        if self.rect.top <= 0:
            self.rect.top = 0
            self.retreated = True
        
    def automove(self, FrameRate):
        self.rect.move_ip(self.xvel*FrameRate*math.cos(self.angle), -self.yvel*FrameRate*math.sin(self.angle))
        
        #strafe
        if self.rect.left < 100:
            self.rect.left = 100
            self.xvel = -self.xvel
        elif self.rect.right > self.windowx - 180:
            self.rect.right = self.windowx - 180
            self.xvel = -self.xvel
        if self.rect.top < 0:
            self.rect.top = 0
            self.yvel = -self.yvel
        elif self.rect.bottom > 400:
            self.rect.bottom = 400
            self.yvel = -self.yvel

    def take_damage(self):
        self.health -= 1
    
    def dragon_mode(self, FrameRate):
        pass
        

    def shoot(self, FrameRate):
        self.shoot_cooldown -= FrameRate
        if self.shoot_cooldown < 0.0:
            self.shoot_cooldown = 0.0
        
        if self.shoot_cooldown == 0.0:
            if not self.dragon:
                new_bullet = bullet(self.rect.left+16, self.rect.bottom, -math.pi/2)
                self.bad_projectiles.append(new_bullet)
                self.shoot_cooldown = 2.0
            else:
                new_fireball = fireball(self.rect.left+16, self.rect.bottom, -math.pi/2)
                self.bad_projectiles.append(new_fireball)
                self.shoot_cooldown = 1.5


    def draw(self, screen):
        """draws evil koi"""
        if not self.dragon:
            screen.blit(self.images[0], self.rect)
        else:
            screen.blit(self.images[1], self.rect)
        for projectile in self.bad_projectiles:
            projectile.draw(screen)
        