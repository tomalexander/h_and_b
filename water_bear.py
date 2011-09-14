import pygame
from generic_bear import generic_bear

class water_bear(generic_bear):
    """the bears that are on the rocks in the middle of the river"""
    JUMPING = 0
    SWIMMING = 1
    
    def __init__(self, player):
        generic_bear.__init__(self)
        self.image = pygame.image.load("img/water_bear_proxy.png")
        self._max_preperation_time = 500
        self._preperation_time = self._max_preperation_time
        self.substate = None
        self.player = player

    def update(self, time_since_last_frame):
        if (self.state == DEAD):
            return
        find_target(self.player)
        check_prep_time(time_since_last_frame)
        update_jump(time_since_last_frame)
        update_swim(time_since_last_frame)
        check_player_collision(self.player)

    def check_prep_time(self, time_since_last_frame):
        if (self.state == TARGET_ACQUIRED):
            self.state = PREPARING
        elif (self.state == PREPARING):
            if (self._preperation_time < 0):
                self.state = ACTING
                self.substate = JUMPING
                self._preperation_time = self._max_preperation_time
            else:
                self._preperation_time -= time_since_last_frame

    def update_jump(self, time_since_last_frame):
        pass

    def update_swim(self, time_since_last_frame):
        pass

    def draw(self, surface):
        pass
