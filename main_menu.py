import pygame

class main_menu():
    """the player's coy fish"""

    WAITING = 0
    RUNNING = 1
    FINISHED = 2
    
    def __init__(self, _game):
        self.state = main_menu.WAITING
        self.time_since_last_frame = 0
        self._game = _game
        self.font = pygame.font.Font(None, 36)
        self._start_text = font.render("Start Game", 1, (255, 255, 255))
        self._exit_text = font.render("Exit Game", 1, (255, 255, 255))
        self.selected = 0
        self._options = [self._start_text, self._exit_text]

    def run(self, surface):
        self.state = main_menu.RUNNING
        while self.state == main_menu.RUNNING:
            self.handle_events()
            self.display(surface)
            pygame.display.flip()
            self.time_since_last_frame = self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.exit_game() #If close button clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._game.exit_game()

    def display(self, surface):
        for i,text in enumerate(self._options):
            text_pos = text.get_rect(centerx=surface.get_width()/2, centery=surface.get_height()/2 - 10*len(self._options) + 10*i)
            surface.blit(text, text_pos)
