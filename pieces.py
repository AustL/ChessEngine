from resources import *
import movement

import pygame
from abc import abstractmethod, ABC


class Piece(ABC):
    def __init__(self, square, colour):
        self.square = square
        self.colour = colour
        self.image = None
        self.alive = True
        self.moving = False
        self.hasMoved = False
        self.letter = '_'
        self.canBeEnPassant = False
        self.value = 0

    def __eq__(self, other):
        if self.square == other.square and self.colour == other.colour:
            return True

        return False

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

    def getValue(self):
        if self.alive:
            return self.value
        return 0

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

    @abstractmethod
    def isValid(self, square, board):
        pass

    def display(self, win):
        if self.alive:
            if not self.moving:
                x, y = self.square
                win.blit(self.image, (x * 100 + 60, y * 100 + 60))
            else:
                x, y = pygame.mouse.get_pos()
                win.blit(self.image, (x - 30, y - 20))

    def generateBoards(self, board):
        boards = []
        moves = self.generateMoves(board)
        for target in moves:
            newBoard = board.clone()
            piece = self.clone()
            newBoard.replacePiece(newBoard.getPieceAt(piece.getSquare()), piece)
            move = movement.Move(piece, target, newBoard)
            if move.executable:
                move.execute()
                boards.append(newBoard)

        return boards

    @abstractmethod
    def generateMoves(self, board):
        pass

    @abstractmethod
    def clone(self):
        pass


class King(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'K'

        if self.isWhite():
            self.image = W_KING
        else:
            self.image = B_KING

        self.value = 99

    def clone(self):
        clone = King(self.square, self.colour)
        clone.alive = self.alive
        clone.hasMoved = self.hasMoved
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square) or not self.alive:
            return False

        x, y = distance(square, self.square)

        if x == y == 0:
            return False

        # Move One Square
        if abs(x) <= 1 and abs(y) <= 1:
            return True

        # Castling
        if abs(x) == 2 and y == 0 and not self.hasMoved:
            # Right
            if x == 2:
                rookSquare = (self.square[0] + 3, self.square[1])
                rook = board.getPieceAt(rookSquare)
                if rook and not rook.getMoved():
                    if not self.moveThroughPieces(rookSquare, board) and not self.moveThroughCheck(rookSquare, board):
                        return True

            # Left
            elif x == -2:
                rookSquare = (self.square[0] - 4, self.square[1])
                rook = board.getPieceAt(rookSquare)
                if rook and not rook.getMoved():
                    if not self.moveThroughPieces(rookSquare, board) and not self.moveThroughCheck(rookSquare, board):
                        return True

        return False

    def moveThroughCheck(self, square, board):
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
        while tempX != x or tempY != y:
            if self.isWhite():
                pieces = board.getBlackPieces()
            else:
                pieces = board.getWhitePieces()

            for piece in pieces:
                if piece.isValid((tempX, tempY), board):
                    return True

            tempX += xDirection
            tempY += yDirection

        return False

    def generateMoves(self, board):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.square[0] + i
                y = self.square[1] + j
                if self.withinBounds((x, y)):
                    if i != 0 or j != 0:
                        if not self.sameColourAt((x, y), board):
                            moves.append((x, y))

        # Castling
        for i in (-2, 2):
            x = self.square[0] + i
            y = self.square[1]
            if self.isValid((x, y), board):
                moves.append((x, y))

        return moves


class Queen(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'Q'

        if self.isWhite():
            self.image = W_QUEEN
        else:
            self.image = B_QUEEN

        self.value = 9

    def clone(self):
        clone = Queen(self.square, self.colour)
        clone.alive = self.alive
        clone.hasMoved = self.hasMoved
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square) or not self.alive:
            return False

        x, y = distance(square, self.square)

        if x == y == 0:
            return False

        # Horizontal and Vertical
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

    def generateMoves(self, board):
        moves = []

        # Horizontal
        for i in range(8):
            x = i
            y = self.square[1]
            if x != self.square[0]:
                if not self.sameColourAt((x, y), board):
                    if not self.moveThroughPieces((x, y), board):
                        if self.withinBounds((x, y)):
                            moves.append((x, y))

        # Vertical
        for i in range(8):
            x = self.square[0]
            y = i
            if y != self.square[1]:
                if not self.sameColourAt((x, y), board):
                    if not self.moveThroughPieces((x, y), board):
                        if self.withinBounds((x, y)):
                            moves.append((x, y))

        # Diagonal
        for i in range(8):
            x = i
            y = self.square[1] - (self.square[0] - i)
            if x != self.square[0]:
                if not self.sameColourAt((x, y), board):
                    if not self.moveThroughPieces((x, y), board):
                        if self.withinBounds((x, y)):
                            moves.append((x, y))

        for i in range(8):
            x = self.square[0] + (self.square[1] - i)
            y = i
            if x != self.square[0]:
                if not self.sameColourAt((x, y), board):
                    if not self.moveThroughPieces((x, y), board):
                        if self.withinBounds((x, y)):
                            moves.append((x, y))

        return moves


