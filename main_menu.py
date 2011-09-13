import pygame

class main_menu():
    """The Main Menu"""

    WAITING = 0
    RUNNING = 1
    FINISHED = 2
    
    def __init__(self, _game):
        self.state = main_menu.WAITING
        self.time_since_last_frame = 0
        self._game = _game
        self.font = pygame.font.Font(None, 36)
        self._start_text = self.font.render("Start Game", 1, (255, 255, 255))
        self._exit_text = self.font.render("Exit Game", 1, (255, 255, 255))
        self._options_text = self.font.render("Options", 1, (255, 255, 255))
        self.selected = 0
        self._options = [self._start_text, self._options_text, self._exit_text]
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load("img/riverproxy.png").convert()
        self.selector = pygame.image.load("img/selector_proxy.png").convert_alpha()

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
                if event.key == pygame.K_DOWN:
                    self.move_down()
                if event.key == pygame.K_UP:
                    self.move_up()

    def display(self, surface):
        self.draw_background(surface)
        for i,text in enumerate(self._options):
            vertical_space = 40
            text_pos = text.get_rect(centerx=surface.get_width()/2, centery=surface.get_height()/2 - vertical_space*len(self._options) + vertical_space*i)
            surface.blit(text, text_pos)

        selector_rect = self.selector.get_rect(centerx=self._options[self.selected].get_rect().x - self.selector.get_rect().width, centery=surface.get_height()/2 - vertical_space*len(self._options) + vertical_space*self.selected)
        surface.blit(self.selector, selector_rect)

    def move_down(self):
        self.selected += 1
        if (self.selected == len(self._options)):
            self.selected = 0

    def move_up(self):
        self.selected -= 1
        if (self.selected == -1):
            self.selected = len(self._options) - 1

    def draw_background(self, surface):
        background_rect = self.image.get_rect()
        surface.blit(self.image, pygame.Rect(0, 0, self.image.get_rect().width, self.image.get_rect().height))
