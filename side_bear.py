import pygame
from generic_bear import generic_bear

class side_bear(generic_bear):
    """The bears that are on the side of the river"""

    SWIPING = 0
    LEFT = -1
    RIGHT = 1
    
    def __init__(self, player, x_position, y_position):
        generic_bear.__init__(self, x_position, y_position)
        self.image = pygame.image.load("img/side_bear_proxy.png")
        self.paw_image = pygame.image.load("img/side_bear_proxy.png")
        self._target_range = 300
        self._swipe_duration = 1000
        self._swipe_progress = 0
        self._swipe_width = 100
        self._swipe_height = 100
        self.paw_rect = None
        self.player = player
        self.drift_speed = 100
        self.cooldown_duration = 1000
        self.cooldown_progress = 0
        if (self.rect.x < 400):
            self.attack_direction = self.RIGHT
        else:
            self.attack_direction = self.LEFT

    def update(self, time_since_last_frame):
        if (self.state == self.DEAD):
            return
        self.find_target(self.player)
        self.check_target_acquired()
        self.update_swipe(time_since_last_frame)
        self.update_paw_rect()
        self.update_cooldown(time_since_last_frame)
        self.drift(time_since_last_frame)

    def check_target_acquired(self):
        if (self.state == self.TARGET_ACQUIRED):
            self.state = self.ACTING

    def update_swipe(self, time_since_last_frame):
        if (self.state == self.ACTING):
            self._swipe_progress += time_since_last_frame
            if (self._swipe_progress > self._swipe_duration):
                self.enter_cooldown()

    def enter_cooldown(self):
        self._swipe_progress = 0
        self.state = self.COOLDOWN
        self.paw_rect = None
        self.cooldown_progress = 0

    def update_cooldown(self, time_since_last_frame):
        if (self.state != self.COOLDOWN):
            return
        self.cooldown_progress += time_since_last_frame
        if (self.cooldown_progress >= self.cooldown_duration):
            self.state = self.WAITING

    def update_paw_rect(self):
        if (self.state == self.ACTING):
            if (self.paw_rect == None):
                self.paw_rect = self.rect.copy()
                if (self.attack_direction == self.RIGHT):
                    self.paw_rect.x = self.rect.x + self.rect.width
                if (self.attack_direction == self.LEFT):
                    self.paw_rect.x = self.rect.x
            self.paw_rect.y = self.rect.y
            self.paw_rect.width = float(self._swipe_progress)/float(self._swipe_duration) * float(self._swipe_width)
            if (self.attack_direction == self.LEFT):
                self.paw_rect.x = self.rect.x - self.paw_rect.width
            self.paw_rect.height = self._swipe_height

    def check_player_collision(self, player):
        if (self.state == ACTING):
            if (self.paw_rect.colliderect(player.rect)):
                self.hit_player(player)
                
    def draw(self, surface):
        surface.blit(self.image, self.rect, pygame.Rect(0,0,self.rect.width, self.rect.height))
        if (self.paw_rect is not None):
            surface.blit(self.paw_image, self.paw_rect, pygame.Rect(0,0,self.paw_rect.width, self.paw_rect.height))
        pass
