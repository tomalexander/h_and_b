import sys
import pygame
from player import player

class game():
    """Main running function"""
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.time_since_last_frame = 0
        self.enemies = []
        self.player = player()
        pass

    def run(self):
        """Begin running the game"""
        self.set_up_screen()
        while True:
            self.handle_events()
            pygame.display.flip()
            self.time_since_last_frame = self.clock.tick(60)

    def set_up_screen(self):
        """Initialize the window"""
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("REPLACE THIS TITLE")
        pygame.mouse.set_visible(0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game() #If close button clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()
		#KOI CONTROLS (pardon the intrusion)
				#movement
                if event.key == pygame.K_UP:
                    self.player.moving[0] = True
                if event.key == pygame.K_DOWN:
                    self.player.moving[1] = True
                if event.key == pygame.K_LEFT:
                    self.player.moving[2] = True
                if event.key == pygame.K_RIGHT:
                    self.player.moving[3] = True
				#abilities
                if event.key == pygame.K_q:
                    self.player.barrel[0] = True
                if event.key == pygame.K_e:
                    self.player.barrel[1] = True
            if event.type == pygame.KEYUP:
				#cancelling movement
                if event.key == pygame.K_UP:
                    self.player.moving[0] = False
                if event.key == pygame.K_DOWN:
                    self.player.moving[1] = False
                if event.key == pygame.K_LEFT:
                    self.player.moving[2] = False
                if event.key == pygame.K_RIGHT:
                    self.player.moving[3] = False
				#cancelling abilities
                if event.key == pygame.K_q:
                    self.player.barrel[0] = True
                if event.key == pygame.K_e:
                    self.player.barrel[1] = True

    def exit_game(self):
        pygame.quit()
        sys.exit()
 
