import pygame
# import King
import Queen

class rook(Queen.queen):
    def __init__(self, screen, board, image, rect, row, col, colour):
        super().__init__(screen, board, image, rect, row, col, colour)

    # find available moves
    def findMoves(self, show = False, isKing=False):
        # return all moves available
        return [self.moveLeft(), self.moveRight(), self.moveUp(), self.moveDown()]

