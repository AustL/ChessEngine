import board
import players
import widgets
import exceptions
from resources import *

import pygame
import os
from collections import deque
import sys
import multiprocessing


class Game:
    def __init__(self):
        self.board = board.Board()
        self.white = players.Human
        self.black = players.Human
        self.history = deque()
        self.moves = 0
        self.state = self.menu
        self.result = ''
        self.difficulty = 2

        self.menuButtons = [
            widgets.ButtonArray(
                win, 80, 200, 720, 200, (2, 1), topBorder=20, bottomBorder=20,
                leftBorder=100, rightBorder=100, separationThickness=200, borderRadius=20,
                inactiveColours=(WHITE, BLACK), pressedColours=(LIGHT_GREY, GREY),
                images=(HUMAN_ICON, HUMAN_ICON), radii=(20, 20), hoverColours=(LIGHT_GREY, GREY),
                onReleases=(self.selectComputer, self.selectComputer),
                onReleaseParams=((WHITE,), (BLACK,))
            ),
            widgets.ButtonArray(
                win, 80, 500, 720, 100, (4, 1), topBorder=10, bottomBorder=10,
                leftBorder=80, rightBorder=80, separationThickness=80, borderRadius=20,
                texts=('1', '2', '3', '4'), fontSizes=(40, 40, 40, 40), inactiveColours=(RED, GREEN, RED, RED),
                pressedColours=(RED, GREEN, RED, RED), hoverColours=(DARK_RED, DARK_GREEN, DARK_RED, DARK_RED),
                onClicks=(self.selectDifficulty, self.selectDifficulty, self.selectDifficulty, self.selectDifficulty),
                onClickParams=((1,), (2,), (3,), (4,)), radii=(40, 40, 40, 40)
            ),
            widgets.Button(
                win, 30, 700, 820, 150, inactiveColour=ORANGE, hoverColour=DARK_ORANGE,
                onClick=self.startGame, text='Start', font=START, radius=30
            )
        ]

        self.endButtons = [
            widgets.Button(
                win, 30, 700, 820, 150, inactiveColour=ORANGE, hoverColour=DARK_ORANGE,
                pressedColour=DARK_ORANGE, onRelease=self.showMenu, text='Play Again?',
                font=START, radius=30
            )
        ]

    def selectHuman(self, colour):
        if colour == WHITE:
            self.white = players.Human
            button = self.menuButtons[0].getButtons()[0]
            button.setImage(HUMAN_ICON)
            button.setOnRelease(self.selectComputer, (WHITE,))
        else:
            self.black = players.Human
            button = self.menuButtons[0].getButtons()[1]
            button.setImage(HUMAN_ICON)
            button.setOnRelease(self.selectComputer, (BLACK,))

    def selectComputer(self, colour):
        if colour == WHITE:
            self.white = players.Computer
            button = self.menuButtons[0].getButtons()[0]
            button.setImage(COMPUTER_ICON)
            button.setOnRelease(self.selectHuman, (WHITE,))
        else:
            self.black = players.Computer
            button = self.menuButtons[0].getButtons()[1]
            button.setImage(COMPUTER_ICON)
            button.setOnRelease(self.selectHuman, (BLACK,))

    def selectDifficulty(self, difficulty):
        self.difficulty = difficulty

        for i, button in enumerate(self.menuButtons[1].getButtons()):
            if i == self.difficulty - 1:
                button.setInactiveColour(GREEN)
                button.setPressedColour(GREEN)
                button.setHoverColour(DARK_GREEN)
            else:
                button.setInactiveColour(RED)
                button.setPressedColour(RED)
                button.setHoverColour(DARK_RED)

    def startGame(self):
        if self.difficulty == 1:
            initialDepth = 2
            variableDepth = False
            timeout = 3

        elif self.difficulty == 2:
            initialDepth = 2
            variableDepth = True
            timeout = 30

        elif self.difficulty == 3:
            initialDepth = 3
            variableDepth = True
            timeout = 60

        else:
            initialDepth = 4
            variableDepth = True
            timeout = 300

        if self.white == players.Human:
            self.white = self.white(WHITE)
        else:
            self.white = self.white(WHITE, initialDepth, variableDepth, timeout)

        if self.black == players.Human:
            self.black = self.black(BLACK)
        else:
            self.black = self.black(BLACK, initialDepth, variableDepth, timeout)

        raise exceptions.StartGame

    def showMenu(self):
        raise exceptions.ShowMenu

    def play(self):
        run = True
        while run:
            try:
                self.state()
            except exceptions.StartGame:
                self.state = self.run

            except exceptions.EndGame as e:
                self.result = e.result
                self.state = self.end
                self.white = type(self.white)
                self.black = type(self.black)

            except exceptions.ShowMenu:
                self.reset()
                self.state = self.menu

    def menu(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

            win.fill(LIGHT_BROWN)
            for button in self.menuButtons:
                button.listen()
                button.draw()

            pygame.display.update()

    def run(self):
        run = True
        while run:
            self.history.append(self.board.clone())
            self.white.listen(win, self)
            self.moves += 1

            result = self.board.isDone(WHITE)
            if result:
                raise exceptions.EndGame(result)

            self.history.append(self.board.clone())
            self.black.listen(win, self)
            self.moves += 1

            result = self.board.isDone(BLACK)
            if result:
                raise exceptions.EndGame(result)

    def end(self):
        if self.result == 'CHECKMATE-WHITE':
            text = 'White wins!'
        elif self.result == 'CHECKMATE-BLACK':
            text = 'Black wins!'
        elif self.result == 'STALEMATE':
            text = 'Draw by stalemate...'
        elif self.result == 'INSUFFICIENT MATERIAL':
            text = 'Draw by insufficient material...'
        else:
            text = 'This game is broken (:'

        text = RESULT.render(text, True, BLACK)
        textRect = text.get_rect(center=(440, 440))

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

            win.fill(LIGHT_BROWN)

            win.blit(text, textRect)

            for button in self.endButtons:
                button.listen()
                button.draw()

            pygame.display.update()

    def undo(self):
        if len(self.history) > 1:
            self.board = self.history.pop()
            self.board = self.history.pop()
            self.moves -= 2
            return True

        return False

    def reset(self):
        self.history = deque()
        self.moves = 0
        self.board = board.Board()

    def getMoves(self):
        return self.moves


if __name__ == '__main__':
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

    pygame.init()
    win = pygame.display.set_mode((880, 880))
    pygame.display.set_caption('Chess')
    pygame.display.set_icon(CHESS_ICON)

    game = Game()
    game.play()
