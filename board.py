from pieces import *


class Board:
    def __init__(self):
        self.whitePieces = []
        self.blackPieces = []
        self.turn = WHITE
        self.createPieces()

    def display(self, win):
        win.blit(CHESSBOARD, (0, 0))

        for piece in self.whitePieces:
            piece.display(win)

        for piece in self.blackPieces:
            piece.display(win)

    def createPieces(self):
        whitePieces = {
            (0, 7): Rook, (0, 6): Pawn,
            (1, 7): Knight, (1, 6): Pawn,
            (2, 7): Bishop, (2, 6): Pawn,
            (3, 7): Queen, (3, 6): Pawn,
            (4, 7): King, (4, 6): Pawn,
            (5, 7): Bishop, (5, 6): Pawn,
            (6, 7): Knight, (6, 6): Pawn,
            (7, 7): Rook, (7, 6): Pawn
        }
        blackPieces = {
            (0, 0): Rook, (0, 1): Pawn,
            (1, 0): Knight, (1, 1): Pawn,
            (2, 0): Bishop, (2, 1): Pawn,
            (3, 0): Queen, (3, 1): Pawn,
            (4, 0): King, (4, 1): Pawn,
            (5, 0): Bishop, (5, 1): Pawn,
            (6, 0): Knight, (6, 1): Pawn,
            (7, 0): Rook, (7, 1): Pawn
        }

        for square, piece in whitePieces.items():
            self.whitePieces.append(piece(square, WHITE))

        for square, piece in blackPieces.items():
            self.blackPieces.append(piece(square, BLACK))

    def getPieceAt(self, location):
        for piece in self.whitePieces + self.blackPieces:
            if piece.getSquare() == location and piece.isAlive():
                return piece

        return None

    def clone(self):
        cloneWhitePieces = [piece.clone() for piece in self.whitePieces]
        cloneBlackPieces = [piece.clone() for piece in self.blackPieces]
        clone = Board()
        clone.whitePieces = cloneWhitePieces
        clone.blackPieces = cloneBlackPieces
        return clone
