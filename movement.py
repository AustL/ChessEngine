import pieces


class Move:
    def __init__(self, piece, target, board):
        self.piece = piece
        self.target = target
        self.board = board
        self.testBoard = board.clone()
        self.executable = True

        if not self.piece or not self.target:
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

            if not self.testBoard.isInCheck(testPiece.getColour()):
                return True
        return False

    def checkSpecialMoves(self, piece, board):
        self.checkCastling(piece, board)
        self.checkEnPassant(piece, board)
        self.checkPromotion(piece, board)

    def checkCastling(self, piece, board):
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

    def checkEnPassant(self, piece, board):
        if isinstance(piece, pieces.Pawn):
            x, y = pieces.distance(self.target, piece.getSquare())
            if abs(y) == 2:
                piece.setEnPassant()
            else:
                piece.removeEnPassant()

            adjacentSquare = (piece.getSquare()[0] + x, piece.getSquare()[1])
            adjacentPiece = board.getPieceAt(adjacentSquare)
            if abs(x) == abs(y) == 1 and not board.getPieceAt(self.target) and adjacentPiece:
                adjacentPiece.setTaken()

    def checkPromotion(self, piece, board):
        if isinstance(piece, pieces.Pawn):
            x, y = self.target
            if y == 0 or y == 7:
                targetPiece = board.getPieceAt(self.target)
                if targetPiece:
                    targetPiece.setTaken()
                oldPiece = piece
                piece = pieces.Queen(self.target, oldPiece.getColour())
                piece.setMoved()
                board.replacePiece(oldPiece, piece)

    def execute(self):
        if self.executable:
            self.checkSpecialMoves(self.piece, self.board)
            targetPiece = self.board.getPieceAt(self.target)
            if targetPiece and targetPiece.getColour() != self.piece.getColour():
                targetPiece.setTaken()
            self.piece.setSquare(self.target)
            self.piece.setMoved()
            self.executable = False
