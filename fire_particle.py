import pygame
from particle import particle



class fire_particle(particle):
    """Particles from fire balls"""

    def __init__(self, game, x_position, y_position):
        particle.__init__(self, game, game.fire_particle_image, 5, 10, 100, x_position, y_position, 500, 1500)
