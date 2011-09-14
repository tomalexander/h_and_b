import sys
import pygame
from player import player
from main_menu import main_menu
from key_bindings import key_bindings
from debris import debris

class game():
    
    def __init__(self):
        """Main running function"""
        self.windowx = 640
        self.windowy = 800
        pygame.init()
        self.clock = pygame.time.Clock()
        self.set_up_screen()
        self.time_since_last_frame = 0.0
        self.enemy_text = open("enemies.txt").readlines()
        self.enemy_data = self.interp_enemies(self.enemy_text)
        self.enemies = []
        self.player = player()
        self.distance = 0
        self.worldspeed = 1 #distance per ms for river image movement
        self.riverimg = pygame.image.load("img/riverproxy.png").convert()
        self.landimgl = pygame.image.load("img/landproxy.png").convert()
        #self.landimgr = pygame.image.load("img/landproxy.png").convert()
        self.landimgr = pygame.transform.rotate(self.landimgl, 180)
        self.key_bindings = key_bindings()
        self.screen_rect = pygame.Rect(0,0,self.windowx,self.windowy)

    def interp_enemies(self, enemy_txt):
        """translate enemies.txt input into a list of tuples"""
        new_data = []
        for entry in enemy_txt:
            someline = entry.split(',')
            #print someline
            new_data.append([int(someline[0]), someline[1], int(someline[2]), int(someline[3])]) #2D Array!
        #Some test code:
        #for en in new_data:
            #print "At time %i, spawn a %s at position (%i, %i)"%(en[0], en[1], en[2], en[3])
        return new_data

    def run(self):
        """Begin running the game"""
        the_menu = main_menu(self)
        the_menu.run(self.screen)
        self.clock.tick()
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
        landrectl = self.landimgl.get_rect()
        landrectr = self.landimgr.get_rect()
        ydisp = (self.distance/2)%riverrect.height
        self.screen.blit(self.riverimg, pygame.Rect(0, ydisp, self.windowx, self.windowy))
        self.screen.blit(self.riverimg, pygame.Rect(0, ydisp - riverrect.height, self.windowx, self.windowy))
        self.screen.blit(self.landimgl, pygame.Rect(0, ydisp, self.windowx, self.windowy))
        self.screen.blit(self.landimgl, pygame.Rect(0, ydisp - landrectl.height, self.windowx, self.windowy))
        self.screen.blit(self.landimgr, pygame.Rect(self.windowx - 160, ydisp, self.windowx, self.windowy))
        self.screen.blit(self.landimgr, pygame.Rect(self.windowx - 160, ydisp - landrectr.height, self.windowx, self.windowy))
        self.player.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)
        
    def update(self):
        """Update every frame"""
        self.distance += self.time_since_last_frame * self.worldspeed
        #think about using clock.tick(60) to have a consistent frame rate across different machines
        #^^^See run(self)
        self.player.update(self.time_since_last_frame)
        #After updating the player, let's deal with enemies
        #1. Check for enemies we need to add
        for enemy in self.enemy_data:
            if self.distance > enemy[0]:
                #Create the enemy, add it to self.enemies
                #print "It's been %i ms, time to spawn an enemy!"%self.distance
                if enemy[1] == "debris":
                    rdyenemy = debris(enemy[2],90)
                    self.enemies.append(rdyenemy)
                else:
                    print "INVALID ENEMY!"
                    exit_game()
                #Remove from data
                self.enemy_data.remove(enemy)
        #2. Update Enemies
        for en in self.enemies:
            en.update(self.time_since_last_frame)
        #3. Remove Enemies that are off screen
        for en in self.enemies:
            if not(self.screen_rect.colliderect(en.rect)):
                self.enemies.remove(en)
                #print "killing enemy!"

    def handle_events(self):
        """Handle events (such as key presses)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game() #If close button clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.activate_menu()
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

    def activate_menu(self):
        m = main_menu(self)
        m.run(self.screen)
                    
    def exit_game(self):
        """Exit the game"""
        pygame.quit()
        sys.exit()
 
