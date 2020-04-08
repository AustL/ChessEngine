from resources import *
import players

import pygame


class Piece:
    def __init__(self, square, colour):
        self.square = square
        self.colour = colour
        self.image = None
        self.alive = True
        self.moving = False
        self.hasMoved = False
        self.letter = '_'
        self.canBeEnPassant = False

    def isWhite(self):
        return self.colour == WHITE

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

    def isMoving(self):
        return self.moving

    def setMoving(self):
        self.moving = True

    def stopMoving(self):
        self.moving = False

    def getMoved(self):
        return self.hasMoved

    def setMoved(self):
        self.hasMoved = True

    def setEnPassant(self):
        self.canBeEnPassant = True

    def removeEnPassant(self):
        self.canBeEnPassant = False

    def getEnPassant(self):
        return self.canBeEnPassant

    def sameColourAt(self, square, board):
        piece = board.getPieceAt(square)
        if piece and piece.getColour() == self.colour:
            return True

        return False

    @staticmethod
    def withinBounds(square):
        x, y = square
        return 0 <= x <= 7 and 0 <= y <= 7

    def moveThroughPieces(self, square, board):
        x, y = square
        xDirection = x - self.square[0]
        yDirection = y - self.square[1]

        if xDirection != 0:
            xDirection //= abs(xDirection)
        else:
            xDirection = 0

        if yDirection != 0:
            yDirection //= abs(yDirection)
        else:
            yDirection = 0

        tempX, tempY = self.square
        tempX += xDirection
        tempY += yDirection
        while tempX != x or tempY != y:
            if board.getPieceAt((tempX, tempY)) is not None:
                return True
            tempX += xDirection
            tempY += yDirection

        return False

    def isValid(self, square, board):
        if self.sameColourAt(square, board):
            return False
        return True

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

        if self.isWhite():
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
                x = self.square[0] + i
                y = self.square[1] + i
                if self.withinBounds((x, y)):
                    if i != 0 or j != 0:
                        if not self.sameColourAt((x, y), board):
                            moves.append(players.Move(self, (x, y), board))


class Queen(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'Q'

        if self.isWhite():
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

        # Horizontal
        if x == 0 or y == 0:
            if self.moveThroughPieces(square, board):
                return False
            return True

        # Diagonal
        if abs(x) == abs(y):
            if self.moveThroughPieces(square, board):
                return False
            return True

        return False


class Rook(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'R'

        if self.isWhite():
            self.image = W_ROOK
        else:
            self.image = B_ROOK

    def clone(self):
        clone = Rook(self.square, self.colour)
        clone.alive = self.alive
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square):
            return False

        x, y = distance(square, self.square)

        if x == y == 0:
            return False

        # Horizontal
        if x == 0 or y == 0:
            if self.moveThroughPieces(square, board):
                return False
            return True

        return False


class Knight(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'N'

        if self.isWhite():
            self.image = W_KNIGHT
        else:
            self.image = B_KNIGHT

    def clone(self):
        clone = Rook(self.square, self.colour)
        clone.alive = self.alive
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square):
            return False

        x, y = distance(square, self.square)

        if x == y == 0:
            return False

        # L-Shaped Moves
        if (abs(x) == 1 and abs(y) == 2) or (abs(x) == 2 and abs(y) == 1):
            return True
        return False


class Bishop(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'B'

        if self.isWhite():
            self.image = W_BISHOP
        else:
            self.image = B_BISHOP

    def clone(self):
        clone = Bishop(self.square, self.colour)
        clone.alive = self.alive
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square):
            return False

        x, y = distance(square, self.square)

        if x == y == 0:
            return False

        # Diagonal
        if abs(x) == abs(y):
            if self.moveThroughPieces(square, board):
                return False
            return True

        return False


class Pawn(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'P'

        if self.isWhite():
            self.image = W_PAWN
        else:
            self.image = B_PAWN

    def clone(self):
        clone = Pawn(self.square, self.colour)
        clone.alive = self.alive
        clone.canBeEnPassant = self.canBeEnPassant
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square):
            return False

        x, y = distance(square, self.square)

        if x == y == 0:
            return False

        # Diagonal Attacking
        if abs(x) == abs(y) == 1:
            attacking = board.getPieceAt(square)
            if attacking:
                if (self.isWhite() and y == -1) or (not self.isWhite() and y == 1):
                    return True
            else:
                adjacent = (self.square[0] + x, self.square[1])
                adjacentPiece = board.getPieceAt(adjacent)
                if adjacentPiece and adjacentPiece.getEnPassant() and not self.sameColourAt(adjacent, board):
                    return True
            return False

        # Forward
        if x == 0:
            # Single Move
            if (self.isWhite() and y == -1) or (not self.isWhite() and y == 1):
                return True

            # Double Move
            if ((self.isWhite() and y == -2) or (not self.isWhite() and y == 2)) and not self.hasMoved:
                if self.moveThroughPieces(square, board):
                    return False
                return True

            return False


def distance(start, end):
    x1, y1 = start
    x2, y2 = end

    return x1 - x2, y1 - y2
