import board
import players
from resources import *

import pygame
import os
from collections import deque


class Game:
    def __init__(self):
        self.board = board.Board()
        self.white = players.Human(WHITE)
        self.black = players.Human(BLACK)
        self.history = deque()

    def run(self):
        run = True
        while run:
            self.history.append(self.board.clone())
            self.white.listen(win, self)
            self.checkEndGame(WHITE)
            self.history.append(self.board.clone())
            self.black.listen(win, self)
            self.checkEndGame(BLACK)

    def checkEndGame(self, colour):
        if self.board.isCheckmate(colour):
            print('Checkmate!')

        if self.board.isStalemate(colour):
            print('Stalemate!')

        if self.board.isInsufficientMaterial():
            print('Insufficient Material!')

        if self.board.isThreefoldRepetition(self):
            print('Threefold Repetition!')

    def undo(self):
        if len(self.history) > 1:
            self.board = self.history.pop()
            self.board = self.history.pop()
            return True

        return False


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
win = pygame.display.set_mode((880, 880))

game = Game()
game.run()
