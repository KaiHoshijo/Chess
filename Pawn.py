import pygame
import King
import Queen
import Rook
import Bishop
import Knight

class pawn(King.king):
    def __init__(self, screen, board, image, rect, row, col, colour, queenImage, rookImage, bishopImage,knightImage, opposingKing):
        super().__init__(screen, board, image, rect, row, col, colour)
        self.firstMove = True
        self.moveTwo = False
        self.queenImage = queenImage
        self.rookImage = rookImage
        self.bishopImage = bishopImage
        self.knightImage = knightImage
        self.opposingKing = opposingKing
        if (colour == "W"):
            self.target = 0
        else:
            self.target = 7

    # move two down
    def moveTwoDown(self, ):
        allMoves = [[self.move(-2, 0), -2, 0]]
        if (self.passPoint(allMoves) != "E"): return [[False, -2, 0]]
        return allMoves

    # move two up
    def moveTwoUp(self, ):
        allMoves = [[self.move(2, 0), 2, 0]]
        if (self.passPoint(allMoves) != "E"): return [[False, 2, 0]]
        return allMoves

    # find available moves
    def findMoves(self, show=True, isKing=False):
        if (self.colour == "W"):
            # return all moves available
            if (show):
                standardMoves = [self.moveDown(["W", "B"])]
            else:
                standardMoves = []
            # move down left if enemy there
            downLeft = self.board.getPosition(self.row-1, self.col-1)
            if (downLeft != None):
                if (downLeft[0] == self.getOppositeColour() or not show):
                    standardMoves.append(self.moveDownLeft())
                if (self.row == 3):
                    for piece in self.enemyPieces:
                        if (piece.getPosition() == (self.row, self.col-1)):
                            try:
                                if (piece.moveTwo):
                                    standardMoves.append(self.moveUpRight())
                            except:
                                continue                

            # move down right if enemy there
            downRight = self.board.getPosition(self.row-1, self.col+1)
            if (downRight != None):
                if (downRight[0] == self.getOppositeColour() or not show):
                    standardMoves.append(self.moveDownRight())
                if (self.row == 3):
                    for piece in self.enemyPieces:
                        if (piece.getPosition() == (self.row, self.col+1)):
                            try:
                                if (piece.moveTwo):
                                    standardMoves.append(self.moveDownRight())
                            except:
                                continue
            
            # move up two if first move
            if (self.firstMove and show):
                standardMoves.append(self.moveTwoDown())
        else:
            if (show):
                standardMoves = [self.moveUp(["W", "B"])]
            else:
                standardMoves = []

            if (self.firstMove and show):
                # move up two if first move
                standardMoves.append(self.moveTwoUp())

            # move up left if enemy there
            upLeft = self.board.getPosition(self.row+1, self.col-1)
            if (upLeft != None):
                if (upLeft[0] == self.getOppositeColour() or not show):
                    standardMoves.append(self.moveUpLeft())
                if (self.row == 4):
                    for piece in self.enemyPieces:
                        if (piece.getPosition() == (self.row, self.col-1)):
                            try:
                                if (piece.moveTwo):
                                    standardMoves.append(self.moveUpLeft())
                            except:
                                continue

            # move up right if enemy there
            upRight = self.board.getPosition(self.row+1, self.col+1)
            if (upRight != None):
                if (upRight[0] == self.getOppositeColour() or not show):
                    standardMoves.append(self.moveUpRight())
                if (self.row == 4):
                    for piece in self.enemyPieces:
                        if (piece.getPosition() == (self.row, self.col+1)):
                            try:
                                if (piece.moveTwo):
                                    standardMoves.append(self.moveUpRight())
                            except:
                                continue
            
        return standardMoves

    # confirm move
    def confirmDragMove(self, move):
        # ensuring that the piece only moves to a desired sport
        currentPosition = self.getPosition()
        if (self.chosenRect != None):
            # check if the mouse is touching still touching the square after the mouse let go
            if (self.rect.colliderect(self.chosenRect)):
                if (self.takePiece(self.chosenPosition)):
                    move = self.increaseMove(move)
                    self.setPosition(self.chosenPosition)

                    if (self.chosenPosition[0] - 2 == currentPosition[0] or self.chosenPosition[0] + 2 == currentPosition[0]):
                        self.moveTwo = True

                    if (self.chosenPosition == (currentPosition[0]+1, currentPosition[1]+1) or self.chosenPosition == (currentPosition[0]+1, currentPosition[1]-1)):
                        for piece in self.enemyPieces:
                            if (piece.getPosition() == (self.chosenPosition[0] - 1, self.chosenPosition[1])):
                                piece.delete()
                            
                    if (self.chosenPosition == (currentPosition[0]-1, currentPosition[1]+1) or self.chosenPosition == (currentPosition[0]-1, currentPosition[1]-1)):
                        for piece in self.enemyPieces:
                            if (piece.getPosition() == (self.chosenPosition[0] + 1, self.chosenPosition[1])):
                                piece.delete()

                    if (self.chosenPosition[0] == self.target):
                        piece = input("Which piece do you want to become? Queen, Rook, Knight, or Bishop: ")
                        while (piece.lower() not in ['queen', 'rook', 'knight', 'bishop']):
                            piece = input("Which piece do you want to become? Queen, Rook, Knight, or Bishop: ")
                        if (piece == 'queen'):
                            sidePieces = self.sidePieces
                            enemyPieces = self.enemyPieces
                            queen = Queen.queen(self.screen, self.board, self.queenImage, self.rect, self.row, self.col, self.colour)
                            queen.setSidePieces(sidePieces)
                            queen.setEnemyPieces(enemyPieces)
                            self.sidePieces.append(queen)
                            self.delete()
                            # print(queen.sidePieces)
                        elif (piece == 'rook'):
                            sidePieces = self.sidePieces
                            enemyPieces = self.enemyPieces
                            rook = Rook.rook(self.screen, self.board, self.rookImage, self.rect, self.row, self.col, self.colour)
                            rook.setSidePieces(self.sidePieces)
                            rook.setEnemyPieces(self.enemyPieces)
                            self.sidePieces.append(rook)
                            self.delete()
                        elif (piece == 'knight'):
                            sidePieces = self.sidePieces
                            enemyPieces = self.enemyPieces
                            knight = Knight.knight(self.screen, self.board, self.knightImage, self.rect, self.row, self.col, self.colour)
                            knight.setSidePieces(self.sidePieces)
                            knight.setEnemyPieces(self.enemyPieces)
                            self.sidePieces.append(knight)
                            self.delete()
                        elif (piece == 'bishop'):
                            sidePieces = self.sidePieces
                            enemyPieces = self.enemyPieces
                            bishop = Bishop.bishop(self.screen, self.board, self.bishopImage, self.rect, self.row, self.col, self.colour)
                            bishop.setSidePieces(self.sidePieces)
                            bishop.setEnemyPieces(self.enemyPieces)
                            self.sidePieces.append(bishop)
                            self.delete()
                    if (self.opposingKing.kingCheck()[0]):
                        self.opposingKing.image.set_alpha(100)
                    self.firstMove = False
            else:
                self.setPosition(currentPosition)
            # resetting for later use
            self.currentPositon = None
            self.chosenRect = None
            return [True, move]
        else:
            self.setPosition(currentPosition)
            return [False, move]
            
