import pygame.image

# Images
CHESSBOARD = pygame.image.load('images/CHESSBOARD.png')
PLAY = pygame.image.load('images/PLAY.png')

DARK_WOOD = pygame.image.load('images/DARK_WOOD.jpg')
LIGHT_WOOD = pygame.image.load('images/LIGHT_WOOD.jpg')
BORDER_WOOD_H = pygame.image.load('images/BORDER_WOOD.jpg')
BORDER_WOOD_V = pygame.transform.rotate(pygame.image.load('images/BORDER_WOOD.jpg'), 90)

B_KING = pygame.image.load('images/B_KING.png')
B_QUEEN = pygame.image.load('images/B_QUEEN.png')
B_ROOK = pygame.image.load('images/B_ROOK.png')
B_KNIGHT = pygame.image.load('images/B_KNIGHT.png')
B_BISHOP = pygame.image.load('images/B_BISHOP.png')
B_PAWN = pygame.image.load('images/B_PAWN.png')

W_KING = pygame.image.load('images/W_KING.png')
W_QUEEN = pygame.image.load('images/W_QUEEN.png')
W_ROOK = pygame.image.load('images/W_ROOK.png')
W_KNIGHT = pygame.image.load('images/W_KNIGHT.png')
W_BISHOP = pygame.image.load('images/W_BISHOP.png')
W_PAWN = pygame.image.load('images/W_PAWN.png')


# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
DARK_BROWN = (209, 139, 71)
LIGHT_BROWN = (255, 206, 158)
MEDIUM_BROWN = (157, 96, 62)
GREEN = (89, 120, 62)
DARK_GREEN = (60, 80, 40)
RED = (200, 0, 0)
BLUE = (0, 0, 100)
LIGHT_GREY = (210, 210, 180)


def switch(colour):
    if colour == WHITE:
        return BLACK
    else:
        return WHITE

