from resources import *
from players import *

import pygame


class Piece:
    def __init__(self, square, colour):
        self.square = square
        self.x, self.y = square
        self.colour = colour
        self.image = None
        self.alive = True
        self.moving = False
        self.letter = '_'

    def getLetter(self):
        return self.letter

    def getSquare(self):
        return self.square

    def setSquare(self, square):
        self.square = square

    def getColour(self):
        return self.colour

    def isAlive(self):
        return self.alive

    def setTaken(self):
        self.alive = False

    def setMoving(self):
        self.moving = True

    def stopMoving(self):
        self.moving = False

    def sameColourAt(self, square, board):
        piece = board.getPieceAt(square)
        if piece and piece.getColour() == self.colour:
            return True

        return False

    @staticmethod
    def withinBounds(square):
        x, y = square
        return 0 <= x <= 7 and 0 <= y <= 7

    def isValid(self, square, board):
        if self.sameColourAt(square, board):
            return False
        return True

    def moveThroughPieces(self, square, board):
        x, y = square
        xDirection = (x - self.x) // abs(x - self.x)
        yDirection = (y - self.y) // abs(y - self.y)

        tempX, tempY = self.square
        while tempX != x or tempY != y:
            tempX += xDirection
            tempY += yDirection
            if board.getPieceAt((tempX, tempY)) is not None:
                return True

        return False

    def display(self, win):
        if self.alive:
            if not self.moving:
                x, y = self.square
                win.blit(self.image, (x * 100 + 60, y * 100 + 60))
            else:
                x, y = pygame.mouse.get_pos()
                win.blit(self.image, (x - 30, y - 20))


class King(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'K'

        if self.colour == WHITE:
            self.image = W_KING
        else:
            self.image = B_KING

    def clone(self):
        clone = King(self.square, self.colour)
        clone.alive = self.alive
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square):
            return False

        x, y = distance(square, self.square)

        if x == y == 0:
            return False

        if abs(x) <= 1 and abs(y) <= 1:
            return True

        return False

    def generateMoves(self, board):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.x + i
                y = self.y + i
                if self.withinBounds((x, y)):
                    if i != 0 or j != 0:
                        if not self.sameColourAt((x, y), board):
                            moves.append(Move(self, (x, y), board))


class Queen(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'Q'

        if self.colour == WHITE:
            self.image = W_QUEEN
        else:
            self.image = B_QUEEN

    def clone(self):
        clone = Queen(self.square, self.colour)
        clone.alive = self.alive
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square):
            return False

        x, y = distance(square, self.square)

        if x == y == 0:
            return False

        if x == 0 or y == 0:
            pass


class Rook(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'R'

        if self.colour == WHITE:
            self.image = W_ROOK
        else:
            self.image = B_ROOK

    def clone(self):
        clone = Rook(self.square, self.colour)
        clone.alive = self.alive
        return clone


class Knight(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'N'

        if self.colour == WHITE:
            self.image = W_KNIGHT
        else:
            self.image = B_KNIGHT

    def clone(self):
        clone = Rook(self.square, self.colour)
        clone.alive = self.alive
        return clone


class Bishop(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'B'

        if self.colour == WHITE:
            self.image = W_BISHOP
        else:
            self.image = B_BISHOP

    def clone(self):
        clone = Bishop(self.square, self.colour)
        clone.alive = self.alive
        return clone


class Pawn(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'P'

        if self.colour == WHITE:
            self.image = W_PAWN
        else:
            self.image = B_PAWN

    def clone(self):
        clone = Pawn(self.square, self.colour)
        clone.alive = self.alive
        return clone


def distance(start, end):
    x1, y1 = start
    x2, y2 = end

    return x1 - x2, y1 - y2
