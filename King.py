import pygame

class king(pygame.sprite.Sprite):
    def __init__(self, screen, board, image, rect, row, col, colour):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.board = board
        self.image = image
        self.rect = rect  
        self.row = row
        self.col = col
        self.colour = colour
        self.sidePieces = []
        self.enemyPieces = []
        self.originalImage = self.image

        startPosition = (row, col)
        self.setPosition(startPosition)

        self.chosenRect = None
        self.chosenPosition = None
        self.hasMove = False

        # self.image.set_alpha(100)

    def update(self):
        pass

    def delete(self):
        self.sidePieces.remove(self)
        self.kill()

    def render(self):
        return pygame.sprite.RenderPlain(self.sidePieces + self.enemyPieces)

    # get position
    def getPosition(self):
        return (self.row, self.col)
    
    # get rect for the king's position
    def getRect(self):
        return self.rect

    # get opposite colour
    def getOppositeColour(self):
        if (self.colour == "W"):
            return "B"
        else:
            return "W"

    # setting position based on row and col
    def setPosition(self, position):
        newCenter = self.board.getPosition(position[0], position[1])[-1]
        if (newCenter != None):
            self.board.setPositionColour(self.getPosition(), "E")
            self.rect.center = newCenter
            self.row = position[0]
            self.col = position[1]
            self.board.setPositionColour(position, self.colour)
        else:
            raise Exception("There is no position there")
    
    # set side pieces
    def setSidePieces(self, pieces):
        self.sidePieces = pieces

    # set enemy pieces
    def setEnemyPieces(self, pieces):
        self.enemyPieces = pieces

    # setting the image of the piece
    def setImage(self, image):
        self.image = image

    # find available moves
    def findMoves(self, show = True, isKing=False):
        # print(isKing)
        # return all moves available
        allMoves = [self.moveLeft(), self.moveRight(), self.moveUp(), self.moveDown(),
        self.moveUpLeft(), self.moveUpRight(), self.moveDownLeft(), self.moveDownRight()]
        if (not isKing):
             return allMoves

        # castling
        if (not self.hasMove):
            for piece in self.sidePieces:
                piecePosition = piece.getPosition()
                if (not piece.hasMove):
                    if (piecePosition[1] == 0):
                        allMoves.append(self.moveTwoLeft())
                    elif (piecePosition[1] == 7):
                        allMoves.append(self.moveTwoRight())

        safeMoves = []
        for move in allMoves:
            # print(move)
            if (len(move) == 1):
                position = (self.row + move[-1][1], self.col + move[-1][2])
                if (not self.kingCheck(position = position)[0]):
                    safeMoves.append(move)
            else:
                for submove in move:
                    position = (self.row + submove[1], self.col + submove[2])
                    if (not self.kingCheck(position = position)[0]):
                        safeMoves.append([submove])
                    else:
                        break

        return safeMoves

    # show available moves after being clicked
    def showMoves(self, show=True, isKing=False):
        # all centers for the king to move to
        allRects = []
        # print(isKing)
        # getting all moves available
        allMoves = self.findMoves(show = show, isKing = isKing)

        # creating dots where all moves are available
        for moves in allMoves:
            draw = True
            for move in moves:
                possible = move[0]
                if (possible):
                    change = move[1:]
                    
                    row, col = self.row, self.col
                    position = self.board.getPosition(row+change[0], col+change[1])
                    positionCenter = position[-1]
                    if (show and position[0] != self.colour and draw):
                        positionRect = pygame.draw.circle(self.screen, (0, 255, 0), positionCenter, 8)
                    else:
                        transparency = pygame.Color(0, 0, 0, 0)
                        transparency.a = 0
                        # print(transparency)
                        positionRect = pygame.draw.circle(self.screen, transparency, positionCenter, 0)
                    allRects.append([positionRect, (row+change[0], col+change[1]), draw])
                    if (position[0] != 'E'):
                            draw = False
        return allRects

    # check if move is valid
    def validMove(self, newRow, newCol):
        """
        newRow: the new row position

        newCol: the new col position
        """
        if (newRow in range(8) and newCol in range(8)):
            newPosition = (newRow, newCol)
            # if (self.colour != self.board.getPosition(newRow, newCol)[0]):
                # print("Move okay!")
            return True
        # print("Not okay!")
        return False

    # move the King
    def move(self, rowMove, colMove):
        """
        rowMove: checking where to move the piece through rows (can be positive or negative)

        colMove: checking where to move the piece through cols (can be positive or negative)
        """
        row, col = self.row, self.col
        return self.validMove(row+rowMove, col+colMove)

    # move left
    def moveLeft(self):
        allMoves = [[self.move(0, -1, ), 0, -1]]
        if (self.passPoint(allMoves) == self.colour): return [[False, 0, -1]]
        return allMoves
    
    # move right
    def moveRight(self, ):
        allMoves = [[self.move(0, 1, ), 0, 1]]
        if (self.passPoint(allMoves) == self.colour): return [[False, 0, 1]]
        return allMoves

    # move up
    def moveUp(self, colour=""):
        if (colour == ""):
            colour = [self.colour]
        allMoves = [[self.move(1, 0, ), 1, 0]]
        if (self.passPoint(allMoves) in colour): return [[False, 1, 0]]
        return allMoves

    # move down
    def moveDown(self, colour=""):
        if (colour == ""):
            colour = [self.colour]
        allMoves = [[self.move(-1, 0, ), -1, 0]]
        if (self.passPoint(allMoves) in colour): return [[False, -1, 0]]
        return allMoves
    
    # move up left
    def moveUpLeft(self, ):
        allMoves = [[self.move(1, -1, ), 1, -1]]
        if (self.passPoint(allMoves) == self.colour): return [[False, 1, -1]]
        return allMoves

    # move up right
    def moveUpRight(self, ):
        allMoves = [[self.move(1, 1, ), 1, 1]]
        if (self.passPoint(allMoves) == self.colour): return [[False, 1, 1]]
        return allMoves

    # move down left
    def moveDownLeft(self, ):
        allMoves = [[self.move(-1, -1, ), -1, -1]]
        if (self.passPoint(allMoves) == self.colour): return [[False, -1, -1]]
        return allMoves
    
    # move down right
    def moveDownRight(self, ):
        allMoves = [[self.move(-1, 1, ), -1, 1]]
        if (self.passPoint(allMoves) == self.colour): return [[False, -1, 1]]
        return allMoves

    # move two right
    def moveTwoRight(self, ):
        allMoves = []
        for col in range(self.col+1, self.col+3):
            newCol = col - self.col
            allMoves.append([self.move(0, newCol), 0, newCol])
            if (self.passPoint(allMoves) == self.colour): break
        return allMoves
    
    # move two left
    def moveTwoLeft(self, ):
        allMoves = []
        for col in range(self.col-1, self.col-3, -1):
            newCol = col - self.col
            allMoves.append([self.move(0, newCol), 0, newCol])
            if (self.passPoint(allMoves) == self.colour): break
        return allMoves

    # move when dragged
    def dragMove(self, king=False):
        # having the king follow the mouse
        self.rect.center = pygame.mouse.get_pos()
        
        # getting the all available moves and their positions
        allRects = self.showMoves(isKing = king)
        for rect, position, draw in allRects:
            # checking if the piece is touching its potential moves
            if (rect.colliderect(self.rect) and draw):
                self.chosenRect = rect
                self.chosenPosition = position
        
    # confirm move
    def confirmDragMove(self, move):
        # ensuring that the piece only moves to a desired sport
        currentPosition = self.getPosition()
        if (self.chosenRect != None):
            # check if the mouse is touching still touching the square after the mouse let go
            if (self.rect.colliderect(self.chosenRect)):
                if (self.takePiece(self.chosenPosition)):
                    move = self.increaseMove(move)
                    print("Taken!")
                    self.setPosition(self.chosenPosition)
                    if (self.chosenPosition[1] + 2 == currentPosition[1] and (currentPosition == (0, 4) or currentPosition == (7, 4))):
                        for piece in self.sidePieces:
                            if (piece.getPosition() == (self.row, 0)):
                                piece.setPosition((self.row, self.chosenPosition[1]+1))
                                break
                    if (self.chosenPosition[1] - 2 == currentPosition[1] and (currentPosition == (0, 4) or currentPosition == (7, 4))):
                        for piece in self.sidePieces:
                            if (piece.getPosition() == (self.row, 7)):
                                piece.setPosition((self.row, self.chosenPosition[1]-1))
                                break
            else:
                self.setPosition(currentPosition)
            # resetting for later use
            self.currentPositon = None
            self.chosenRect = None
            return [True, move]
        self.setPosition(currentPosition)
        return [False, move]

    # take piece if chess conditions are met
    def takePiece(self, position, delete=True):
        """
        position: The position that's attempted to move to
        pieces: All playable pieces of opposite colour
        """
        desired = self.board.getPosition(position[0], position[1])
        # only run this if the piece is the opposite colour
        if (desired[0] == self.getOppositeColour()):
            chosen = None
            for piece in self.enemyPieces:
                pieceMoves = piece.showMoves(False)
                piecePositions = [(move[1][0], move[1][1]) for move in pieceMoves]
                # print(piecePositions, position[-1], position[-1] in piecePositions)
                # check if the piece trying to be taken is protected
                if (piece.getPosition() == position):
                    chosen = piece
                # if (position in piecePositions):
                #     # print("Can't take")
                #     # return false since the piece can't be taken
                #     return False
            if (delete):
                chosen.delete()
        elif (desired[0] == self.colour):
            # don't take if the piece is the same colour as this piece
            return False
        # can take piece if the position has an opposite colour chess piece that can't be taken or is an empty square
        return True
        
    # can't go pass this point
    def passPoint(self, allMoves):
        if (allMoves[-1][0]):
            position = (self.row + allMoves[-1][1], self.col + allMoves[-1][2])
            colour = self.board.getPosition(position[0], position[1])[0]
            return colour

    # check if king is in check
    def kingCheck(self, position = ""):
        if (position == ""):
            position = self.getPosition()
        position = (position[0], position[1])
        for piece in self.enemyPieces:
            pieceMoves = piece.showMoves(False)
            piecePositions = [(move[1][0], move[1][1]) for move in pieceMoves]
            if (position in piecePositions):
                return [True, piecePositions]
        # self.setImage(self.originalImage)
        return [False, None]

    # check if king is in checkmate
    def kingCheckMate(self, piecePositions):        
        # if the king can still move or pieces can block this move then no checkmate
        if (self.stillMove() or self.block(piecePositions)):
            return False
        # else checkmate!
        return True
    
    # check if king is in stalemate
    def kingStaleMate(self):
        if (not self.stillMove() and len(self.sidePieces) == 1):
            return True
        return False
    
    # check if the king can still move
    def stillMove(self, position = ''):
        currentPosition = position
        if (position == ""):
            currentPosition = self.getPosition()


        # check if its potential positions end in check
        allMoves = self.findMoves()
        for move in allMoves:
            if (move[-1][0]):
                # return true if there is a safe position
                nextPosition = (self.row+move[0][1], self.col+move[0][2])
                if (self.validMove(nextPosition[0], nextPosition[1])):

                    check = self.kingCheck(nextPosition)
                    take = self.takePiece(nextPosition, delete=False)

                    if (not check[0] and take):                  

                        return True
        # return false since there's no safe positions
        return False

    # block abilities
    def block(self, piecePositions):
        block = False
        for piece in self.sidePieces:
            pieceMoves = piece.showMoves(False)
            helpPositions = [(move[1][0], move[1][1]) for move in pieceMoves]
            for position in helpPositions:
                if (position in piecePositions):
                    piece.image.set_alpha(0)
                    originalPosition = piece.getPosition()
                    piece.setPosition(position)
                    if (not self.kingCheck()[0]):
                        block = True
                    piece.setPosition(originalPosition)
                    piece.image.set_alpha(255)
                    if (block):
                        return block
        return block

    # increaes move
    def increaseMove(self, move):
        return move + 1