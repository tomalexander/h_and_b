import pygame

class evil_koi(object):
    """the final boss"""
    def __init__(self, windowx):
        #pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.images = [pygame.image.load("img/evilkoiproxy.png"), pygame.image.load("img/dragonproxy.png")]
        self.rect = self.images[0].get_rect()
        self.energy = 0
        #move evil koi to the middle of the screen
        self.rect.move_ip(284, 0)
        self.xvel = 35
        self.yvel = 35
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
        
        
    def update(self, FrameRate):
        
    def automove(self, FrameRate):
        
        
        if self.rect.left < 100:
            self.rect.left = 100
        elif self.rect.right > windowx - 180:
            self.rect.right = windowx - 180
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > 400:
            self.rect.bottom = 400

    def dragon_mode(self, FrameRate):
        

    def shoot(self, screen):
        

    def draw:
        