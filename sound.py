import pygame


class game_music():
    def __init__(self):
        self.background = pygame.mixer.music.load("sound/background.ogg")
        pygame.mixer.music.play(-1, 0.0)
