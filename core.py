import pygame
from pygame.locals import *
import sys


def exit_if_user_pressed_quit():
    # Did use press quit
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
