import pygame
from pygame.locals import *
import os

# local imports
import Board
import King
import Queen
import Bishop
import Rook
import Pawn
import Knight
import time

# setting up pygame
pygame.init()

# seting up the screen, clock, and font
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
# naming the game
pygame.display.set_caption("Chess")

# getting the size of the screen
screenWidth = screen.get_width()
screenHeight = screen.get_height()

# loading images
def create_image(name):
    fullname = os.path.join('chessPieces', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    image.set_colorkey(image.get_at((0,0)), RLEACCEL)
    return image, image.get_rect()

# getting the size of the box
boxWidth = screenWidth // 8
boxHeight = screenHeight // 8

# loading the board
board = Board.board(screen, boxWidth, boxHeight, (133, 87, 35, 0), (245, 245, 220, 0))

# setting up the king piece for white
# kingImage, kingRect = load_image("BK.png", -1)
kingImage, kingRect = create_image("BK.png")
blackKing = King.king(screen, board, kingImage, kingRect, 0, 4, "B")

kingImage, kingRect = create_image("WK.png")
whiteKing = King.king(screen, board, kingImage, kingRect, 7, 4, "W")

queenImage, queenRect = create_image("BQ.png")
rookImage, rookRect = create_image("WR.png")
knightImage, knightRect = create_image("WN.png")
bishopImage, bishopRect = create_image("WB.png")
# emptyImage, emptyRect = load_image("Empty.png", -1)

# testing the different move capabilities
# king.moveRight()

whitePieces = [whiteKing]
blackPieces = [blackKing]

def setUpPieces(colour, evilKing, pieces, baseRow, pawnRow):
    for p in range(8):
        pawnImage, pawnRect = create_image(colour + "P.png")
        rookImage, rookRect = create_image(colour + "R.png")
        knightImage, knightRect = create_image(colour + "N.png")
        bishopImage, bishopRect = create_image(colour + "B.png")
        queenImage, queenRect = create_image(colour + "Q.png")
        pawn = Pawn.pawn(screen, board, pawnImage, pawnRect, pawnRow, p, colour, queenImage, rookImage, bishopImage, knightImage, evilKing)
        pieces.append(pawn)

    rookImage, rookRect = create_image(colour + "R.png")
    rook = Rook.rook(screen, board, rookImage, rookRect, baseRow, 0, colour)
    pieces.append(rook)
    rookImage, rookRect = create_image(colour + "R.png")
    rook1 = Rook.rook(screen, board, rookImage, rookRect, baseRow, 7, colour)
    pieces.append(rook1)

    knightImage, knightRect = create_image(colour + "N.png")
    knight = Knight.knight(screen, board, knightImage, knightRect, baseRow, 1, colour)
    pieces.append(knight)
    knightImage, knightRect = create_image(colour + "N.png")
    knight1 = Knight.knight(screen, board, knightImage, knightRect, baseRow, 6, colour)
    pieces.append(knight1)

    bishopImage, bishopRect = create_image(colour + "B.png")
    bishop = Bishop.bishop(screen, board, bishopImage, bishopRect, baseRow, 2, colour)
    pieces.append(bishop)
    bishopImage, bishopRect = create_image(colour + "B.png")
    bishop1 = Bishop.bishop(screen, board, bishopImage, bishopRect, baseRow, 5, colour)
    pieces.append(bishop1)

    queenImage, queenRect = create_image(colour + "Q.png")
    queen = Queen.queen(screen, board, queenImage, queenRect, baseRow, 3, colour)
    pieces.append(queen)


setUpPieces("W", blackKing, whitePieces, 7, 6)
setUpPieces("B", whiteKing, blackPieces, 0, 1)

for piece in whitePieces:
    piece.setEnemyPieces(blackPieces)
    piece.setSidePieces(whitePieces)
for piece in blackPieces:
    piece.setEnemyPieces(whitePieces)
    piece.setSidePieces(blackPieces)

move = 0

def dragPiece(piece, pieces, opposingKing, king=False,):
    global move
    if (pygame.mouse.get_pressed()[0]):
        mouseX, mouseY = pygame.mouse.get_pos()
        if (piece.getRect().collidepoint(mouseX, mouseY)):
            piece.dragMove(king) 
            return True
    else:
        confirm = piece.confirmDragMove(move)
        move = confirm[1]
        if (confirm[0]):
            pieceCheck = pieces[0].kingCheck()
            if (not pieceCheck[0]):
                # pieces[0].setImage(pieces[0].originalImage)
                pieces[0].image.set_alpha(255)

            print("Move")
            piece.hasMove = True
            check = opposingKing.kingCheck()
            # print(check)
            if (check[0]):
                # print("Check")
                # print(checkImage)
                opposingKing.image.set_alpha(100)
                # print(opposingKing.image)
                if (opposingKing.kingCheckMate(check[1])):
                    print("Game Over!")
            else:
                opposingKing.image.set_alpha(255)
                stale = opposingKing.kingStaleMate()
                if (stale):
                    print("Stale mate!!!")
        return False
    
def playBoard(pieces, piecePlay, kingLabel, theKing, evilKing):
    for piece in pieces:
        if (piecePlay == None):
            if (piece != theKing):
                dragPiece(piece, pieces, evilKing)
                kingLabel = False
            else:
                dragPiece(piece, pieces, evilKing, king=True)
                kingLabel = True
            piecePlay = piece
        if (not dragPiece(piecePlay, pieces, evilKing, kingLabel)):
                # print("Nah")
                piecePlay = None
                kingLabel = False
    return piecePlay, kingLabel

# setting up sprites
allsprites = whiteKing.render()

whitePiece = None
whiteKingLabel = False

blackPiece = None
blackKingLabel = False

play = True
while play:
    # setting the frame rate of the game
    clock.tick(60)
    # draw the board
    allCenters = board.drawBoard()

    for event in pygame.event.get():
        if (event.type == QUIT):
            play = False

    # dragging the pieces to move them
    if (move % 2 == 0):
        # print("White move")
        whitePiece, whiteKingLabel = playBoard(whitePieces, whitePiece, whiteKingLabel, whiteKing, blackKing)
    else: 
        # print("Black move")
        blackPiece, blackKingLabel = playBoard(blackPieces, blackPiece, blackKingLabel, blackKing, whiteKing)
    allsprites = whiteKing.render()

    # updating the sprites
    allsprites.update()

    # updating the screen
    allsprites.draw(screen)
    pygame.display.flip()