class Rook(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'R'

        if self.isWhite():
            self.image = W_ROOK
        else:
            self.image = B_ROOK

        self.value = 5

    def clone(self):
        clone = Rook(self.square, self.colour)
        clone.alive = self.alive
        clone.hasMoved = self.hasMoved
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square) or not self.alive:
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

    def generateMoves(self, board):
        moves = []

        # Horizontal
        for i in range(8):
            x = i
            y = self.square[1]
            if x != self.square[0]:
                if not self.sameColourAt((x, y), board):
                    if not self.moveThroughPieces((x, y), board):
                        if self.withinBounds((x, y)):
                            moves.append((x, y))

        # Vertical
        for i in range(8):
            x = self.square[0]
            y = i
            if y != self.square[1]:
                if not self.sameColourAt((x, y), board):
                    if not self.moveThroughPieces((x, y), board):
                        if self.withinBounds((x, y)):
                            moves.append((x, y))

        return moves


class Knight(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'N'

        if self.isWhite():
            self.image = W_KNIGHT
        else:
            self.image = B_KNIGHT

        self.value = 3

    def clone(self):
        clone = Knight(self.square, self.colour)
        clone.alive = self.alive
        clone.hasMoved = self.hasMoved
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square) or not self.alive:
            return False

        x, y = distance(square, self.square)

        if x == y == 0:
            return False

        # L-Shaped Moves
        if (abs(x) == 1 and abs(y) == 2) or (abs(x) == 2 and abs(y) == 1):
            return True
        return False

    def generateMoves(self, board):
        moves = []

        for i, j in ((-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)):
            x = self.square[0] + i
            y = self.square[1] + j
            if self.withinBounds((x, y)):
                if not self.sameColourAt((x, y), board):
                    moves.append((x, y))

        return moves


class Bishop(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'B'

        if self.isWhite():
            self.image = W_BISHOP
        else:
            self.image = B_BISHOP

        self.value = 3

    def clone(self):
        clone = Bishop(self.square, self.colour)
        clone.alive = self.alive
        clone.hasMoved = self.hasMoved
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square) or not self.alive:
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

    def generateMoves(self, board):
        moves = []

        # Diagonal
        for i in range(8):
            x = i
            y = self.square[1] - (self.square[0] - i)
            if x != self.square[0]:
                if not self.sameColourAt((x, y), board):
                    if not self.moveThroughPieces((x, y), board):
                        if self.withinBounds((x, y)):
                            moves.append((x, y))

        for i in range(8):
            x = self.square[0] + (self.square[1] - i)
            y = i
            if x != self.square[0]:
                if not self.sameColourAt((x, y), board):
                    if not self.moveThroughPieces((x, y), board):
                        if self.withinBounds((x, y)):
                            moves.append((x, y))

        return moves


class Pawn(Piece):
    def __init__(self, square, colour):
        super().__init__(square, colour)
        self.letter = 'P'

        if self.isWhite():
            self.image = W_PAWN
        else:
            self.image = B_PAWN

        self.value = 1

    def clone(self):
        clone = Pawn(self.square, self.colour)
        clone.alive = self.alive
        clone.canBeEnPassant = self.canBeEnPassant
        clone.hasMoved = self.hasMoved
        return clone

    def isValid(self, square, board):
        if self.sameColourAt(square, board) or not self.withinBounds(square) or not self.alive:
            return False

        x, y = distance(square, self.square)

        if x == y == 0:
            return False

        attacking = board.getPieceAt(square)

        # Diagonal Attacking
        if abs(x) == abs(y) == 1:
            if attacking:
                if (self.isWhite() and y == -1) or (not self.isWhite() and y == 1):
                    return True
            else:
                # En Passant
                adjacent = (self.square[0] + x, self.square[1])
                adjacentPiece = board.getPieceAt(adjacent)
                if adjacentPiece and adjacentPiece.getEnPassant() and not self.sameColourAt(adjacent, board):
                    return True
            return False

        # Forward
        if x == 0:
            # Single Move
            if (self.isWhite() and y == -1) or (not self.isWhite() and y == 1):
                if attacking is None:
                    return True
                return False

            # Double Move
            if ((self.isWhite() and y == -2) or (not self.isWhite() and y == 2)) and not self.hasMoved:
                if not self.moveThroughPieces(square, board) and attacking is None:
                    return True
                return False

        return False

    def generateMoves(self, board):
        moves = []

        # Single Move
        for i in range(-1, 2):
            x = self.square[0] + i
            if self.isWhite():
                y = self.square[1] - 1
            else:
                y = self.square[1] + 1

            if abs(i) == 1:
                # Taking Piece
                attacking = board.getPieceAt((x, y))
                if attacking and not self.sameColourAt((x, y), board):
                    moves.append((x, y))
                else:
                    # En Passant
                    adjacent = (x, self.square[1])
                    adjacentPiece = board.getPieceAt(adjacent)
                    if adjacentPiece and adjacentPiece.getEnPassant() and not self.sameColourAt(adjacent, board):
                        moves.append((x, y))

            # Move Forward
            elif i == 0:
                if board.getPieceAt((x, y)) is None and self.withinBounds((x, y)):
                    moves.append((x, y))

        # Double Move
        if not self.hasMoved:
            if self.isWhite():
                y = self.square[1] - 2
            else:
                y = self.square[1] + 2

            x = self.square[0]

            if board.getPieceAt((x, y)) is None and not self.moveThroughPieces((x, y), board):
                moves.append((x, y))

        return moves


def distance(start, end):
    x1, y1 = start
    x2, y2 = end

    return x1 - x2, y1 - y2
