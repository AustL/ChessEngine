import board
import players
import widgets
from resources import *

import pygame
import os
from collections import deque
from sys import exit


class Game:
    def __init__(self):
        self.board = board.Board()
        self.white = players.Human(WHITE)
        self.black = players.Human(BLACK)
        self.history = deque()
        self.moves = 0

        self.menuButtons = [
            widgets.ButtonArray(win, 80, 400, 720, 200, (2, 1), topBorder=20, bottomBorder=20,
                                leftBorder=100, rightBorder=100, separationThickness=200, borderRadius=20,
                                inactiveColours=(WHITE, BLACK), activeColours=(WHITE, BLACK),
                                images=(HUMAN_ICON, HUMAN_ICON), radii=(20, 20), hoverColours=(LIGHT_GREY, GREY),
                                onClicks=(self.selectComputer, self.selectComputer),
                                onClickParams=((WHITE,), (BLACK,)))
        ]

    def selectHuman(self, colour):
        if colour == WHITE:
            self.white = players.Human(WHITE)
            button = self.menuButtons[0].getButtons()[0]
            button.setImage(HUMAN_ICON)
            button.setOnClick(self.selectComputer, (WHITE,))
        else:
            self.black = players.Human(BLACK)
            button = self.menuButtons[0].getButtons()[1]
            button.setImage(HUMAN_ICON)
            button.setOnClick(self.selectComputer, (BLACK,))

    def selectComputer(self, colour):
        if colour == WHITE:
            self.white = players.Computer(WHITE, 2)
            button = self.menuButtons[0].getButtons()[0]
            button.setImage(COMPUTER_ICON)
            button.setOnClick(self.selectHuman, (WHITE,))
        else:
            self.black = players.Computer(BLACK, 2)
            button = self.menuButtons[0].getButtons()[1]
            button.setImage(COMPUTER_ICON)
            button.setOnClick(self.selectHuman, (BLACK,))

    def play(self):
        self.menu()
        self.run()

    def menu(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()

            win.fill(LIGHT_BROWN)
            for button in self.menuButtons:
                button.listen()
                button.draw()

            pygame.display.update()

    def run(self):
        result = None

        run = True
        while run:
            self.history.append(self.board.clone())
            self.white.listen(win, self)
            self.moves += 1

            result = self.board.isDone(WHITE)
            if result:
                break

            self.history.append(self.board.clone())
            self.black.listen(win, self)
            self.moves += 1

            result = self.board.isDone(BLACK)
            if result:
                break

        print(result)

    def undo(self):
        if len(self.history) > 1:
            self.board = self.history.pop()
            self.board = self.history.pop()
            self.moves -= 2
            return True

        return False

    def getMoves(self):
        return self.moves


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

    pygame.init()
    win = pygame.display.set_mode((880, 880))
    pygame.display.set_caption('Chess')

    game = Game()
    game.play()
