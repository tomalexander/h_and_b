import pygame
from bullet import bullet
from bullet import fireball
import math

class player(object):
    """the player's koi fish"""
    def __init__(self, windowx, game):
        #pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.images = [pygame.image.load("img/koi.png"), pygame.image.load("img/dragon_sheet.png"), pygame.image.load("img/transform_two.png"), pygame.image.load("img/koi_flip.png")]
        self.rect = self.images[0].get_rect()
        self.rect.width = 32
        self.energy = 0.0
        #move koi to the middle of the screen
        self.rect.move_ip(284, 534)
        self.xvel = 35
        self.yvel = 35
        #CONTROL LOCKS
        #movement: up, down, left, right
        self.moving = [False, False, False, False]
        #barrel roll controls [q pressed, e pressed, time since q, time since e, cooldown]
        self.barrel = [False, False, 0.0, 0.0, 0.0]
        self.barrel_lock = False
        #shooting
        self.shoot = False
        self.shoot_cooldown = 0.75
        self.projectiles = []
        #dragon mode activated
        self.dragon = False
        self.dragon_prescene = 0
        self.dragon_pre_lock = False
        self.dragon_cooldown = 0.0
        self.dragon_prereq = 300
        self.dragon_flag = False
        #animation utilities
        self.frame = 0
        self.windowx = windowx
        self.game = game
        self.death_time = 0.0
        self.regular = True
        self.frames = 0
        self.death = False
		
    def update(self, FrameRate):
        """handles input"""
        FrameRate = FrameRate/100
        self.frames += 1
        
        if self.regular:
            if self.frames % 30 < 15:
                self.frame = 0
            else:
                self.frame = 1
        
        self.energy += 0.5
        if self.energy > 300.0:
            self.energy = 300.0
        
        #we're going to move if we aren't in the middle of a roll
        self.barrel_lock = self.barrel_roll(FrameRate)
        if not self.barrel_lock:
            self.move(FrameRate)
        
        #handle dragon mode attempt
        if self.dragon == True:
            self.pre_dragon(FrameRate)
        
        #handle shooting
        self.handle_shoot(FrameRate)
                
        #pass projectiles back to game
        return self.projectiles

    #ABILITIES
    def barrel_roll(self, FrameRate):
        #reset cooldown
        self.barrel[4] -= FrameRate
        if self.barrel[4] < 0.0:
            self.barrel[4] = 0.0
        #check to see if we even have enough energy
        if self.energy < 50:
            self.barrel[0] = False
            self.barrel[1] = False
            return False
        #optional: take out dragon's barrel roll
        if self.dragon:
            self.barrel[0] = False
            self.barrel[1] = False
            return False
        #contradictory input received and we're not in the middle of anything
        if self.barrel[0] and self.barrel[1] and self.barrel[2]==0 and self.barrel[3]==0:
            self.barrel[0] = False
            self.barrel[1] = False
            return False
        #check to see if a left-roll is in progress or if we're free to start one
        if self.barrel[2]>0.0 or (self.barrel[0] and self.barrel[3]==0.0 and self.barrel[4]==0.0):
            self.barrel[0] = False
            #check to see if we're done, otherwise continue
            if self.barrel[2] >= 5.0:
                #reset utilites
                self.barrel[4] = 1.0
                self.barrel[2] = 0.0
                self.energy -= 100
                self.regular = True
                return False
            else:
                #advance animation
                self.regular = False
                self.roll_left(FrameRate)
                return True
        elif self.barrel[3]>0.0 or(self.barrel[1] and self.barrel[2]==0.0 and self.barrel[4]==0.0):
            #again, check if done, otherwise continue
            self.barrel[1] = False
            if self.barrel[3] >= 5.0:
                #reset utilities
                self.barrel[4] = 1.0
                self.barrel[3] = 0.0
                self.energy -= 100
                self.regular = True
                return False
            else:
                #advance animation
                self.regular = False
                self.roll_right(FrameRate)
                return True
        #if nothing is going on in here
        else:
            return False

    def roll_left(self, FrameRate):
        self.barrel[2] += FrameRate
        #handle animation
        if self.barrel[2] < 1.25:
            self.frame = 3
        elif self.barrel[2] < 2.50:
            self.frame = 2
        elif self.barrel[2] < 3.75:
            self.frame = 1
        else:
            self.frame = 0
        
        #handle actual movement
        acc = 1.3
        if self.dragon:
            acc = 1.5
        future = self.rect.move(-self.xvel*acc*FrameRate, 0)
        if future.left < 100:
            self.rect.left = 100
        else:
            self.rect = future
                
    def roll_right(self, FrameRate):
        self.barrel[3] += FrameRate
        #handle animation
        if self.barrel[3] < 1.25:
            self.frame = 1
        elif self.barrel[3] < 2.50:
            self.frame = 2
        elif self.barrel[3] < 3.75:
            self.frame = 3
        else:
            self.frame = 0
        
        #handle actual movement
        acc = 1.3
        if self.dragon:
            acc = 1.5
        future = self.rect.move(self.xvel*acc*FrameRate, 0)
        if future.right > self.windowx - 180:
            self.rect.right = self.windowx - 180
        else:
            self.rect = future
    
    #MOVEMENT
    def move(self, FrameRate):
        updown_lock = False
        leftright_lock = False
        #Negate any contradictory movements
        if self.moving[0] and self.moving[1]:
            updown_lock = True
        elif self.moving[2] and self.moving[3]:
            leftright_lock = True
        
        if not updown_lock:
            #up
            if self.moving[0]:
                future = self.rect.move(0, -self.yvel*FrameRate)
                if(future.top<400):
                    self.rect.top=400
                else:
                    self.rect = future
            #down
            elif self.moving[1]:
                future = self.rect.move(0, self.yvel*FrameRate)
                if(future.bottom>800):
                    self.rect.bottom = 800
                else:
                    self.rect = future
        if not leftright_lock:
            #left
            if self.moving[2]:
                future = self.rect.move(-self.xvel*FrameRate, 0)
                if(future.left < 100):
                    self.rect.left = 100
                else:
                    self.rect = future
            #right
            elif self.moving[3]:
                future = self.rect.move(self.xvel*FrameRate, 0)
                if(future.right > self.windowx-180):
                    self.rect.right = self.windowx-180
                else:
                    self.rect = future
    
    def pre_dragon(self, FrameRate):
        #disable dragon mode if they don't have enough energy
        if self.energy < self.dragon_prereq and not self.dragon_flag:
            self.dragon = False
            return
        if self.dragon_prescene >= 30:
            self.dragon_mode(FrameRate)
            return
        #start dragon transform sequence
        self.regular = False
        self.dragon_prescene += 1
        self.rect.width = 48
        self.rect.height = 96
        
        #animations!
        if self.dragon_prescene % 10 < 5:
            self.frame = 0
        else:
            self.frame = 1
    
    #ACTIVATING AND DEACTIVATING DRAGON MODE
    def dragon_mode(self, FrameRate):
        self.dragon_pre_lock = True
        self.dragon_flag = True
        #activate dragon mode
        self.rect.width = 48
        self.rect.height = 96
        self.dragon_cooldown += FrameRate
        self.energy -= 1.5
        #do animations
        if self.dragon_cooldown % 30 < 15:
            self.frame = 1
        else:
            self.frame = 0
        #deactivate dragon mode
        if self.dragon_cooldown > 50.0:
            self.energy = 0.0
            self.frame = 0
            self.dragon = False
            self.dragon_cooldown = 0
            self.rect.width = 32
            self.rect.height = self.images[0].get_rect().height
            self.dragon_prescene = 0
            self.dragon_flag = False
            self.dragon_pre_lock = False
            self.regular = True

    def handle_shoot(self, FrameRate):
        self.shoot_cooldown -= FrameRate
        if self.shoot_cooldown < 0.0:
            self.shoot_cooldown = 0.0
        
        if self.shoot == True and self.shoot_cooldown == 0.0:
            if not self.dragon:
                self.game.music.play_drop()
                new_bullet = bullet(self.rect.left+16, self.rect.top, math.pi/2)
                self.projectiles.append(new_bullet)
                self.shoot_cooldown = 2.0
            else:
                self.game.music.play_fireball()
                new_fireball = fireball(self.rect.left+16, self.rect.top, math.pi/2)
                self.projectiles.append(new_fireball)
                self.shoot_cooldown = 1.5
        for i, projectile in enumerate(self.projectiles):
            if not projectile.update(FrameRate):
                self.projectiles.pop(i)
    
    def move_to_mid(self, FrameRate):
        FrameRate = FrameRate/100
    
        if self.rect.left > 284:
            self.rect.move_ip(-self.xvel*FrameRate, self.yvel*FrameRate)
        elif self.rect.left < 284:
            self.rect.move_ip(self.xvel*FrameRate, self.yvel*FrameRate)
            
        if self.rect.left > 264 and self.rect.left < 304:
            self.rect.left = 284
        
        if self.rect.top > 400:
            self.rect.top = 400
    
    def death_animation(self, FrameRate):
        FrameRate = FrameRate/100
        self.death = True
        self.death_time += FrameRate
        self.regular = False
        self.rect.move_ip(0, 25*FrameRate)
        if self.death_time < 1.25:
            self.frame = 1
        else:
            self.frame = 2
        
    
    def draw(self, screen):
        """draws koi"""
        #screen.fill((255,255,255), self.rect)
        if self.death:
            screen.blit(self.images[0], self.rect, pygame.Rect(32*(self.frame), 0, 32, 64))
        elif not self.dragon and not self.barrel_lock:
            screen.blit(self.images[3], self.rect, pygame.Rect(32*(self.frame), 0, 32, 64))
        elif not self.dragon:
            screen.blit(self.images[0], self.rect, pygame.Rect(32*(self.frame), 0, 32, 64))
        elif self.dragon and not self.dragon_pre_lock:
            screen.blit(self.images[2], self.rect, pygame.Rect(48*(self.frame), 0, 48, 96))
        else:
            screen.blit(self.images[1], self.rect, pygame.Rect(48*(self.frame), 0, 48, 96))

        for projectile in self.projectiles:
            projectile.draw(screen)

