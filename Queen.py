import pygame
import King

class queen(King.king):
    def __init__(self, screen, board, image, rect, row, col, colour):
        super().__init__(screen, board, image, rect, row, col, colour)
    
    # move left
    def moveLeft(self, ):
        allMoves = []
        for col in range(self.col-1, -1, -1):
            newCol = col - self.col
            allMoves.append([self.move(0, newCol, ), 0, newCol])
            if (self.passPoint(allMoves) == self.colour): break
        return allMoves

    # move right
    def moveRight(self, ):
        allMoves = []
        for col in range(self.col+1, 9):
            newCol = col - self.col
            allMoves.append([self.move(0, newCol, ), 0, newCol])
            if (self.passPoint(allMoves) == self.colour): break
        return allMoves
    
    # move up
    def moveUp(self, ):
        allMoves = []
        for row in range(self.row+1, 9):
            newRow = row - self.row
            allMoves.append([self.move(newRow, 0, ), newRow, 0])
            if (self.passPoint(allMoves) == self.colour): break
        return allMoves

    # move down
    def moveDown(self, ):
        allMoves = []
        for row in range(self.row-1, -1, -1):
            newRow = row - self.row
            allMoves.append([self.move(newRow, 0, ), newRow, 0])
            if (self.passPoint(allMoves) == self.colour): break
        return allMoves

    # move up left
    def moveUpLeft(self, ):
        allMoves = []
        for row, col in zip(range(self.row+1, 9), range(self.col-1, -1, -1)):
            newRow = row - self.row
            newCol = col - self.col
            allMoves.append([self.move(newRow, newCol, ), newRow, newCol])
            if (self.passPoint(allMoves) == self.colour): break
        return allMoves
    
    # move up right
    def moveUpRight(self, ):
        allMoves = []
        for row, col in zip(range(self.row+1, 9), range(self.col+1, 9)):
            newRow = row - self.row
            newCol = col - self.col
            allMoves.append([self.move(newRow, newCol, ), newRow, newCol])
            if (self.passPoint(allMoves) == self.colour): break
        return allMoves

    # move down left
    def moveDownLeft(self, ):
        allMoves = []
        for row, col in zip(range(self.row-1, -1, -1), range(self.col-1, -1, -1)):
            newRow = row - self.row
            newCol = col - self.col
            allMoves.append([self.move(newRow, newCol, ), newRow, newCol])
            if (self.passPoint(allMoves) == self.colour): break
        return allMoves

    # move down right
    def moveDownRight(self, ):
        allMoves = []
        for row, col in zip(range(self.row-1, -1, -1), range(self.col+1, 9)):
            newRow = row - self.row
            newCol = col - self.col
            allMoves.append([self.move(newRow, newCol, ), newRow, newCol])
            if (self.passPoint(allMoves) == self.colour): break
        return allMoves


