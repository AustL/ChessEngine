from board import *
from players import *

import pygame
import os


class Game:
    def __init__(self):
        self.board = Board()
        self.white = Human(WHITE, self.board)
        self.black = Human(BLACK, self.board)

    def run(self):
        self.white.listen(win)
        self.black.listen(win)


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
win = pygame.display.set_mode((880, 880))

game = Game()
game.run()
