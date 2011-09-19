import sys
import pygame
from player import player
from main_menu import main_menu
from key_bindings import key_bindings
from debris import debris
from debris import rock
from generic_bear import generic_bear
from water_bear import water_bear
from side_bear import side_bear
from evil_koi import evil_koi
from sound import game_music

import math

class game():
    
    def __init__(self):
        """Main running function"""
        self.windowx = 680
        self.windowy = 800
        pygame.init()
        self.clock = pygame.time.Clock()
        self.set_up_screen()
        self.time_since_last_frame = 0.0
        self.enemy_text = open("enemies.txt").readlines()
        self.enemy_data = self.interp_enemies(self.enemy_text)
        self.text_text = open("text_disp.txt").readlines()
        self.text_data = self.interp_text(self.text_text)
        self.text_list = []
        self.debris_list = []
        self.rock_list = []
        self.sbear_list = []
        self.wbear_list = []
        self.boss = None
        self.lives = 3
        self.last_death = 0
        self.immortal_time = 2000
        self.player = player(self.windowx)
        self.distance = 0
        self.worldspeed = 1 #distance per ms for river image movement
        self.riverimg = pygame.image.load("img/river1.png").convert()
        #self.landimgl = pygame.image.load("img/landproxy.png").convert()
        #self.landimgr = pygame.image.load("img/landproxy.png").convert()
        #self.landimgr = pygame.transform.rotate(self.landimgl, 180)
        self.landimgl = pygame.image.load("img/good_grass_left.png").convert_alpha()
        self.landimgr = pygame.image.load("img/good_grass_right.png").convert_alpha()
        self.sidebarimg = pygame.image.load("img/sidebarproxy.png").convert()
        self.heartimg = pygame.image.load("img/heart.png").convert_alpha()
        self.key_bindings = key_bindings()
        self.screen_rect = pygame.Rect(0,0,self.windowx,self.windowy)
        self.player_killed = False
        self.deaddraw = True
        self.deaddrawnum = 0 #a counter to make the player flicker when respawning
        self.font24 = pygame.font.Font(None, 24) #Temp Font
        #final boss stuff
        #self.bad_koi = evil_koi(self.windowx)
        self.bad_projectiles = []
        self.music = game_music()

    def interp_enemies(self, enemy_txt):
        """translate enemies.txt input into a list of lists"""
        new_data = []
        for entry in enemy_txt:
            someline = entry.split(',')
            new_data.append([int(someline[0]), someline[1], int(someline[2]), int(someline[3])]) #2D Array!
        return new_data
        
    def interp_text(self, text_txt):
        """translate text_disp.txt input into a list of lists"""
        new_data = []
        for entry in text_txt:
            someline = entry.split(',')
            new_data.append([int(someline[0]), someline[1], int(someline[2])]) #2D Array!
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
        barrect = self.sidebarimg.get_rect()
        ydisp = (self.distance/2)%riverrect.height
        ydisp2 = (self.distance/4)%riverrect.height
        self.screen.blit(self.riverimg, pygame.Rect(100, ydisp, self.windowx, self.windowy))
        self.screen.blit(self.riverimg, pygame.Rect(100, ydisp - riverrect.height, self.windowx, self.windowy))
        self.screen.blit(self.landimgl, pygame.Rect(0, ydisp2, landrectl.width, landrectl.height))
        self.screen.blit(self.landimgl, pygame.Rect(0, ydisp2 - landrectl.height, landrectl.width, landrectl.height))
        self.screen.blit(self.landimgr, pygame.Rect(self.windowx - 80 - landrectr.width, ydisp2, landrectr.width, landrectr.height))
        self.screen.blit(self.landimgr, pygame.Rect(self.windowx - 80 - landrectr.width, ydisp2 - landrectr.height, landrectr.width, landrectr.height))
        #Have to draw side bears before side bar to cut overlap, sorry for messing up your code
        for e in self.sbear_list:
            e.draw(self.screen)
        #Sidebar Stuff
        self.screen.blit(self.sidebarimg, pygame.Rect(self.windowx - 80, 0, barrect.width, barrect.height))
        #Lives
        for i in range(self.lives):
            self.screen.blit(self.heartimg, pygame.Rect(self.windowx - 80 + 8+24*i, self.windowy - 20, 16, 16))
        energynum = self.font24.render("E: %i"%self.player.energy, 1, (255,0,255), (255,255,0))
        energyrect = energynum.get_rect()
        energyrect.center = (self.windowx-40, self.windowy-80)
        self.screen.blit(energynum, energyrect)
        distnum = self.font24.render("D: %i"%self.distance, 1, (255,0,255), (255,255,0))
        distrect = distnum.get_rect()
        distrect.center = (self.windowx-40, self.windowy-120)
        self.screen.blit(distnum, distrect)
        #Player
        if self.distance > self.last_death + self.immortal_time or self.deaddraw:
            self.player.draw(self.screen)
        self.deaddrawnum += 1
        if self.deaddrawnum > 10:
            self.deaddrawnum = 0
            self.deaddraw = not(self.deaddraw)
        #Enemy Draws:
        for e in self.debris_list:
            e.draw(self.screen)
        for e in self.rock_list:
            e.draw(self.screen)
        for e in self.wbear_list:
            e.draw(self.screen)
        if self.boss != None:
            self.boss.draw(self.screen)
        #Text Engine
        for txt in self.text_list:
            txtsurf = self.font24.render("%s"%txt[0], 1, (255,0,255), (255,255,0))
            txtrect = txtsurf.get_rect()
            txtrect.center = (300, self.windowy-40)
            self.screen.blit(txtsurf, txtrect)
        
    def update(self):
        """Update every frame"""
        self.distance += self.time_since_last_frame * self.worldspeed
        projectiles = self.player.update(self.time_since_last_frame)
        #If player is dead, deal with lives
        if self.player_killed == True:
            if self.distance > self.last_death + self.immortal_time:
                self.last_death = self.distance
                self.lives -= 1
                self.player_killed = False
                if self.lives < 0:
                    txtsurf = self.font24.render("GAME OVER", 1, (255,0,255), (255,255,0))
                    txtrect = txtsurf.get_rect()
                    txtrect.center = (300, self.windowy/2)
                    self.screen.blit(txtsurf, txtrect)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    self.exit_game()
            else:
                self.player_killed = False
        #After updating the player, let's deal with enemies
        #1. Check for enemies we need to add
        for enemy in self.enemy_data:
            if self.distance > enemy[0]:
                #Create the enemy, add it to self.enemies
                #print "It's been %i ms, time to spawn an enemy!"%self.distance
                if enemy[1] == "debris":
                    rdyenemy = debris(enemy[2],-math.pi/2)
                    self.debris_list.append(rdyenemy)
                elif enemy[1] == "rock":
                    rdyenemy = rock(enemy[2],-math.pi/2)
                    self.rock_list.append(rdyenemy)
                elif enemy[1] == "side_bear":
                    rdyenemy = side_bear(self.player,enemy[2],enemy[3])
                    self.sbear_list.append(rdyenemy)
                elif enemy[1] == "water_bear":
                    rdyenemy = water_bear(self.player,enemy[2],enemy[3])
                    self.wbear_list.append(rdyenemy)
                elif enemy[1] == "evil_koi":
                    self.boss = evil_koi(self.windowx)
                else:
                    print "INVALID ENEMY!"
                    self.exit_game()
                #Remove from data
                self.enemy_data.remove(enemy)
        #2. Update Enemies
        for en in self.debris_list:
            en.update(self.time_since_last_frame)
        for rc in self.rock_list:
            rc.update(self.time_since_last_frame)
        for sbr in self.sbear_list:
            sbr.update(self.time_since_last_frame)
        for wbr in self.wbear_list:
            wbr.update(self.time_since_last_frame)
        if self.boss != None:
            self.bad_projectiles = self.boss.update(self.time_since_last_frame)
        #3. Remove Enemies that are off screen
        for en in self.debris_list:
            if not(self.screen_rect.colliderect(en.rect)):
                self.debris_list.remove(en)
        for rc in self.rock_list:
            if not(self.screen_rect.colliderect(rc.rect)):
                self.rock_list.remove(rc)
        for sbr in self.sbear_list:
            if not(self.screen_rect.colliderect(sbr.rect)):
                self.sbear_list.remove(sbr)
        for wbr in self.wbear_list:
            if not(self.screen_rect.colliderect(wbr.rect)):
                self.wbear_list.remove(wbr)
        #Text Engine
        #1. Look for adding texts
        for txt in self.text_data:
            if self.distance > txt[0]:
                #Add the text into our list
                self.text_list.append([txt[1], txt[0] + txt[2]])
                self.text_data.remove(txt)
        #2. Display the texts (SEE DRAW)
        #3. Remove Out of date texts
        for i, txt in enumerate(self.text_list):
            if self.distance > txt[1]:
                #print "removing %s at time %i"%(txt[0], txt[1])
                self.text_list.pop(i)
        #COLLISION
        self.handle_collision(projectiles)
    
    def handle_collision(self, projectiles):
        #check to see if bullets hit anything
        for bullet in projectiles:
            for i, trash in enumerate(self.debris_list):
                if bullet.rect.colliderect(trash.rect):
                    if bullet.type == "fireball":
                        self.debris_list.pop(i)
                    else:
                        trash.displace(bullet.rect)
            for k, rock in enumerate(self.rock_list):
                if bullet.rect.colliderect(rock.rect) and bullet.type == "fireball":
                    self.rock_list.pop(k)
            for j, wbear in enumerate(self.wbear_list):
                if bullet.rect.colliderect(wbear.rect) and bullet.type == "fireball":
                    self.wbear_list.pop(j)
            if self.boss != None and bullet.rect.colliderect(self.boss.rect):
                self.boss.take_damage()
        

        #do player collision
        for i, trash in enumerate(self.debris_list):
            if self.player.rect.colliderect(trash.rect):
                self.player_killed = True
                self.debris_list.pop(i)
            #have debris collide with other debris
            for log in self.debris_list:
                if log.rect.colliderect(trash.rect) and not log.collided:
                    log.angle = -log.angle
                    log.spinning = -log.spinning
                    trash.angle = -trash.angle
                    trash.spinning = -trash.spinning
                    log.collided = True
                    trash.collided = True
        for k, rock in enumerate(self.rock_list):
            if self.player.rect.colliderect(rock.rect):
                self.player_killed = True
                self.rock_list.pop(k)
        for j, wbear in enumerate(self.wbear_list):
            if wbear.state != wbear.GOING_HOME and self.player.rect.colliderect(wbear.rect) and self.player.barrel_lock==False:
                self.player_killed = True
                wbear.force_going_home()
        for j, sbear in enumerate(self.sbear_list):
            if sbear.paw_rect is not None and self.player.rect.colliderect(sbear.paw_rect) and self.player.barrel_lock==False:
                self.player_killed = True
        for x, bullet in enumerate(self.bad_projectiles):
            if bullet.rect.colliderect(self.player.rect):
                self.player_killed = True
        if self.boss != None and self.boss.rect.colliderect(self.player.rect):
            self.player_killed = True

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
                if event.key in self.key_bindings.up:
                    self.player.moving[0] = True
                if event.key in self.key_bindings.down:
                    self.player.moving[1] = True
                if event.key in self.key_bindings.left:
                    self.player.moving[2] = True
                if event.key in self.key_bindings.right:
                    self.player.moving[3] = True
				#abilities
                if event.key in self.key_bindings.barrel_left:
                    self.player.barrel[0] = True
                if event.key in self.key_bindings.barrel_right:
                    self.player.barrel[1] = True
                if event.key in self.key_bindings.shoot:
                    self.player.shoot = True
                if event.key in self.key_bindings.dragon:
                    self.player.dragon = True
            if event.type == pygame.KEYUP:
				#cancelling movement
                if event.key in self.key_bindings.up:
                    self.player.moving[0] = False
                if event.key in self.key_bindings.down:
                    self.player.moving[1] = False
                if event.key in self.key_bindings.left:
                    self.player.moving[2] = False
                if event.key in self.key_bindings.right:
                    self.player.moving[3] = False
				#cancelling abilities
                if event.key in self.key_bindings.barrel_left:
                    self.player.barrel[0] = True
                if event.key in self.key_bindings.barrel_right:
                    self.player.barrel[1] = True
                if event.key in self.key_bindings.shoot:
                    self.player.shoot = False

    def activate_menu(self):
        m = main_menu(self)
        m.run(self.screen)
                    
    def exit_game(self):
        """Exit the game"""
        pygame.quit()
        sys.exit()
 
