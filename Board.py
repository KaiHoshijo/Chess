import pygame

class board():
    def __init__(self, screen, boxWidth, boxHeight, colour1, colour2):
        self.screen = screen
        self.boxWidth = boxWidth
        self.boxHeight = boxHeight
        self.colour1 = colour1
        self.colour2 = colour2
        self.positions = {}
        self.fill()
        allCenters = self.drawBoard()
        for row in self.positions:
            for col, position in enumerate(self.positions[row]):
                self.positions[row][col] = position + [allCenters[row][col]]

    # get colour1
    def getColour1(self):
        return self.colour1
    
    # get colour2
    def getColour2(self):
        return self.colour2

    # get box width
    def getBoxWidth(self):
        return self.boxWidth
    
    # get box height
    def getBoxHeight(self):
        return self.boxHeight

    # drawing the board
    def drawBoard(self):
        allCenters = []
        for coloumn in range(8):
            colour1 = self.colour2 if coloumn % 2 == 0 else self.colour1
            colour2 = self.colour1 if coloumn % 2 == 0 else self.colour2
            allCenters.append(self.drawRow(coloumn * self.boxHeight, colour1, colour2))
        return allCenters

    # drawing one box
    def drawRect(self, x, y, colour):
        rect = pygame.Rect(x, y, self.boxWidth, self.boxHeight)
        pygame.draw.rect(self.screen, colour, rect)
        return rect.center

    # draw row
    def drawRow(self, y, colour1, colour2):
        centers = []
        for box in range(8):
            colour = colour1 if box % 2 == 0 else colour2
            centers.append(self.drawRect(box * self.boxWidth, y, colour))
        return centers


    # fill up board
    def fill(self):
        rows = list(range(8))
        for row in rows:
            positions = ["E", "E"]
            self.positions[row] = [positions for _ in range(8)]
    
    # set position
    def setPositionColour(self, position, colour):
        self.positions[position[0]][position[1]][0] = colour

    # get position
    def getPosition(self, row, coloumn):
        if row in self.positions.keys():
            if coloumn in range(8):
                return self.positions[row][coloumn]
        return None

    # get all positions
    def getAllPositions(self):
        for row in self.positions.keys():
            yield self.positions[row]