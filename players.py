import pygame


class Move:
    def __init__(self, piece, target, board):
        self.piece = piece
        self.target = target
        self.board = board
        self.executable = self.isValid()

    def __str__(self):
        return self.piece.getLetter() + str(self.piece.getSquare()) + str(self.target)

    def isValid(self):
        if self.piece.isValid(self.target, self.board):
            return True
        return False

    def execute(self):
        if self.executable:
            targetPiece = self.board.getPieceAt(self.target)
            if targetPiece:
                targetPiece.setTaken()
            self.piece.setSquare(self.target)

            self.executable = False


class Human:
    def __init__(self, colour, board):
        self.colour = colour
        self.board = board
        self.selectedPiece = None

    def listen(self, win):
        run = True
        while run:
            move = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.select(pygame.mouse.get_pos())

                if event.type == pygame.MOUSEBUTTONUP:
                    move = self.deselect(pygame.mouse.get_pos())

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print('Click')

            if move:
                move.execute()
            self.board.display(win)
            pygame.display.update()

    def select(self, location):
        x, y = location
        x = (x - 40) // 100
        y = (y - 40) // 100
        self.selectedPiece = self.board.getPieceAt((x, y))
        if self.selectedPiece:
            self.selectedPiece.setMoving()

    def deselect(self, location):
        x, y = location
        x = (x - 40) // 100
        y = (y - 40) // 100
        piece = self.selectedPiece
        target = (x, y)
        self.selectedPiece.stopMoving()
        self.selectedPiece = None

        return Move(piece, target, self.board)