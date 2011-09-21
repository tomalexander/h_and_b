import pygame
from options_menu import options_menu

class main_menu():
    """The Main Menu"""

    WAITING = 0
    RUNNING = 1
    FINISHED = 2
    
    def __init__(self, _game):
        self.state = main_menu.WAITING
        self.time_since_last_frame = 0
        self._game = _game
        self.title_font = pygame.font.Font("fonts/Aquanaut.ttf", 96)
        self.font = pygame.font.Font("fonts/SVBasicManual.ttf", 36)
        self._start_text = self.font.render("Start Game", 1, (255, 255, 255))
        self._exit_text = self.font.render("Exit Game", 1, (255, 255, 255))
        self._options_text = self.font.render("Options", 1, (255, 255, 255))
        self._restart_text = self.font.render("Restart Game", 1, (255, 255, 255))
        self._title_text = self.title_font.render("Finding Nema", 1, (255,255,255))
        self.selected = 0
        self._options = [self._start_text, self._options_text, self._exit_text, self._restart_text]
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load("img/menu_background_proxy.png").convert()
        self.selector = pygame.image.load("img/selector_proxy.png").convert_alpha()
        self._rotate_duration = 1500
        self._rotate_progress = 0
        self.restart_game = False

    def run(self, surface):
        self.state = main_menu.RUNNING
        while self.state == main_menu.RUNNING:
            self.handle_events(surface)
            self.update_progress(self.time_since_last_frame)
            self.display(surface)
            pygame.display.flip()
            self.time_since_last_frame = self.clock.tick(60)

    def update_progress(self, time_since_last_frame):
        self._rotate_progress += time_since_last_frame
        while (self._rotate_progress > self._rotate_duration):
            self._rotate_progress -= self._rotate_duration

    def handle_events(self, surface):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.exit_game() #If close button clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._game.exit_game()
                elif event.key == pygame.K_DOWN:
                    self.move_down()
                elif event.key == pygame.K_UP:
                    self.move_up()
                elif event.key == pygame.K_RETURN:
                    if (self.selected == 0): #start game
                        self.state = main_menu.FINISHED
                    if (self.selected == 1): #options
                        sub_menu = options_menu(self._game)
                        sub_menu.run(surface)
                    if (self.selected == 2): #end game
                        self._game.exit_game()
                    if (self.selected == 3):
                        self.restart_game = True
                        self.state = main_menu.FINISHED

    def display(self, surface):
        self.draw_background(surface)
        self.title_pos = self._title_text.get_rect(centerx=surface.get_width()/2, centery=surface.get_height()/8)
        surface.blit(self._title_text, self.title_pos)
        for i,text in enumerate(self._options):
            vertical_space = 40
            text_pos = text.get_rect(centerx=surface.get_width()/2, centery=surface.get_height()/2 - vertical_space*len(self._options) + vertical_space*i)
            surface.blit(text, text_pos)

        selector_rect = self.selector.get_rect()
        selector_rect.centerx = surface.get_width()/3.5
        selector_rect.centery = surface.get_height()/2 - vertical_space*len(self._options) + vertical_space*self.selected
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
        y_progress = float(-1) * float(self._rotate_progress) / float(self._rotate_duration) * float(self.image.get_rect().height)
        surface.blit(self.image, pygame.Rect(0, 0, self.image.get_rect().width, self.image.get_rect().height), pygame.Rect(0, y_progress, self.image.get_rect().width, self.image.get_rect().height))
        surface.blit(self.image, pygame.Rect(0, -1 * (self.image.get_rect().height+y_progress), self.image.get_rect().width, self.image.get_rect().height), pygame.Rect(0, 0, self.image.get_rect().width, self.image.get_rect().height))
