import pygame
from math import sqrt

class generic_bear(pygame.sprite.Sprite):
    """Common parent class of bear enemies"""

    WAITING = 0
    TARGET_ACQUIRED = 1
    PREPARING = 2
    ACTING = 3
    DEAD = 4
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.state = WAITING
        self._frame = 0
        self._max_hp = 100
        self._health = self._max_hp
        self._target = None
        self._target_range = 500

    def find_target(self, player):
        if (self._target == None):
            self.state == WAITING
        if (self.state != WAITING):
            return
        distance = get_distance_to_player(player)
        if (distance < self._target_range):
            self._target = player
            self.state = TARGET_ACQUIRED

    def get_distance_to_player(self, player):
        return get_distance(self.rect.x, self.rect.y, player.rect.x, player.rect.y)

    def get_distance(self, x1, y1, x2, y2):
        return sqrt( (y2-y1)**2 + (x2-x1)**2 )

    def check_player_collision(self, player):
        if (self.rect.colliderect(player.rect)):
            hit_player(player)

    def hit_player(self, player):
        pass