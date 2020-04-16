import pygame

pygame.font.init()

# Images
CHESSBOARD = pygame.image.load('images/CHESSBOARD.png')
HUMAN_ICON = pygame.transform.scale(pygame.image.load('images/HUMAN.png'), (150, 150))
COMPUTER_ICON = pygame.transform.scale(pygame.image.load('images/COMPUTER.png'), (120, 120))
CHESS_ICON = pygame.image.load('images/ICON.ico')


PIECES = [
    pygame.image.load('images/W_KING.png'),
    pygame.image.load('images/W_QUEEN.png'),
    pygame.image.load('images/W_ROOK.png'),
    pygame.image.load('images/W_KNIGHT.png'),
    pygame.image.load('images/W_BISHOP.png'),
    pygame.image.load('images/W_PAWN.png'),

    pygame.image.load('images/B_KING.png'),
    pygame.image.load('images/B_QUEEN.png'),
    pygame.image.load('images/B_ROOK.png'),
    pygame.image.load('images/B_KNIGHT.png'),
    pygame.image.load('images/B_BISHOP.png'),
    pygame.image.load('images/B_PAWN.png'),
]

# Fonts
RESULT = pygame.font.SysFont('calibri', 70)
START = pygame.font.SysFont('calibri', 50)

# Sounds
# ...

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
DARK_GREY = (20, 20, 20)
DARK_BROWN = (209, 139, 71)
LIGHT_BROWN = (255, 206, 158)
MEDIUM_BROWN = (157, 96, 62)
GREEN = (89, 150, 62)
DARK_GREEN = (70, 130, 50)
RED = (200, 60, 50)
DARK_RED = (180, 0, 0)
BLUE = (0, 0, 100)
ORANGE = (240, 156, 0)
DARK_ORANGE = (200, 133, 0)
LIGHT_GREEN = (210, 210, 180)
LIGHT_GREY = (220, 220, 220)


def switch(colour):
    if colour == WHITE:
        return BLACK
    else:
        return WHITE
