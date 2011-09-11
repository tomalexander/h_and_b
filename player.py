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
        self.barrel = [False, False] #barrel roll controls
        self.shoot = False
        self.dragon = False
        self.frame = 0
		
    def update(self, FrameRate):
        """handles input"""
        #Negate any contradictory movements
        if self.moving[0] and self.moving[1]:
            return
        elif self.moving[2] and self.moving[3]:
            return
        #MOVEMENT
        #up
        if self.moving[0]:
            future = self.rect.move(0, -self.yvel*FrameRate)
            if(future.top<534):
                self.rect.top=534
            else:
                self.rect = future
        elif self.moving[1]:
            future = self.rect.move(0, self.yvel*FrameRate)
            if(future.bottom>800):
                self.rect.bottom = 800
            else:
                self.rect = future
        if self.moving[2]:
            future = self.rect.move(-self.xvel*FrameRate, 0)
            if(future.left < 75):
                self.rect.left = 75
            else:
                self.rect = future
        elif self.moving[3]:
            future = self.rect.move(self.xvel*FrameRate, 0)
            if(future.right > 525):
                self.rect.right = 525
            else:
                self.rect = future
	

    def draw(self, screen):
        """draws koi"""
        screen.blit(self.image, self.rect);
