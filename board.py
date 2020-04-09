import pieces
from resources import *


class Board:
    def __init__(self):
        self.whitePieces = []
        self.blackPieces = []
        self.turn = WHITE
        self.createPieces()

    def __eq__(self, other):
        for piece1, piece2 in zip(self.whitePieces, other.whitePieces):
            if piece1 != piece2:
                return False

        for piece1, piece2 in zip(self.blackPieces, other.blackPieces):
            if piece1 != piece2:
                return False

        return True

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

    def getWhitePieces(self):
        return self.whitePieces

    def getBlackPieces(self):
        return self.blackPieces

    def replacePiece(self, oldPiece, newPiece):
        for i, piece in enumerate(self.whitePieces):
            if piece is oldPiece:
                self.whitePieces[i] = newPiece

        for i, piece in enumerate(self.blackPieces):
            if piece is oldPiece:
                self.blackPieces[i] = newPiece

        del oldPiece

    def isDone(self, colour):
        if self.isCheckmate(colour):
            if colour == WHITE:
                return 'CHECKMATE-WHITE'
            else:
                return 'CHECKMATE-BLACK'

        if self.isStalemate(colour):
            return 'STALEMATE'

        if self.isInsufficientMaterial():
            return 'INSUFFICIENT MATERIAL'

        return False

    def isCheckmate(self, colour):
        # Colour is colour of piece that just moved
        if not self.isInCheck(switch(colour)):
            return False

        if colour == WHITE:
            enemyPieces = self.blackPieces
        else:
            enemyPieces = self.whitePieces

        boards = []
        for piece in enemyPieces:
            boards.extend(piece.generateBoards(self))

        if boards:
            return False

        return True

    def isInsufficientMaterial(self):
        if self.isInsufficientMaterialFor(WHITE) and self.isInsufficientMaterialFor(BLACK):
            return True

        return False

    def isInsufficientMaterialFor(self, colour):
        if colour == WHITE:
            colourPieces = self.whitePieces
        else:
            colourPieces = self.blackPieces

        alivePieces = {}

        for piece in colourPieces:
            if piece.isAlive():
                alivePieces[type(piece)] = alivePieces.get(type(piece), 0) + 1

        if (pieces.Queen not in alivePieces) and (pieces.Rook not in alivePieces) and (pieces.Pawn not in alivePieces):
            # King
            if (pieces.Bishop not in alivePieces) and (pieces.Knight not in alivePieces):
                return True

            # King and up to 2 Knights
            elif (pieces.Bishop not in alivePieces) and alivePieces[pieces.Knight] < 3:
                return True

            # King and Bishop
            elif (pieces.Knight not in alivePieces) and alivePieces[pieces.Bishop] == 1:
                return True

    def isStalemate(self, colour):
        # Colour is side that last moved
        if self.isInCheck(switch(colour)):
            return False

        if colour == WHITE:
            enemyPieces = self.blackPieces
        else:
            enemyPieces = self.whitePieces

        boards = []
        for piece in enemyPieces:
            boards.extend(piece.generateBoards(self))

        if boards:
            return False

        return True

    def isInCheck(self, colour):
        # Colour is side in check
        if colour == WHITE:
            enemyPieces = self.blackPieces
            king = self.whitePieces[8]
        else:
            enemyPieces = self.whitePieces
            king = self.blackPieces[8]

        kingSquare = king.getSquare()
        for piece in enemyPieces:
            if piece.isValid(kingSquare, self):
                return True

        return False

    def generateAllBoards(self, colour):
        # Colour is side whose turn it is to move
        if colour == WHITE:
            colourPieces = self.whitePieces
        else:
            colourPieces = self.blackPieces

        boards = []
        for piece in colourPieces:
            boards.extend(piece.generateBoards(self))

        return boards

    def clone(self):
        cloneWhitePieces = [piece.clone() for piece in self.whitePieces]
        cloneBlackPieces = [piece.clone() for piece in self.blackPieces]
        clone = Board()
        clone.whitePieces = cloneWhitePieces
        clone.blackPieces = cloneBlackPieces
        return clone

    def evaluate(self, colour):
        # Colour is side that is maximising
        score = 0

        # Material
        for piece in self.whitePieces:
            score += piece.getValue()

        for piece in self.blackPieces:
            score -= piece.getValue()

        if colour == WHITE:
            sign = 1
        else:
            sign = -1

        return score * sign
