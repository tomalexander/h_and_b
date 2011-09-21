import pygame

class key_capture():
    """The Key Capture Menu"""

    WAITING = 0
    RUNNING = 1
    FINISHED = 2
    
    def __init__(self, _game, text):
        self.state = key_capture.WAITING
        self.time_since_last_frame = 0
        self._game = _game
        self.font = pygame.font.Font("fonts/SVBasicManual.ttf", 36)
        self._main_text = self.font.render("Binding " + text + ", Hit any key or Escape", 1, (255, 255, 255))
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load("img/menu_background_proxy.png").convert()
        self._rotate_duration = 1500
        self._rotate_progress = 0
        self.value = pygame.K_ESCAPE

    def run(self, surface):
        self.state = key_capture.RUNNING
        while self.state == key_capture.RUNNING:
            self.handle_events()
            self.update_progress(self.time_since_last_frame)
            self.display(surface)
            pygame.display.flip()
            self.time_since_last_frame = self.clock.tick(60)

    def update_progress(self, time_since_last_frame):
        self._rotate_progress += time_since_last_frame
        while (self._rotate_progress > self._rotate_duration):
            self._rotate_progress -= self._rotate_duration

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.exit_game() #If close button clicked
            elif event.type == pygame.KEYDOWN:
                self.value = event.key
                self.state = self.FINISHED

    def display(self, surface):
        self.draw_background(surface)
        text_pos = self._main_text.get_rect(centerx=surface.get_width()/2, centery=surface.get_height()/2)
        surface.blit(self._main_text, text_pos)

    def draw_background(self, surface):
        background_rect = self.image.get_rect()
        #Wooo scrolling background
        y_progress = float(-1) * float(self._rotate_progress) / float(self._rotate_duration) * float(self.image.get_rect().height)
        surface.blit(self.image, pygame.Rect(0, 0, self.image.get_rect().width, self.image.get_rect().height), pygame.Rect(0, y_progress, self.image.get_rect().width, self.image.get_rect().height))
        surface.blit(self.image, pygame.Rect(0, -1 * (self.image.get_rect().height+y_progress), self.image.get_rect().width, self.image.get_rect().height), pygame.Rect(0, 0, self.image.get_rect().width, self.image.get_rect().height))
