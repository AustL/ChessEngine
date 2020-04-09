import pieces


class Move:
    def __init__(self, piece, target, board):
        self.piece = piece
        self.target = target
        self.board = board
        self.testBoard = board.clone()
        self.executable = True

        if not self.piece or not self.target:
            print('Move arguments not valid!')
            print('Piece:', self.piece)
            print('Target', self.target)
            self.executable = False

        if not self.isValid():
            self.executable = False

    def __str__(self):
        return f'{self.piece.getLetter()}: {self.piece.getSquare()} --> {self.target}'

    def isValid(self):
        if self.piece.isValid(self.target, self.board):
            targetPiece = self.testBoard.getPieceAt(self.target)
            if targetPiece:
                targetPiece.setTaken()

            testPiece = self.piece.clone()
            self.testBoard.replacePiece(self.testBoard.getPieceAt(self.piece.getSquare()), testPiece)

            self.checkSpecialMoves(testPiece, self.testBoard)
            testPiece.setSquare(self.target)
            testPiece.setMoved()

            if self.testBoard.isLegalMove(testPiece.getColour()):
                return True
        return False

    def checkSpecialMoves(self, piece, board):
        # Castling
        if isinstance(piece, pieces.King):
            x, y = pieces.distance(self.target, piece.getSquare())
            if y == 0:
                if x == 2:
                    rookSquare = (piece.getSquare()[0] + 3, piece.getSquare()[1])
                    targetSquare = (piece.getSquare()[0] + 1, piece.getSquare()[1])
                    rook = board.getPieceAt(rookSquare)
                    if rook:
                        rook.setSquare(targetSquare)
                        rook.setMoved()
                elif x == -2:
                    rookSquare = (piece.getSquare()[0] - 4, piece.getSquare()[1])
                    targetSquare = (piece.getSquare()[0] - 1, piece.getSquare()[1])
                    rook = board.getPieceAt(rookSquare)
                    if rook:
                        rook.setSquare(targetSquare)
                        rook.setMoved()

        if isinstance(self.piece, pieces.Pawn):
            # En Passant
            x, y = pieces.distance(self.target, self.piece.getSquare())
            if abs(y) == 2:
                self.piece.setEnPassant()
            else:
                self.piece.removeEnPassant()

            adjacentSquare = (self.piece.getSquare()[0] + x, self.piece.getSquare()[1])
            adjacentPiece = self.board.getPieceAt(adjacentSquare)
            if abs(x) == abs(y) == 1 and not self.board.getPieceAt(self.target) and adjacentPiece:
                adjacentPiece.setTaken()

            # Promotion
            x, y = self.target
            if y == 0 or y == 7:
                oldPiece = self.piece
                self.piece = pieces.Queen(oldPiece.getSquare(), oldPiece.getColour())
                self.piece.setMoved()
                self.board.replacePiece(oldPiece, self.piece)

    def execute(self):
        if self.executable:
            targetPiece = self.board.getPieceAt(self.target)
            if targetPiece:
                targetPiece.setTaken()

            self.checkSpecialMoves(self.piece, self.board)
            self.piece.setSquare(self.target)
            self.piece.setMoved()
            self.executable = False
