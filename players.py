import pieces

import pygame


class Move:
    def __init__(self, piece, target, board):
        self.piece = piece
        self.target = target
        self.board = board
        self.executable = True

        if not self.piece or not self.target:
            print('Move arguments not valid!')
            print('Piece:', self.piece)
            print('Target', self.target)
            self.executable = False

        if not self.isValid():
            self.executable = False

    def __str__(self):
        return self.piece.getLetter() + str(self.piece.getSquare()) + str(self.target)

    def isValid(self):
        if self.piece.isValid(self.target, self.board):
            return True
        return False

    def checkSpecialMoves(self):
        # En Passant
        if isinstance(self.piece, pieces.Pawn):
            x, y = pieces.distance(self.target, self.piece.getSquare())
            if abs(y) == 2:
                self.piece.setEnPassant()
            if abs(x) == abs(y):
                self.board.getPieceAt((self.piece.getSquare()[0] + x, self.piece.getSquare()[1])).setTaken()

        # Castling
        if isinstance(self.piece, pieces.King):
            x, y = pieces.distance(self.target, self.piece.getSquare())
            if y == 0:
                if x == 2:
                    rookSquare = (self.piece.getSquare()[0] + 3, self.piece.getSquare()[1])
                    targetSquare = (self.piece.getSquare()[0] + 1, self.piece.getSquare()[1])
                    rook = self.board.getPieceAt(rookSquare)
                    if rook:
                        rook.setSquare(targetSquare)
                        rook.setMoved()
                elif x == -2:
                    rookSquare = (self.piece.getSquare()[0] - 4, self.piece.getSquare()[1])
                    targetSquare = (self.piece.getSquare()[0] - 1, self.piece.getSquare()[1])
                    rook = self.board.getPieceAt(rookSquare)
                    if rook:
                        rook.setSquare(targetSquare)
                        rook.setMoved()

    def execute(self):
        if self.executable:
            print('Move:', self)
            targetPiece = self.board.getPieceAt(self.target)
            if targetPiece:
                targetPiece.setTaken()

            self.checkSpecialMoves()
            self.piece.setSquare(self.target)
            self.piece.setMoved()
            self.executable = False


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

            if move and move.executable:
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

            return Move(piece, target, game.board)
