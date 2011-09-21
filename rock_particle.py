import pygame
from particle import particle



class rock_particle(particle):
    """Particles from rock balls"""

    def __init__(self, game, x_position, y_position):
        particle.__init__(self, game, game.rock_particle_image, 5, 10, 100, x_position, y_position, 3000, 5000)
