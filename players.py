import movement
from resources import *

import pygame
import random


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
                    quit()

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
                    print('Move:', move)
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

    def listen(self, win, game):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            print('Thinking...')
            board = self.maxFunction(game.board, -400, 400, 0, self.colour)
            game.board = board
            run = False

            game.board.display(win)
            pygame.display.update()

    def maxFunction(self, board, alpha, beta, depth, colour):
        # Colour is side to move
        if depth >= self.maxDepth:
            return board.evaluate(self.colour)

        # If position is lost for side to move
        if board.isCheckmate(switch(colour)):
            if self.colour == colour:
                return -200
            else:
                return 200

        boards = board.generateAllBoards(colour)
        bestBoards = []
        bestScore = -300

        for newBoard in boards:
            score = self.minFunction(newBoard, alpha, beta, depth + 1, switch(colour))
            if score > bestScore:
                bestScore = score
                bestBoards = [newBoard]
            elif depth == 0 and score == bestScore:
                bestBoards.append(newBoard)

            if score > beta:
                return bestScore
            alpha = max(alpha, score)

        if depth == 0:
            return random.choice(bestBoards)

        return bestScore

    def minFunction(self, board, alpha, beta, depth, colour):
        # Colour is side to move
        if depth >= self.maxDepth:
            return board.evaluate(self.colour)

        # If position is lost for side to move
        if board.isCheckmate(switch(colour)):
            if self.colour == colour:
                return -200
            else:
                return 200

        boards = board.generateAllBoards(colour)
        worstBoards = []
        worstScore = 300

        for newBoard in boards:
            score = self.maxFunction(newBoard, alpha, beta, depth + 1, switch(colour))
            if score < worstScore:
                worstScore = score
                worstBoards = [newBoard]
            elif depth == 0 and score == worstScore:
                worstBoards.append(newBoard)

            if score < alpha:
                return worstScore
            beta = min(alpha, score)

        if depth == 0:
            return random.choice(worstBoards)

        return worstScore
