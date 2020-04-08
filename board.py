import pieces
from resources import *


class Board:
    def __init__(self):
        self.whitePieces = []
        self.blackPieces = []
        self.turn = WHITE
        self.createPieces()

    def display(self, win):
        win.blit(CHESSBOARD, (0, 0))
        hoveringPiece = None

        for piece in self.whitePieces:
            if piece.isMoving():
                hoveringPiece = piece
            piece.display(win)

        for piece in self.blackPieces:
            if piece.isMoving():
                hoveringPiece = piece
            piece.display(win)

        if hoveringPiece:
            hoveringPiece.display(win)

    def createPieces(self):
        whitePieces = {
            (0, 7): pieces.Rook, (0, 6): pieces.Pawn,
            (1, 7): pieces.Knight, (1, 6): pieces.Pawn,
            (2, 7): pieces.Bishop, (2, 6): pieces.Pawn,
            (3, 7): pieces.Queen, (3, 6): pieces.Pawn,
            (4, 7): pieces.King, (4, 6): pieces.Pawn,
            (5, 7): pieces.Bishop, (5, 6): pieces.Pawn,
            (6, 7): pieces.Knight, (6, 6): pieces.Pawn,
            (7, 7): pieces.Rook, (7, 6): pieces.Pawn
        }
        blackPieces = {
            (0, 0): pieces.Rook, (0, 1): pieces.Pawn,
            (1, 0): pieces.Knight, (1, 1): pieces.Pawn,
            (2, 0): pieces.Bishop, (2, 1): pieces.Pawn,
            (3, 0): pieces.Queen, (3, 1): pieces.Pawn,
            (4, 0): pieces.King, (4, 1): pieces.Pawn,
            (5, 0): pieces.Bishop, (5, 1): pieces.Pawn,
            (6, 0): pieces.Knight, (6, 1): pieces.Pawn,
            (7, 0): pieces.Rook, (7, 1): pieces.Pawn
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
