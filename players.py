import movement
from resources import *

from random import choice
from math import inf
from sys import exit
from multiprocessing import Process, Queue
import time


class Human:
    def __init__(self, colour):
        self.colour = colour
        self.selectedPiece = None

    def listen(self, win, game):
        run = True
        while run:
            move = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.select(pygame.mouse.get_pos(), game)

                if event.type == pygame.MOUSEBUTTONUP:
                    move = self.deselect(pygame.mouse.get_pos(), game)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if game.undo():
                            run = False

            if move:
                if move.executable:
                    move.execute()
                    run = False

            game.board.display(win)
            pygame.display.update()

    def select(self, location, game):
        x, y = location
        x = (x - 40) // 100
        y = (y - 40) // 100
        self.selectedPiece = game.board.getPieceAt((x, y))
        if self.selectedPiece and self.selectedPiece.getColour() == self.colour:
            self.selectedPiece.setMoving()

    def deselect(self, location, game):
        x, y = location
        x = (x - 40) // 100
        y = (y - 40) // 100
        piece = self.selectedPiece
        target = (x, y)
        if self.selectedPiece and self.selectedPiece.getColour() == self.colour:
            self.selectedPiece.stopMoving()
            self.selectedPiece = None

            return movement.Move(piece, target, game.board)


class Computer:
    def __init__(self, colour, maxDepth):
        self.colour = colour
        self.maxDepth = maxDepth
        self.move = Queue()

    def listen(self, win, game):
        self.setVariableDepth(game)

        computer = Process(target=self.maxFunction, args=(game.board, -inf, inf, 0, self.colour))
        computer.start()
        print(f'Thinking ahead {self.maxDepth} moves...')
        start = time.time()

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if game.undo():
                            computer.kill()
                            run = False

            if not self.move.empty():
                game.board = self.move.get()
                print('Moved in {:.2f} seconds'.format(time.time() - start))
                computer.kill()
                run = False

            game.board.display(win)
            pygame.display.update()

    def setVariableDepth(self, game):
        if game.board.isInCheck(self.colour):
            self.maxDepth = 4
        elif game.getMoves() > 40:
            self.maxDepth = 4
        elif game.getMoves() > 20:
            self.maxDepth = 3

    def maxFunction(self, board, alpha, beta, depth, colour):
        # Colour is side to move
        if depth >= self.maxDepth:
            return board.evaluate(self.colour)

        # If position is lost for side to move
        if board.isCheckmate(switch(colour)):
            if self.colour == colour:
                return -1000000 + depth
            else:
                return 1000000 - depth

        boards = board.generateAllBoards(colour)
        bestBoards = []
        bestScore = -inf

        for newBoard in boards:
            score = self.minFunction(newBoard, alpha, beta, depth + 1, switch(colour))
            if score > bestScore:
                bestScore = score
                bestBoards = [newBoard]
            elif depth == 0 and score == bestScore:
                bestBoards.append(newBoard)

            if score > beta:
                break

            alpha = max(alpha, score)

        if depth == 0:
            self.move.put(choice(bestBoards))
            return

        return bestScore

    def minFunction(self, board, alpha, beta, depth, colour):
        # Colour is side to move
        if depth >= self.maxDepth:
            return board.evaluate(self.colour)

        # If position is lost for side to move
        if board.isCheckmate(switch(colour)):
            if self.colour == colour:
                return -1000000 + depth
            else:
                return 1000000 - depth

        boards = board.generateAllBoards(colour)
        worstBoards = []
        worstScore = inf

        for newBoard in boards:
            score = self.maxFunction(newBoard, alpha, beta, depth + 1, switch(colour))
            if score < worstScore:
                worstScore = score
                worstBoards = [newBoard]
            elif depth == 0 and score == worstScore:
                worstBoards.append(newBoard)

            if score < alpha:
                break

            beta = min(alpha, score)

        if depth == 0:
            self.move.put(choice(worstBoards))

        return worstScore

    def setDepth(self, depth):
        self.maxDepth = depth
