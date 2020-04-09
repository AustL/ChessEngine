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
        self.black = players.Computer(BLACK, 3)
        self.history = deque()

    def run(self):
        result = None

        run = True
        while run:
            self.history.append(self.board.clone())
            self.white.listen(win, self)

            result = self.board.isDone(WHITE)
            if result:
                break

            self.history.append(self.board.clone())
            self.black.listen(win, self)

            result = self.board.isDone(BLACK)
            if result:
                break

        print(result)

    def undo(self):
        if len(self.history) > 1:
            self.board = self.history.pop()
            self.board = self.history.pop()
            return True

        return False


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    win = pygame.display.set_mode((880, 880))

    game = Game()
    game.run()
