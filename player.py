import pygame
from bullet import bullet
import math

class player(object):
    """the player's koi fish"""
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.images = [pygame.image.load("img/koiproxy.png"), pygame.image.load("img/dragonproxy.png")]
        self.rect = self.images[0].get_rect()
        #move koi to the middle of the screen
        self.rect.move_ip(284, 534)
        self.xvel = 35
        self.yvel = 35
        #CONTROL LOCKS
        #movement: up, down, left, right
        self.moving = [False, False, False, False]
        #barrel roll controls [q pressed, e pressed, time since q, time since e, cooldown]
        self.barrel = [False, False, 0.0, 0.0, 0.0]
        #shooting
        self.shoot = False
        self.shoot_cooldown = 0.0
        self.projectiles = []
        #dragon mode activated
        self.dragon = False
        self.frame = 0
		
    def update(self, FrameRate):
        """handles input"""
        FrameRate = FrameRate/100
        #we're going to move if we aren't in the middle of a roll
        lock = self.barrel_roll(FrameRate)
        if lock == False:
            self.move(FrameRate)
        #handle shooting
        self.shoot_cooldown -= FrameRate
        if self.shoot_cooldown < 0.0:
            self.shoot_cooldown = 0.0
        if self.shoot == True:
            if self.shoot_cooldown == 0.0:
                new_bullet = bullet(self.rect.left+16, self.rect.top, math.pi/2)
                self.projectiles.append(new_bullet)
                self.shoot_cooldown = 0.5
        for projectile in self.projectiles:
            projectile.update(FrameRate)
            

    #ABILITIES
    def barrel_roll(self, FrameRate):
        #reset cooldown
        self.barrel[4] -= FrameRate
        if self.barrel[4] < 0.0:
            self.barrel[4] = 0.0
        #contradictory input receives and we're not in the middle of anything
        if self.barrel[0] and self.barrel[1] and self.barrel[2]==0 and self.barrel[3]==0:
            return False
        #check to see if a left-roll is in progress or if we're free to start one
        if self.barrel[2]>0.0 or (self.barrel[0] and self.barrel[3]==0.0 and self.barrel[4]==0.0):
            self.barrel[0] = False
            #check to see if we're done, otherwise continue
            if self.barrel[2] >= 1.0:
                #reset utilites
                self.barrel[4] = 1.0
                self.barrel[2] = 0.0
                return False
            else:
                #advance animation
                self.roll_left(FrameRate)
                return True
        elif self.barrel[3]>0.0 or(self.barrel[1] and self.barrel[2]==0.0 and self.barrel[4]==0.0):
            #again, check if done, otherwise continue
            self.barrel[1] = False
            if self.barrel[3] >= 1.0:
                #reset utilities
                self.barrel[4] = 1.0
                self.barrel[3] = 0.0
                return False
            else:
                #advance animation
                self.roll_right(FrameRate)
                return True
        #if nothing is going on in here
        else:
            return False

    def roll_left(self, FrameRate):
        self.barrel[2] += FrameRate
        future = self.rect.move(-self.xvel*2*FrameRate, 0)
        if future.left < 75:
            self.rect.left = 75
        else:
            self.rect = future
                
    def roll_right(self, FrameRate):
        self.barrel[3] += FrameRate
        future = self.rect.move(self.xvel*2*FrameRate, 0)
        if future.right > 525:
            self.rect.right = 525
        else:
            self.rect = future
    
    #MOVEMENT
    def move(self, FrameRate):
    #Negate any contradictory movements
        if self.moving[0] and self.moving[1]:
            return
        elif self.moving[2] and self.moving[3]:
            return
        
        #up
        if self.moving[0]:
            future = self.rect.move(0, -self.yvel*FrameRate)
            if(future.top<534):
                self.rect.top=534
            else:
                self.rect = future
        #down
        elif self.moving[1]:
            future = self.rect.move(0, self.yvel*FrameRate)
            if(future.bottom>800):
                self.rect.bottom = 800
            else:
                self.rect = future
        #left
        if self.moving[2]:
            future = self.rect.move(-self.xvel*FrameRate, 0)
            if(future.left < 75):
                self.rect.left = 75
            else:
                self.rect = future
        #right
        elif self.moving[3]:
            future = self.rect.move(self.xvel*FrameRate, 0)
            if(future.right > 525):
                self.rect.right = 525
            else:
                self.rect = future
	
    #DRAGON MODE
    def dragon_mode(self, FrameRate):
        pass
        
    def shoot(self, FrameRate):
        pass
        
    def draw(self, screen):
        """draws koi"""
        screen.blit(self.images[0], self.rect);
        for projectile in self.projectiles:
            projectile.draw(screen)

