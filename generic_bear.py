import pygame

class generic_bear(pygame.sprite.Sprite):
    """Common parent class of bear enemies"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
