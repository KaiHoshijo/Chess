import pygame
import King

class knight(King.king):
    def __init__(self, screen, board, image, rect, row, col, colour):
        super().__init__(screen, board, image, rect, row, col, colour)

    # move up left
    def moveUpLeft(self, ):
        allMoves = [[self.move(2, -1, ), 2, -1]]
        if (self.passPoint(allMoves) == self.colour): return [[False, 2, -1]]
        return allMoves
    
    # move up right
    def moveUpRight(self, ):
        allMoves = [[self.move(2, 1, ), 2, 1]]
        if (self.passPoint(allMoves) == self.colour): return [[False, 2, 1]]
        return allMoves

    # move down left
    def moveDownLeft(self, ):
        allMoves = [[self.move(-2, -1, ), -2, -1]]
        if (self.passPoint(allMoves) == self.colour): return [[False, -2, -1]]
        return allMoves

    # move down right
    def moveDownRight(self, ):
        allMoves = [[self.move(-2, 1, ), -2, 1]]
        if (self.passPoint(allMoves) == self.colour): return [[False, -2, 1]]
        return allMoves
    
    # move right up
    def moveRightUp(self, ):
        allMoves = [[self.move(1, 2, ), 1, 2]]
        if (self.passPoint(allMoves) == self.colour): return [[False, 1, 2]]
        return allMoves

    # move right down
    def moveRightDown(self, ):
        allMoves = [[self.move(-1, 2, ), -1, 2]]
        if (self.passPoint(allMoves) == self.colour): return [[False, -1, 2]]
        return allMoves

    # move left up
    def moveLeftUp(self, ):
        allMoves = [[self.move(1, -2, ), 1, -2]]
        if (self.passPoint(allMoves) == self.colour): return [[False, 1, -2]]
        return allMoves
    
    # move left down
    def moveLeftDown(self, ):
        allMoves = [[self.move(-1, -2, ), -1, -2]]
        if (self.passPoint(allMoves) == self.colour): return [[False, -1, -2]]
        return allMoves
    
    # find available moves
    def findMoves(self, show = True, isKing = False):
        # return all moves available
        return [self.moveUpLeft(), self.moveUpRight(), self.moveDownLeft(), self.moveDownRight(), 
        self.moveRightUp(), self.moveRightDown(), self.moveLeftUp(), self.moveLeftDown()]