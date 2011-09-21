import pygame
from particle import particle



class water_particle(particle):
    """Particles from water balls"""

    def __init__(self, game, x_position, y_position):
        particle.__init__(self, game, game.water_particle_image, 5, 5, 50, x_position, y_position, 300, 800)
