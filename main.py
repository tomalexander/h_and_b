#!/usr/bin/python2
#

import os, sys
import pygame
from game import game
import player

already_run = False

while True:
    the_game = game()
    the_game.run(already_run)
    already_run = True
