from resources import *
import movement

from abc import abstractmethod, ABC

# Taken from sunfish
PIECE_VALUES = {'P': 100, 'N': 280, 'B': 320, 'R': 479, 'Q': 929, 'K': 60000}
PIECE_SQUARE_TABLE = {
    'P': (
        100, 100, 100, 100, 100, 100, 100, 100,
        178, 183, 186, 173, 202, 182, 185, 190,
        107, 129, 121, 144, 140, 131, 144, 107,
        83, 116, 98, 115, 114, 100, 115, 87,
        74, 103, 110, 109, 106, 101, 100, 77,
        78, 109, 105, 89, 90, 98, 103, 81,
        69, 108, 93, 63, 64, 86, 103, 69,
        100, 100, 100, 100, 100, 100, 100, 100
    ),
    'N': (
        214, 227, 205, 205, 270, 225, 222, 210,
        277, 274, 380, 244, 284, 342, 276, 266,
        290, 347, 281, 354, 353, 307, 342, 278,
        304, 304, 325, 317, 313, 321, 305, 297,
        279, 285, 311, 301, 302, 315, 282, 280,
        262, 290, 293, 302, 298, 295, 291, 266,
        257, 265, 282, 280, 282, 280, 257, 260,
        206, 257, 254, 256, 261, 245, 258, 211
    ),
    'B': (
        261, 242, 238, 244, 297, 213, 283, 270,
        309, 340, 355, 278, 281, 351, 322, 298,
        311, 359, 288, 361, 372, 310, 348, 306,
        345, 337, 340, 354, 346, 345, 335, 330,
        333, 330, 337, 343, 337, 336, 320, 327,
        334, 345, 344, 335, 328, 345, 340, 335,
        339, 340, 331, 326, 327, 326, 340, 336,
        313, 322, 305, 308, 306, 305, 310, 310
    ),
    'R': (
        514, 508, 512, 483, 516, 512, 535, 529,
        534, 508, 535, 546, 534, 541, 513, 539,
        498, 514, 507, 512, 524, 506, 504, 494,
        479, 484, 495, 492, 497, 475, 470, 473,
        451, 444, 463, 458, 466, 450, 433, 449,
        437, 451, 437, 454, 454, 444, 453, 433,
        426, 441, 448, 453, 450, 436, 435, 426,
        449, 455, 461, 484, 477, 461, 448, 447
    ),
    'Q': (
        935, 930, 921, 825, 998, 953, 1017, 955,
        943, 961, 989, 919, 949, 1005, 986, 953,
        927, 972, 961, 989, 1001, 992, 972, 931,
        930, 913, 951, 946, 954, 949, 916, 923,
        915, 914, 927, 924, 928, 919, 909, 907,
        899, 923, 916, 918, 913, 918, 913, 902,
        893, 911, 929, 910, 914, 914, 908, 891,
        890, 899, 898, 916, 898, 893, 895, 887
    ),
    'K': (
        60004, 60054, 60047, 59901, 59901, 60060, 60083, 59938,
        59968, 60010, 60055, 60056, 60056, 60055, 60010, 60003,
        59938, 60012, 59943, 60044, 59933, 60028, 60037, 59969,
        59945, 60050, 60011, 59996, 59981, 60013, 60000, 59951,
        59945, 59957, 59948, 59972, 59949, 59953, 59992, 59950,
        59953, 59958, 59957, 59921, 59936, 59968, 59971, 59968,
        59996, 60003, 59986, 59950, 59943, 59982, 60013, 60004,
        60017, 60030, 59997, 59986, 60006, 59999, 60040, 60018
    )
}


class Piece(ABC):
    def __init__(self, square, colour):
        self.square = square
        self.colour = colour
        self.alive = True
        self.moving = False
        self.hasMoved = False
        self.letter = '_'
        self.canBeEnPassant = False

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
        if self.isWhite():
            value = PIECE_SQUARE_TABLE[self.letter][self.square[1] * 8 + self.square[0]]
        else:
            value = PIECE_SQUARE_TABLE[self.letter][(7 - self.square[1]) * 8 + self.square[0]]

        if self.isAlive():
            return value

        return -PIECE_VALUES[self.letter]

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

    @abstractmethod
    def display(self, win):
        pass

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

    def display(self, win):
        if self.alive:
            if self.isWhite():
                image = PIECES[0]
            else:
                image = PIECES[6]

            if not self.moving:
                x, y = self.square
                win.blit(image, (x * 100 + 60, y * 100 + 60))
            else:
                x, y = pygame.mouse.get_pos()
                win.blit(image, (x - 30, y - 20))

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

    def display(self, win):
        if self.alive:
            if self.isWhite():
                image = PIECES[1]
            else:
                image = PIECES[7]

            if not self.moving:
                x, y = self.square
                win.blit(image, (x * 100 + 60, y * 100 + 60))
            else:
                x, y = pygame.mouse.get_pos()
                win.blit(image, (x - 30, y - 20))

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

    def display(self, win):
        if self.alive:
            if self.isWhite():
                image = PIECES[2]
            else:
                image = PIECES[8]

            if not self.moving:
                x, y = self.square
                win.blit(image, (x * 100 + 60, y * 100 + 60))
            else:
                x, y = pygame.mouse.get_pos()
                win.blit(image, (x - 30, y - 20))

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

    def display(self, win):
        if self.alive:
            if self.isWhite():
                image = PIECES[3]
            else:
                image = PIECES[9]

            if not self.moving:
                x, y = self.square
                win.blit(image, (x * 100 + 60, y * 100 + 60))
            else:
                x, y = pygame.mouse.get_pos()
                win.blit(image, (x - 30, y - 20))

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

    def display(self, win):
        if self.alive:
            if self.isWhite():
                image = PIECES[4]
            else:
                image = PIECES[10]

            if not self.moving:
                x, y = self.square
                win.blit(image, (x * 100 + 60, y * 100 + 60))
            else:
                x, y = pygame.mouse.get_pos()
                win.blit(image, (x - 30, y - 20))

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

    def display(self, win):
        if self.alive:
            if self.isWhite():
                image = PIECES[5]
            else:
                image = PIECES[11]

            if not self.moving:
                x, y = self.square
                win.blit(image, (x * 100 + 60, y * 100 + 60))
            else:
                x, y = pygame.mouse.get_pos()
                win.blit(image, (x - 30, y - 20))

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
