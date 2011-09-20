import pygame

class generic_bar():
    """the player's coy fish"""
    def __init__(self, value, maximum, bar_color, border_color, x_position, y_position, width, height):
        self.value = value
        self.maximum = maximum
        self.bar_color = bar_color
        self.border_color = border_color
        self.border_rect = pygame.Rect(x_position, y_position, width, height)
        self.bar_rect = self.border_rect.copy()
        self.border_width = 2

    def add_value(self, inp):
        self.value += inp
        if (self.value > self.maximum):
            self.value = self.maximum

    def sub_value(self, inp):
        self.value -= inp
        if (self.value < 0):
            self.value = 0

    def set_value(self, inp):
        self.value = inp
        if (self.value < 0):
            self.value = 0
        if (self.value > self.maximum):
            self.value = self.maximum

    def update_bar_rect(self):
        self.bar_rect.height = self.border_rect.height * self.value / self.maximum
        self.bar_rect.y = self.border_rect.y + self.border_rect.height - self.bar_rect.height

    def draw(self, surface):
        self.update_bar_rect()
        surface.fill(self.bar_color, self.bar_rect)
        pygame.draw.rect(surface, self.border_color, self.border_rect, self.border_width)
