import pygame
from generic_bear import generic_bear
from math import atan2, degrees, fabs, radians, cos, sin

class water_bear(generic_bear):
    """the bears that are on the rocks in the middle of the river"""
    JUMPING = 0
    SWIMMING = 1
    
    def __init__(self, player, x_position, y_position):
        generic_bear.__init__(self, x_position, y_position)
        self.image = pygame.image.load("img/panda_swim_down.png")
        self._max_preperation_time = 500
        self._preperation_time = self._max_preperation_time
        self.substate = None
        self.player = player
        self.speed = 200
        self.jump_multiplier = 0.5
        self.jump_duration = 250
        self.jump_progress = 0
        self.drift_speed = 100

    def update(self, time_since_last_frame):
        if (self.state == self.DEAD):
            return
        self.find_target(self.player)
        self.far_from_home()
        self.check_prep_time(time_since_last_frame)
        self.update_jump(time_since_last_frame)
        self.update_swim(time_since_last_frame)
        self.update_home(time_since_last_frame)
        self.check_player_collision(self.player)
        self.drift(time_since_last_frame)


    def check_prep_time(self, time_since_last_frame):
        if (self.state == self.TARGET_ACQUIRED):
            self.state = self.PREPARING
        elif (self.state == self.PREPARING):
            if (self._preperation_time < 0):
                self.state = self.ACTING
                self.substate = self.JUMPING
                self._preperation_time = self._max_preperation_time
            else:
                self._preperation_time -= time_since_last_frame

    def update_jump(self, time_since_last_frame):
        if (self.state != self.ACTING or self.substate != self.JUMPING):
            self.jump_progress = 0
            return
        self.jump_progress += time_since_last_frame
        #get direction to player
        distance_to_move = float(time_since_last_frame) / float(1000) * float(self.speed)
        angle_to_player = degrees(atan2(self.rect.centery - self.player.rect.centery, self.rect.centerx - self.player.rect.centerx))
        y_multiplier = 1
        x_multiplier = 1
        #if player is above bear, move up
        if (angle_to_player > 0):
            y_multiplier *= -1
        #if player is left of bear, move left
        if (fabs(angle_to_player) < 90):
            x_multiplier *= -1
        abs_x_diff = fabs(self.rect.centerx - self.player.rect.centerx)
        abs_y_diff = fabs(self.rect.centery - self.player.rect.centery)
        x_percent = float(abs_x_diff) / float(abs_x_diff + abs_y_diff)
        y_percent = float(abs_y_diff) / float(abs_x_diff + abs_y_diff)
        x_multiplier *= x_percent
        y_multiplier *= y_percent
        self.rect.move_ip(distance_to_move*x_multiplier*self.jump_multiplier,distance_to_move*y_multiplier*self.jump_multiplier)
        if (self.jump_progress > self.jump_duration):
            self.substate = self.SWIMMING

    def update_swim(self, time_since_last_frame):
        if (self.state != self.ACTING or self.substate != self.SWIMMING):
            return
        #get direction to player
        distance_to_move = float(time_since_last_frame) / float(1000) * float(self.speed)
        angle_to_player = degrees(atan2(self.rect.centery - self.player.rect.centery, self.rect.centerx - self.player.rect.centerx))
        y_multiplier = 1
        x_multiplier = 1
        #if player is above bear, move up
        if (angle_to_player > 0):
            y_multiplier *= -1
        #if player is left of bear, move left
        if (fabs(angle_to_player) < 90):
            x_multiplier *= -1
        abs_x_diff = fabs(self.rect.centerx - self.player.rect.centerx)
        abs_y_diff = fabs(self.rect.centery - self.player.rect.centery)
        x_percent = float(abs_x_diff) / float(abs_x_diff + abs_y_diff)
        y_percent = float(abs_y_diff) / float(abs_x_diff + abs_y_diff)
        x_multiplier *= x_percent
        y_multiplier *= y_percent
        self.rect.move_ip(distance_to_move*x_multiplier,distance_to_move*y_multiplier)

    def update_home(self, time_since_last_frame):
        if (self.state != self.GOING_HOME):
            return
        #get direction to player
        distance_to_move = float(time_since_last_frame) / float(1000) * float(self.speed)
        angle_to_home = degrees(atan2(self.rect.centery - self._original_y, self.rect.centerx - self._original_x))
        y_multiplier = 1
        x_multiplier = 1
        #if player is above bear, move up
        if (angle_to_home > 0):
            y_multiplier *= -1
        #if player is left of bear, move left
        if (fabs(angle_to_home) < 90):
            x_multiplier *= -1
        abs_x_diff = fabs(self.rect.centerx - self._original_x)
        abs_y_diff = fabs(self.rect.centery - self._original_y)
        if (abs_x_diff + abs_y_diff == 0):
            self.state = self.WAITING
            return
        x_percent = float(abs_x_diff) / float(abs_x_diff + abs_y_diff)
        y_percent = float(abs_y_diff) / float(abs_x_diff + abs_y_diff)
        x_multiplier *= x_percent
        y_multiplier *= y_percent
        self.rect.move_ip(distance_to_move*x_multiplier,distance_to_move*y_multiplier)
        if (self.get_distance(self.rect.x, self.rect.y, self._original_x, self._original_y) < 10):
            self.state = self.WAITING


    def draw(self, surface):
        surface.blit(self.image, self.rect, pygame.Rect(0,0,self.rect.width,self.rect.height))

    def force_going_home(self):
        self.state = self.GOING_HOME
