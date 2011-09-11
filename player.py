import pygame

class player(object):
    """the player's koi fish"""
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = pygame.image.load("img/koiproxy.png")
        self.rect = self.image.get_rect()
        #move koi to the middle of the screen
        self.rect.move_ip(284, 534)
        self.rect.width = 32
        self.rect.height = 64
        self.xvel = 6
        self.yvel = 6
        #control locks
        self.moving = [False, False, False, False] #up, down, left, right
        #barrel roll controls [q pressed, e pressed, time since q, time since e, cooldown]
        self.barrel = [False, False, 0.0, 0.0, 0.0]
        self.shoot = False
        self.dragon = False
        self.frame = 0
		
    def update(self, FrameRate):
        """handles input"""
        FrameRate = FrameRate/10
        #we're going to move if we aren't in the middle of a roll
        lock = self.barrel_roll(FrameRate)
        if lock == False:
            self.move(FrameRate)

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
            if self.barrel[3] >= 1.0:
                #reset utilities
                self.barrel[4] = 1.0
                self.barrel[3] = 0.0
                return False
            else:
                #advance animation
                self.barrel[3] += FrameRate
                self.roll_right(FrameRate)
                return True
        #if nothing is going on in here
        else:
            return False

    def roll_left(self, FrameRate):
        self.barrel[3] += FrameRate
        future = self.rect.move(-self.xvel*2*FrameRate, 0)
        if future.right > 525:
            self.rect.right = 525
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
	

    def draw(self, screen):
        """draws koi"""
        screen.blit(self.image, self.rect);
