import pygame

class generic_bar():
    """Vertical Bar Class"""
    def __init__(self, value, maximum, bar_color, border_color, x_position, y_position, width, height):
        self.value = value
        self.maximum = maximum
        self.bar_color = bar_color
        self.border_color = border_color
        self.border_rect = pygame.Rect(x_position, y_position, width, height)
        self.bar_rect = self.border_rect.copy()
        self.border_width = 2

    def add_value(self, inp):
        """Add to value, capped at maximum"""
        self.value += inp
        if (self.value > self.maximum):
            self.value = self.maximum

    def sub_value(self, inp):
        """Subtract from value, capped at 0"""
        self.value -= inp
        if (self.value < 0):
            self.value = 0

    def set_value(self, inp):
        """Set the value of the bar, capped at 0 and maximum"""
        self.value = inp
        if (self.value < 0):
            self.value = 0
        if (self.value > self.maximum):
            self.value = self.maximum

    def update_bar_rect(self):
        """update the rect that is to be blitted"""
        self.bar_rect.height = self.border_rect.height * self.value / self.maximum
        self.bar_rect.y = self.border_rect.y + self.border_rect.height - self.bar_rect.height

    def draw(self, surface):
        self.update_bar_rect()
        surface.fill(self.bar_color, self.bar_rect)
        pygame.draw.rect(surface, self.border_color, self.border_rect, self.border_width)
