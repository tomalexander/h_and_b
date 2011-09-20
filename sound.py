import pygame
from random import choice

class game_music():
    def __init__(self):
        self.background = pygame.mixer.music.load("sound/background.ogg")
        pygame.mixer.music.play(-1, 0.0)
        self.drop = [pygame.mixer.Sound("sound/30341__junggle__waterdrop24.wav"), pygame.mixer.Sound("sound/drop1.ogg"), pygame.mixer.Sound("sound/drop2.ogg"), pygame.mixer.Sound("sound/drop3.ogg"), pygame.mixer.Sound("sound/drop4.ogg"), pygame.mixer.Sound("sound/drop5.ogg")]
        self.rawr = [pygame.mixer.Sound("sound/4511__noisecollector__dragon7.wav"), pygame.mixer.Sound("sound/85568__joelaudio__dragon-roar.wav")]
        self.hit = [pygame.mixer.Sound("sound/38156__jcambs1990__stomp-that.wav")]
        self.fireball = [pygame.mixer.Sound("sound/45809__themfish__gas-fire-catch.wav")]

    def play_rawr(self):
        choice(self.rawr).play()

    def play_drop(self):
        choice(self.drop).play()

    def play_hit(self):
        choice(self.hit).play()

    def play_fireball(self):
        choice(self.fireball).play()
