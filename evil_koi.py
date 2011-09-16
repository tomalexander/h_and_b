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
        #boss battle flags
        self.health = 100
        
        
    def update(self, FrameRate):
        FrameRate = FrameRate/100
        if self.health > 60:
            self.automove(FrameRate)
            self.shoot(FrameRate)
        elif self.health > 30:
            pass #secondary boss stage goes here
        else:
            pass #final boss stage goes here
        
            
        return self.bad_projectiles
        
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
        for i, projectile in enumerate(self.bad_projectiles):
            if not projectile.update(FrameRate):
                self.projectiles.pop(i)

    def draw(self, screen):
        """draws evil koi"""
        if not self.dragon:
            screen.blit(self.images[0], self.rect)
        else:
            screen.blit(self.images[1], self.rect)
        for projectile in self.bad_projectiles:
            projectile.draw(screen)
        