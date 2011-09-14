import pygame
from math import sqrt

class generic_bear(object):
    """Common parent class of bear enemies"""

    WAITING = 0
    TARGET_ACQUIRED = 1
    PREPARING = 2
    ACTING = 3
    DEAD = 4
    
    def __init__(self, x_position, y_position):
        self.state = self.WAITING
        self._frame = 0
        self._max_hp = 100
        self._health = self._max_hp
        self._target = None
        self._target_range = 500
        self._original_x = x_position
        self._original_y = y_position
        self.rect = pygame.Rect(x_position, y_position, 210, 120)

    def find_target(self, player):
        if (self._target == None):
            self.state == self.WAITING
        if (self.state != self.WAITING):
            return
        distance = self.get_distance_to_player(player)
        if (distance < self._target_range):
            self._target = player
            self.state = self.TARGET_ACQUIRED

    def get_distance_to_player(self, player):
        return self.get_distance(self.rect.x, self.rect.y, player.rect.x, player.rect.y)

    def get_distance(self, x1, y1, x2, y2):
        return sqrt( (y2-y1)**2 + (x2-x1)**2 )

    def check_player_collision(self, player):
        if (self.rect.colliderect(player.rect)):
            self.hit_player(player)

    def hit_player(self, player):
        pass
