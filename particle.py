import pygame
from random import random, choice, randint, uniform

class particle():
    """HERES YOUR PARTICLES DR MARC"""

    def __init__(self, game, image, wiggle_room, min_speed, max_speed, x_position, y_position, min_duration, max_duration):
        self.game = game
        self.wiggle_room = wiggle_room
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.min_duration = float(min_duration)
        self.max_duration = float(max_duration)
        self.duration = 0.0
        self.total_duration = uniform(self.min_duration, self.max_duration)
        self.x_position = float(x_position) + float(randint(0, self.wiggle_room))
        self.y_position = float(y_position) + float(randint(0, self.wiggle_room))
        self.rect = pygame.Rect(self.x_position, self.y_position, 5, 5)
        self.image = image.copy() #pygame.image.load("img/")
        self.x_multiplier = random()
        self.y_multiplier = 1 - self.x_multiplier
        self.x_direction = choice([-1, 1])
        self.y_direction = choice([-1, 1])
        self.speed = randint(self.min_speed, self.max_speed)
        self.x_vel = self.speed * self.x_multiplier * self.x_direction
        self.y_vel = self.speed * self.y_multiplier * self.y_direction
        self.dead = False
        

    def update(self, time_since_last_frame):
        if (not self.dead):
            self.x_position += float(self.x_vel) * float(time_since_last_frame)/float(1000)
            self.y_position += float(self.y_vel) * float(time_since_last_frame)/float(1000)
            self.rect.x = self.x_position
            self.rect.y = self.y_position
            self.duration += time_since_last_frame
            if (self.duration >= self.total_duration):
                self.dead = True
            self.image.set_alpha(255 - 255*(self.duration / self.total_duration))

    def draw(self, surface):
        if (not self.dead):
            surface.blit(self.image, self.rect)
