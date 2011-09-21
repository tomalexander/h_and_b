import pygame
from key_capture import key_capture
from key_bindings import key_bindings

class options_menu():
    """The Options Menu"""

    WAITING = 0
    RUNNING = 1
    FINISHED = 2
    
    def __init__(self, _game):
        self.state = options_menu.WAITING
        self.time_since_last_frame = 0
        self._game = _game
        self.font = pygame.font.Font(None, 36)
        self.selected = 0
        self._options = []
        self.update_options()
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load("img/menu_background_proxy.png").convert()
        self.selector = pygame.image.load("img/selector_proxy.png").convert_alpha()
        self._rotate_duration = 1500
        self._rotate_progress = 0

    def update_options(self):
        self._options = []
        self._options.append(self.font.render("Up: " + key_bindings.get_list(self._game.key_bindings.up), 1, (255, 255, 255)))
        self._options.append(self.font.render("Down: " + key_bindings.get_list(self._game.key_bindings.down), 1, (255, 255, 255)))
        self._options.append(self.font.render("Left: " + key_bindings.get_list(self._game.key_bindings.left), 1, (255, 255, 255)))
        self._options.append(self.font.render("Right: " + key_bindings.get_list(self._game.key_bindings.right), 1, (255, 255, 255)))
        self._options.append(self.font.render("Barrel Roll Left: " + key_bindings.get_list(self._game.key_bindings.barrel_left), 1, (255, 255, 255)))
        self._options.append(self.font.render("Barrel Roll Right: " + key_bindings.get_list(self._game.key_bindings.barrel_right), 1, (255, 255, 255)))
        self._options.append(self.font.render("Shoot: " + key_bindings.get_list(self._game.key_bindings.shoot), 1, (255, 255, 255)))
        self._options.append(self.font.render("Dragon Mode: " + key_bindings.get_list(self._game.key_bindings.dragon), 1, (255, 255, 255)))
        

    def run(self, surface):
        self.state = options_menu.RUNNING
        while self.state == options_menu.RUNNING:
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
                    self.state = self.FINISHED
                elif event.key == pygame.K_DOWN:
                    self.move_down()
                elif event.key == pygame.K_UP:
                    self.move_up()
                elif event.key == pygame.K_RETURN:
                    self.rebind_key(surface)
                    self.update_options()
                    

    def rebind_key(self, surface):
        #editing_list = []
        editing_name = ""
        if (self.selected == 0):
            editing_list = self._game.key_bindings.up
            editing_name = "Up"
        if (self.selected == 1):
            editing_list = self._game.key_bindings.down
            editing_name = "Down"
        if (self.selected == 2):
            editing_list = self._game.key_bindings.left
            editing_name = "Left"
        if (self.selected == 3):
            editing_list = self._game.key_bindings.right
            editing_name = "Right"
        if (self.selected == 4):
            editing_list = self._game.key_bindings.barrel_left
            editing_name = "Barrel Roll Left"
        if (self.selected == 5):
            editing_list = self._game.key_bindings.barrel_right
            editing_name = "Barrel Roll Right"
        if (self.selected == 6):
            editing_list = self._game.key_bindings.shoot
            editing_name = "Shoot"
        if (self.selected == 7):
            editing_list = self._game.key_bindings.dragon
            editing_name = "Dragon"
        new_key = key_capture(self._game, "Primary " + editing_name)
        new_key.run(surface)
        if (new_key.value == pygame.K_ESCAPE):
            return
        del editing_list[:]
        editing_list.append(new_key.value)
        second_key = key_capture(self._game, "Secondary " + editing_name)
        second_key.run(surface)
        if (second_key.value == pygame.K_ESCAPE):
            editing_list.append(None)
            return
        editing_list.append(second_key.value)
        print editing_list
        

    def display(self, surface):
        self.draw_background(surface)
        for i,text in enumerate(self._options):
            vertical_space = 40
            text_pos = text.get_rect(centerx=surface.get_width()/2, centery=surface.get_height()/2 - vertical_space*len(self._options)/2 + vertical_space*i)
            surface.blit(text, text_pos)

        selector_rect = self.selector.get_rect()
        max_width = 0
        for text_surface in self._options:
            max_width = max(max_width, text_surface.get_width())
        selector_rect.centerx = surface.get_width()/2 - max_width/2 - 32
        selector_rect.centery = surface.get_height()/2 - vertical_space*len(self._options)/2 + vertical_space*self.selected
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
