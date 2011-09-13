import pygame
from generic_bear import generic_bear

class side_bear(generic_bear):
    """The bears that are on the side of the river"""

    SWIPING = 0
    
    def __init__(self):
        generic_bear.__init__(self)
        self._target_range = 100
        self._swipe_duration = 300
        self._sipe_progress = 0
        self._swipe_width = 100
        self.paw_rect = None

    def update(self, time_since_last_frame, player):
        if (self.state == DEAD):
            return
        find_target(player)
        check_target_acquired()
        update_swipe(time_since_last_frame)
        update_paw_rect()

    def check_target_acquired(self):
        if (self.state == TARGET_ACQURIED):
            self.state = ACTING

    def update_swipe(time_since_last_frame):
        if (self.state == ACTING):
            self._swipe_progress += time_since_last_frame
            if (self._swipe_progress > self._swipe_duration):
                self._swipe_progress = 0
                self.state = WAITING

    def update_paw_rect():
        if (self.state == ACTING):
            self.paw_rect = self.rect.copy()
            self.paw_rect.x = self.rect.x + self.rect.width
            self.paw_rect.width = float(self._swipe_progress)/float(self._swipe_duration) * float(self._swipe_width)

    def check_player_collision(self, player):
        if (self.state == ACTING):
            if (self.paw_rect.colliderect(player.rect)):
                hit_player(player)
