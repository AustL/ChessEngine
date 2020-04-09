import movement

import pygame


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

            if move:
                if move.executable:
                    move.execute()
                    print('Move:', move)
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
            # print('Possible Moves:', self.selectedPiece.generateMoves(game.board))

    def deselect(self, location, game):
        x, y = location
        x = (x - 40) // 100
        y = (y - 40) // 100
        piece = self.selectedPiece
        target = (x, y)
        if self.selectedPiece and self.selectedPiece.getColour() == self.colour:
            self.selectedPiece.stopMoving()
            self.selectedPiece = None

            return movement.Move(piece, target, game.board)
