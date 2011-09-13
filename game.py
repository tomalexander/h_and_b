import sys
import pygame
from player import player
from main_menu import main_menu

class game():
    
    def __init__(self):
        """Main running function"""
        self.windowx = 640
        self.windowy = 800
        pygame.init()
        self.clock = pygame.time.Clock()
        self.set_up_screen()
        self.time_since_last_frame = 0.0
        self.enemies = []
        self.player = player()
        self.distance = 0
        self.worldspeed = 1 #distance per ms for river image movement
        self.riverimg = pygame.image.load("img/riverproxy.png").convert()
        pass

    def run(self):
        """Begin running the game"""
        the_menu = main_menu(self)
        the_menu.run(self.screen)
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.time_since_last_frame = float(self.clock.tick(60))

    def set_up_screen(self):
        """Initialize the window"""
        self.screen = pygame.display.set_mode((self.windowx, self.windowy))
        pygame.display.set_caption("A Game With Koi Fish, Bears, Debris, and DRAGON MODE!!!!111!!!11!!!!1one")
        pygame.mouse.set_visible(0)
    
    def draw(self):
        """Draw all the things!"""
        #Currently, the setup is up to two images dealing with the scrolling river
        riverrect = self.riverimg.get_rect()
        ydisp = (self.distance/2)%riverrect.height
        self.screen.blit(self.riverimg, pygame.Rect(0, ydisp, self.windowx, self.windowy))
        self.screen.blit(self.riverimg, pygame.Rect(0, ydisp - riverrect.height, self.windowx, self.windowy))
        self.player.draw(self.screen)
        
    def update(self):
        """Update every frame"""
        self.distance += self.time_since_last_frame * self.worldspeed
        if self.time_since_last_frame > 0:
            self.player.update(self.time_since_last_frame)
        else:
            self.player.update(0)

    def handle_events(self):
        """Handle events (such as key presses)"""
        #TODO: Implement Koi shooting + Dragon Mode Controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game() #If close button clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()
		#KOI CONTROLS (pardon the intrusion)
				#movement
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.moving[0] = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.moving[1] = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.moving[2] = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.moving[3] = True
				#abilities
                if event.key == pygame.K_q:
                    self.player.barrel[0] = True
                if event.key == pygame.K_e:
                    self.player.barrel[1] = True
                if event.key == pygame.K_SPACE:
                    self.player.shoot = True
                if event.key == pygame.K_r:
                    self.player.dragon = True
            if event.type == pygame.KEYUP:
				#cancelling movement
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.moving[0] = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.moving[1] = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.moving[2] = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.moving[3] = False
				#cancelling abilities
                if event.key == pygame.K_q:
                    self.player.barrel[0] = True
                if event.key == pygame.K_e:
                    self.player.barrel[1] = True
                if event.key == pygame.K_SPACE:
                    self.player.shoot = False

    def exit_game(self):
        """Exit the game"""
        pygame.quit()
        sys.exit()
 
