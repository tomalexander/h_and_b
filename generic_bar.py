import pygame

class generic_bar(pygame.sprite.Sprite):
    """the player's coy fish"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.value = 0
        self.maximum = 100
