import pygame
# import King
import Queen

class bishop(Queen.queen):
    def __init__(self, screen, board, image, rect, row, col, colour):
        super().__init__(screen, board, image, rect, row, col, colour)
    
    # find available moves
    def findMoves(self, show = True, isKing=False):
        # return all moves available
        return [self.moveUpLeft(), self.moveUpRight(), self.moveDownLeft(), self.moveDownRight()]
