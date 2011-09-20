import pygame
from generic_bear import generic_bear

class side_bear(generic_bear):
    """The bears that are on the side of the river"""

    LEFT = 0
    RIGHT = 1
    PAW_UP = 0
    PAW_DOWN = 1
    
    def __init__(self, player, x_position, y_position):
        generic_bear.__init__(self, x_position, y_position)
        self.rect.width = 200
        self.rect.height = 200
        self._target_range = 300
        self._swipe_duration = 1000
        self._swipe_progress = 0
        self._swipe_width = 50
        self._swipe_height = 100
        self.paw_rect = None
        self.player = player
        self.drift_speed = 100
        if (self.rect.x < 400):
            self.attack_direction = self.RIGHT
        else:
            self.attack_direction = self.LEFT
        if (self.attack_direction == self.RIGHT):
            self.image = pygame.image.load("img/panda_swipe_left.png")
        else:
            self.image = pygame.image.load("img/panda_swipe_right.png")
        self.paw_state = self.PAW_UP

    def update(self, time_since_last_frame):
        if (self.state == self.DEAD):
            return
        self.update_swipe(time_since_last_frame)
        self.update_paw_rect()
        self.drift(time_since_last_frame)

    def update_swipe(self, time_since_last_frame):
        self._swipe_progress += time_since_last_frame
        if (self._swipe_progress > self._swipe_duration):
            self._swipe_progress -= self._swipe_duration
            if (self.paw_state == self.PAW_UP):
                self.paw_state = self.PAW_DOWN
            elif (self.paw_state == self.PAW_DOWN):
                self.paw_state = self.PAW_UP

    def update_paw_rect(self):
        if (self.paw_rect == None):
            self.paw_rect = self.rect.copy()
            self.paw_rect.height = self._swipe_height
            self.paw_rect.width = self._swipe_width

        if (self.attack_direction == self.RIGHT):
            self.paw_rect.x = self.rect.x + self.rect.width - self.paw_rect.width
        else:
            self.paw_rect.x = self.rect.x
        self.paw_rect.y = self.rect.y
        if (self.paw_state == self.PAW_DOWN):
            self.paw_rect.y += self.paw_rect.height

    def draw(self, surface):
        surface.fill((255,255,255), self.paw_rect)
        if (self.paw_state == self.PAW_UP):
            surface.blit(self.image, self.rect, pygame.Rect(0,0,self.rect.width, self.rect.height))
        else:
            surface.blit(self.image, self.rect, pygame.Rect(self.rect.width,0,self.rect.width, self.rect.height))
