import cmu_graphics
from cmu_graphics import *
from urllib.request import urlopen
from PIL import Image
import random


#IMAGE AND SOUND CITATIONS

#battlship title screen image - https://www.google.com/search?q=battleship+images+game&sca_esv=465def9e32fd9f0d&rlz=1C5CHFA_enUS985US985&udm=2&biw=1440&bih=683&ei=1cZMZ_O9ELWs5NoP3uHm8AM&ved=0ahUKEwiz_M6ntIeKAxU1FlkFHd6wGT4Q4dUDCBA&uact=5&oq=battleship+images+game&gs_lp=EgNpbWciFmJhdHRsZXNoaXAgaW1hZ2VzIGdhbWUyBRAAGIAEMgYQABgIGB4yBhAAGAgYHkiGBlDVAliuBXABeACQAQCYATigAfYBqgEBNbgBA8gBAPgBAZgCBqACgwLCAgoQABiABBhDGIoFwgIGEAAYBxgewgIGEAAYChgewgIEEAAYHsICBhAAGAUYHpgDAIgGAZIHATagB6kN&sclient=img#vhid=Hu8DU3xoHmB-tM&vssid=mosaic
#ocean background icon - https://www.freepik.com/premium-photo/backgrounds-water-from-ocean-wave-surface-background-texture_11491727.htm
#ship images - https://www.gmboardgames.com/blog/en/armada-espanola-2/
#sound icon - https://www.vecteezy.com/free-vector/audio-symbol
#bomb icon - https://www.flaticon.com/free-icon/bomb_4357187 
#explosion icon - https://www.flaticon.com/free-icon/explosion_599698
#wave icon - https://www.flaticon.com/free-icon/wave_9047187 
# spash sound - https://pixabay.com/sound-effects/search/water%20drops/ 
#explosion sound - https://pixabay.com/sound-effects/search/explosion/
#coin icon - https://itch.io/game-assets/tag-coin 
#mega bomb icon - https://www.flaticon.com/free-icon/time-bomb_2099753?term=bomb&related_id=2099753
#shield icon - https://iconduck.com/emojis/130754/shield
#plane icon - https://www.flaticon.com/free-icon/airplane_7893979
#bouncer icon - https://www.freepik.com/icons/reverse
#shop next and prev arrows - https://stock.adobe.com/search?k=next+and+back+button


###################################################################################################


def loadPilImage(url):
    return Image.open(url)

class Ship:
    def __init__(self, name, size, x, y, cellWidth):
        self.name = name
        self.size = size
        self.x = x
        self.y = y
        self.direction = 'horizontal'
        self.placed = False
        self.image = None
        self.width = cellWidth * size
        self.height = cellWidth * 2

    def rotate(self):
        if self.direction == 'horizontal':
            self.direction = 'vertical'
        else:
            self.direction = 'horizontal'
        self.width, self.height = self.height, self.width

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setPlaced(self, placed):
        self.placed = placed

    def isSunk(self, playerAims):
        if self.direction == 'horizontal':
            row = int((self.y - 50) // self.height)  # Convert to board coordinates
            col = int((self.x - 275) // (self.width/self.size))  # Convert to board coordinates
            for i in range(self.size):
                if playerAims[row][col + i] != 'X':
                    return False
        else: 
            row = int((self.y - 50) // (self.height/2))  # Convert to board coordinates
            col = int((self.x - 275) // self.width)  # Convert to board coordinates
            for i in range(self.size):
                if playerAims[row + i][col] != 'X':
                    return False
        return True

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.mainBoard = [[None] * cols for row in range(rows)]  # records player's ship location
        self.playerAims = [[None] * cols for row in range(rows)]  # shots made by the player
        self.computerAims = [[None] * cols for row in range(rows)]  # shots made by computer
    

    def drawBoard(self, left, top, cellWidth, cellHeight, borderWidth):
        for row in range(self.rows):
            for col in range(self.cols):
                cellLeft = left + (col * cellWidth)
                cellTop = top + (row * cellHeight)
                
                drawRect(cellLeft, cellTop, cellWidth, cellHeight, 
                        fill=None, border='black', borderWidth=borderWidth)

                if isinstance(self.mainBoard[row][col], Ship):
                    ship = self.mainBoard[row][col]
                    if ship.direction == 'horizontal':
                        drawImage(ship.image, ship.x, ship.y)
                    else:
                        drawImage(ship.image, ship.x, ship.y, rotateAngle=90)

        drawRect(left, top, cellWidth * self.cols, cellHeight * self.rows,
                fill=None, border='black', borderWidth=2*borderWidth)


    def drawIcons(self, left, top, cellWidth, cellHeight, icons):
        for row in range(self.rows):
            for col in range(self.cols):
                cellLeft = left + (col * cellWidth)
                cellTop = top + (row * cellHeight)

                iconX = cellLeft + (cellWidth/2) - 15
                iconY = cellTop + (cellHeight/2) - 15
                
                if self.computerAims[row][col] == 'S':
                    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill='royalBlue', opacity=40)
                elif self.computerAims[row][col] == 'X' or self.playerAims[row][col] == 'X':
                    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill='pink', opacity=40)
                    drawImage(icons['explosion'], iconX, iconY)
                elif self.computerAims[row][col] == 'O' or self.playerAims[row][col] == 'O':
                    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill='lightBlue', opacity=40)
                    drawImage(icons['wave'], iconX, iconY)
        

    def placeShip(self, ship, row, col):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mainBoard[r][c] == ship:
                    self.mainBoard[r][c] = None
                
    # Place ship in new position
        if ship.direction == 'horizontal':
            if col + ship.size > self.cols:
                return False
            for i in range(ship.size):
                self.mainBoard[row][col + i] = ship
        else:  # vertical
            if row + ship.size > self.rows:
                return False
            for i in range(ship.size):
                self.mainBoard[row + i][col] = ship
        return True

    def playerFire(self, row, col):
        print(f"Firing at {row},{col}: {self.mainBoard[row][col]}")
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        
        if self.playerAims[row][col] is not None:
            return False
        
        if isinstance(self.mainBoard[row][col], str) or isinstance(self.mainBoard[row][col], Ship):
            self.playerAims[row][col] = 'X'
            return True
        else:
            self.playerAims[row][col] = 'O'
            return False
        

    def compFire(self, row, col):
        if isinstance(self.mainBoard[row][col], Ship):
            ship = self.mainBoard[row][col]
            if ship.name in self.game.upgrades.shieldedShips:
                self.computerAims[row][col] = 'S'
                return False
        if self.mainBoard[row][col] != None:
            self.computerAims[row][col] = 'X'
            return True
        else:
            self.computerAims[row][col] = 'O'
            return False
        
class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.setupBoard()
        self.initializeShips()
        self.originalSetup()
        self.upgrades = UpgradesHolder(self)
        self.invalid = False
        self.lineX = self.width / 2
        self.lineY = self.height / 2
        self.hit = False
        self.miss = False
        self.wantToSink = False
        
        
        self.oceanImage = CMUImage(loadPilImage('ocean.jpg').resize((width, height)))
        self.soundIcon = CMUImage(loadPilImage('sound_icon.png').resize((40, 40)))
        self.explosionIcon = CMUImage(loadPilImage('explosion.png').resize((30, 30)))
        self.waveIcon = CMUImage(loadPilImage('wave.png').resize((30, 30)))
        self.coinIcon = CMUImage(loadPilImage('coin.png').resize((30, 30)))
        self.shieldIcon = CMUImage(loadPilImage('shield.png').resize((150, 150)))
        self.megaBombIcon = CMUImage(loadPilImage('time-bomb.png').resize((150, 150)))
        self.image1 = CMUImage(loadPilImage('ship_home.jpg').resize((width, height)))
        self.playIcon = CMUImage(loadPilImage('play.png').resize((50, 50)))
        self.tutorialImage = CMUImage(loadPilImage('tutorial-one.png').resize((250, 250)))
        self.bombIcon = CMUImage(loadPilImage('bomb.png').resize((40, 40)))
        self.bouncerIcon = CMUImage(loadPilImage('bouncer.png').resize((150, 150)))
        self.arrowIcon = CMUImage(loadPilImage('arrow.png').resize((35, 35)))
        self.planeBombIcon = CMUImage(loadPilImage('plane.png').resize((150, 150)))


        self.tutorialStartScreen = CMUImage(loadPilImage('startScreen.png').resize((300, 250)))
        self.tutorialFireScreen = CMUImage(loadPilImage('fireScreen.png').resize((300, 250)))
        self.tutorialPlayerView = CMUImage(loadPilImage('playerView.png').resize((400, 250)))
        self.tutorialShopView = CMUImage(loadPilImage('shopView.png').resize((300, 250)))
        self.tutorialUseUpgrade = CMUImage(loadPilImage('useAppear.png').resize((100, 100)))


        
    def setupBoard(self):
        
        self.rows = 10
        self.cols = 10
        boardSize = min(self.width * 0.4, self.height * 0.8)
        self.boardWidth = boardSize
        self.boardHeight = boardSize
        
        horizontalMargin = (self.width - (2 * boardSize)) / 3
        verticalMargin = (self.height - boardSize) / 2
        
        self.boardLeft1 = horizontalMargin
        self.boardLeft2 = 2 * horizontalMargin + boardSize
        self.boardTop1 = verticalMargin
        self.boardTop2 = verticalMargin
        
        self.cellWidth = self.boardWidth / self.cols
        self.cellHeight = self.boardHeight / self.rows
        self.cellBorderWidth = 2
        
        self.playerBoard = Board(self.rows, self.cols)
        self.computerBoard = Board(self.rows, self.cols)

    def initializeShips(self):
        shipStartX = self.boardLeft1 + self.boardWidth + 20
        verticalMargin = (self.height - self.boardHeight) / 2

        self.ship2 = Ship('ship2', 2, shipStartX, verticalMargin, self.cellWidth)
        self.ship3 = Ship('ship3', 3, shipStartX, verticalMargin + self.cellWidth * 1.2, self.cellWidth)
        self.ship4 = Ship('ship4', 4, shipStartX, verticalMargin + self.cellWidth * 2.4, self.cellWidth)
        self.ship5 = Ship('ship5', 5, shipStartX, verticalMargin + self.cellWidth * 3.6, self.cellWidth)
        self.ship6 = Ship('ship6', 5, shipStartX, verticalMargin + self.cellWidth * 4.8, self.cellWidth)

        self.allShips = [self.ship2, self.ship3, self.ship4, self.ship5, self.ship6]
        

        for ship in self.allShips:
            shipImage = loadPilImage(f'{ship.size}Ship.png')
            ship.image = CMUImage(shipImage.resize((int(ship.width), int(ship.height))))


    def originalSetup(self):
        self.draggingShip = None
        self.allShipsPlaced = False
        self.computerShipsPlaced = False
        self.gameOver = False
        self.playerWon = False
        self.points = 0
        self.hoveredRow = None
        self.hoveredCol = None
        self.lastHit = None
        self.shipJustSunk = None
        self.shipJustSunkSize = 0
        self.sunkList = []
        self.hitShips = []

    def checkAllShipsPlaced(self):
        for ship in self.allShips:
            if not ship.placed:
                self.allShipsPlaced = False
                return
        self.allShipsPlaced = True

    def isValidPlacement(self, ship, row, col):
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols:
            return False
            
        if ship.direction == 'horizontal':
            if col + ship.size > self.cols:
                return False
        else:
            if row + ship.size > self.rows:
                return False

        startRow = max(0, row - 1)
        startCol = max(0, col - 1)

        if ship.direction == 'vertical':
            endRow = min(self.rows, row + ship.size + 1)
            endCol = min(self.cols, col + 2)

        else:
            endRow = min(self.rows, row + 2)
            endCol = min(self.cols, col + ship.size + 1)

        for r in range(startRow, endRow):
            for c in range(startCol, endCol):
                if self.playerBoard.mainBoard[r][c] != None:
                    if self.playerBoard.mainBoard[r][c] != ship:
                        return False
        return True

    def drawLabels(self):
        letter = 'A'
        for row in range(self.rows):
            drawLabel(letter, self.boardLeft1 - 15, self.boardTop1 + (row * self.cellHeight) + 15)
            if self.computerShipsPlaced:
                drawLabel(letter, self.boardLeft2 - 15, self.boardTop2 + (row * self.cellHeight) + 15)
            letter = chr(ord(letter) + 1)
        
        number = 1
        for col in range(self.cols):
            drawLabel(str(number), 
                     self.boardLeft1 + (col * self.cellWidth) + 15, 
                     self.boardTop1 - 15)
            if self.computerShipsPlaced:
                drawLabel(str(number), 
                         self.boardLeft2 + (col * self.cellWidth) + 15, 
                         self.boardTop2 - 15)
            number += 1

    def generateComputerBoard(self):

        self.computerShips = {'ship2': {'size': 2, 'placed': False},
            'ship3': {'size': 3, 'placed': False},
            'ship4': {'size': 4, 'placed': False},
            'ship5': {'size': 5, 'placed': False},
            'ship6': {'size': 5, 'placed': False}
        }

        # referenced for how to loop through dict values: https://www.w3schools.com/python/gloss_python_loop_dictionary_items.asp
        for shipName, shipInfo in self.computerShips.items():
            currAttempts = 0
            maxAttempts = 100
            
            while shipInfo['placed'] == False and currAttempts < maxAttempts:
                direction = random.choice(['horizontal', 'vertical'])
                if direction == 'horizontal':
                    row = random.randint(0, self.rows - 1)
                    col = random.randint(0, self.cols - shipInfo['size'])
                else:
                    row = random.randint(0, self.rows - shipInfo['size'])
                    col = random.randint(0, self.cols - 1)

                isValidPlace = True
                for i in range(-1, shipInfo['size'] + 1):
                    for j in range(-1, 2):
                        if direction == 'horizontal':
                            dRow = row + j
                            dCol = col + i
                        else:
                            dRow = row + i
                            dCol = col + j
                            
                        if ((0 <= dRow < self.rows) and (0 <= dCol < self.cols) and 
                            (self.computerBoard.mainBoard[dRow][dCol] is not None)):
                            isValidPlace = False
                            break

                    if not isValidPlace:
                        break
                
                if isValidPlace:
                    for i in range(shipInfo['size']):
                        if direction == 'horizontal':
                            self.computerBoard.mainBoard[row][col + i] = shipName
                        else:
                            self.computerBoard.mainBoard[row + i][col] = shipName
                        shipInfo['placed'] = True
                currAttempts += 1
        for row in self.computerBoard.mainBoard:
            print(row)
        
        self.computerShipsPlaced = True

    def computerTurn(self):
        if self.wantToSink and self.sunkList:
            row, col = self.sunkList.pop(0)
            if (0 <= row < self.rows and 0 <= col < self.cols and 
                self.playerBoard.computerAims[row][col] is None):
                self.lastHit = (row, col)
                shipInCell = self.playerBoard.mainBoard[row][col]
                
                if (row, col) in self.upgrades.bouncerCells:
                    self.upgrades.bouncerCells.remove((row, col))
                    self.upgrades.lastBouncerHit = (row, col)
                    self.upgrades.showBounceAnimation = True
                    self.computerBoard.playerAims[row][col] = 'X'
                    return
                
                if shipInCell is not None:
                    shipName = None
                    for ship in self.allShips:
                        if shipInCell == ship:
                            shipName = ship.name
                            break
                    
                    if shipName in self.upgrades.shieldedShips:
                        self.upgrades.shieldedShips.remove(shipName)
                        self.playerBoard.computerAims[row][col] = 'S'
                        return 
                    else:
                        self.playerBoard.computerAims[row][col] = 'X'
                        if self.points > 0:
                            self.points -= 5
                        self.wantToSink = True
                        self.checkAdjacentCells(row, col)
                else:
                    self.playerBoard.computerAims[row][col] = 'O'
            else:
                self.computerTurn()
                
            # Add game over check here
            if self.checkAllPlayerShipsSunk():
                return
            return

        unHitCells = []
        for row in range(self.rows):
            for col in range(self.cols):
                if (self.playerBoard.computerAims[row][col] is None or 
                    self.playerBoard.computerAims[row][col] == 'S'):
                    unHitCells.append((row, col))
        
        if unHitCells:
            row, col = random.choice(unHitCells)
            self.lastHit = (row, col)
            shipInCell = self.playerBoard.mainBoard[row][col]
            
            if (row, col) in self.upgrades.bouncerCells:
                self.upgrades.bouncerCells.remove((row, col))
                self.upgrades.lastBouncerHit = (row, col)
                self.upgrades.showBounceAnimation = True
                self.computerBoard.playerAims[row][col] = 'X'
                return
                
            if shipInCell is not None:
                shipName = None
                for ship in self.allShips:
                    if shipInCell == ship:
                        shipName = ship.name
                        break
                
                if shipName in self.upgrades.shieldedShips:
                    self.upgrades.shieldedShips.remove(shipName)
                    self.playerBoard.computerAims[row][col] = 'S'
                else:
                    self.playerBoard.computerAims[row][col] = 'X'
                    if self.points > 0:
                        self.points -= 5
                    self.wantToSink = True
                    self.checkAdjacentCells(row, col)
            else:
                self.playerBoard.computerAims[row][col] = 'O'
                
        # Add game over check here too
        if self.checkAllPlayerShipsSunk():
            return

    def checkAllComputerShipsSunk(self):
    # Check if all computer ships have been hit
        for row in range(self.rows):
            for col in range(self.cols):
                if (isinstance(self.computerBoard.mainBoard[row][col], str) and 
                    self.computerBoard.playerAims[row][col] != 'X'):
                    return False
        self.gameOver = True
        self.playerWon = True
        setActiveScreen('gameOver')
        return True
    
    def checkAllPlayerShipsSunk(self):
        for ship in self.allShips:
            if not ship.isSunk(self.playerBoard.computerAims):
                return False
        self.gameOver = True
        self.playerWon = False
        setActiveScreen('gameOver')
        return True

    def checkAdjacentCells(self, row, col):
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for drow, dcol in moves:
            newRow = row + drow
            newCol = col + dcol
            if (0 <= newRow < self.rows and 
                0 <= newCol < self.cols and 
                self.playerBoard.computerAims[newRow][newCol] is None):
                self.sunkList.append((newRow, newCol))

              
class UpgradesHolder:
    def __init__(self, game):
        self.game = game
        self.megaBombs = 0
        self.megaBombInUse = False
        self.shields = 0
        self.shieldInUse = False
        self.shieldedShips = set()
        self.bouncers = 0
        self.bouncerInUse = False
        self.planeBomb = 0
        self.planeBombInUse = False
        self.bouncerCells = set()
        self.selectingBouncers = False
        self.bouncersToPlace = 0
        self.lastBouncerHit = None
        self.showBounceAnimation = False
        self.planeSelectedCells = []

    def useMegaBomb(self, row, col, board):
        shipHit = False
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                newRow = row + drow
                newCol = col + dcol
                if 0 <= newRow < self.game.rows and 0 <= newCol < self.game.cols:
                    # Check for any non-None value since computer ships are stored as strings
                    if board.mainBoard[newRow][newCol] is not None:
                        board.playerAims[newRow][newCol] = 'X'
                        shipHit = True
                        self.game.points += 10
                    else:
                        board.playerAims[newRow][newCol] = 'O'
        self.megaBombs -= 1
        self.megaBombInUse = False
        return shipHit

    def useShield(self, ship):
        if self.shields > 0:
            self.shieldedShips.add(ship)
            self.shields -= 1
            self.shieldInUse = False
            return True
        return False

    def useBouncer(self, row, col):
        if self.bouncers > 0 and (row, col) not in self.bouncerCells:
            self.bouncerCells.add((row, col))
            self.bouncersToPlace -= 1
            if self.bouncersToPlace == 0:
                self.selectingBouncers = False
                self.bouncerInUse = False
            return True
        return False

    def usePlaneBomb(self, selectedCells, computerBoard):
        if len(selectedCells) == 3 and self.planeBomb > 0:
            for row, col in selectedCells:
                if isinstance(computerBoard.mainBoard[row][col], Ship):
                    computerBoard.playerAims[row][col] = 'X'
                    self.game.points += 20
                else:
                    computerBoard.playerAims[row][col] = 'O'
            self.planeBomb -= 1
            self.planeBombInUse = False
            self.planeSelectedCells = []
            return True
        return False


##########################################################

    
def onAppStart(app):
    app.width = 900
    app.height = 500
    app.game = Game(app.width, app.height)

    urlSoundBackground = 'sound/battleship_background_music.mp3'
    app.sound = Sound(urlSoundBackground)
    app.musicPaused = False
    app.sound.play(loop=True)
    urlSplash = 'sound/missAudio.mp3'
    app.splash = Sound(urlSplash)
    urlExplosion = 'sound/explosion.mp3'
    app.explode = Sound(urlExplosion)

def allKeyPresses(app, key):
    if key == 'p':
        setActiveScreen('ships')
    elif key == 't':
        setActiveScreen('tutorial')
    elif key == 'h':
        setActiveScreen('selection')
    elif key == 'space' and app.game.draggingShip:
        ship = app.game.draggingShip
        ship.rotate()



######### START SCREEN 
def start_onKeyPress(app, key):
    allKeyPresses(app, key)

def start_redrawAll(app):
    drawImage(app.game.image1, 0, 0)
    drawImage(app.game.soundIcon, 825, 15)
    if app.musicPaused:
        drawLine(825, 15, 865, 55, fill='red')

    drawRect(app.width/2 - 10, app.height/2 + 200, 60, 40, fill='white')
    drawImage(app.game.playIcon, app.width/2, app.height/2 + 195)

def start_onMousePress(app, mouseX, mouseY):
    if mouseX >= 825 and mouseX <= 865 and mouseY >= 30 and mouseY <= 70:
        if app.musicPaused: 
            app.musicPaused = False
            app.sound.play(loop=True)
        else: 
            app.musicPaused = True
            app.sound.pause()
    if mouseX >= 440 and mouseX <= 500 and mouseY >= 450 and mouseY <= 490:
        setActiveScreen('selection')


######### SELECTION SCREEN 

def selection_redrawAll(app):
    drawImage(app.game.oceanImage, 0, 0, opacity=40)
    drawRect(150, 50, app.width/2 + 150, app.height/2 - 20, fill='steelBlue', opacity=90)
    drawRect(150, 50, app.width/2 + 150, app.height/2 - 20, fill=None, border='white', borderWidth=3)
    drawLabel('Welcome to Battleship!', 450, 90, size = 25, fill='white', bold=True)
    drawLabel('Begin your competition against the AI, start', 450, 140, size = 20, fill='white')
    drawLabel('with a tutorial, or browse the shop!', 450, 160, size = 20, fill='white')
    drawLabel('Keep track of your points at the top-left of your ', 450, 210, size = 15, fill='white')
    drawLabel('screen and turn the background music on/off by pressing the icon at the top right :)', 450, 230, size = 15, fill='white')
    drawLabel("Press 'h' at any time to come back to this screen!", 450, 250, size = 15, fill = 'white', italic = True)

    drawRect(100, 300, 200, 100, fill='steelBlue', opacity=90)
    drawRect(100, 300, 200, 100, fill=None, border='white', borderWidth=3)
    drawLabel('Tutorial', 200, 350, size=20, bold=True, fill='white')


    drawRect(350, 300, 200, 100, fill='steelBlue', opacity=90)
    drawRect(350, 300, 200, 100, fill=None, border='white', borderWidth=3)
    drawLabel('Begin the Game', 450, 350, size=20, bold=True, fill='white')

    drawRect(600, 300, 200, 100, fill='steelBlue', opacity=90)
    drawRect(600, 300, 200, 100, fill=None, border='white', borderWidth=3)
    drawLabel('Visit the Shop', 700, 350, size=20, bold=True, fill='white')

    drawImage(app.game.soundIcon, 825, 15)
    if app.musicPaused:
        drawLine(825, 15, 865, 55, fill='red')

def selection_onMousePress(app, mouseX, mouseY):
    if mouseX >= 825 and mouseX <= 865 and mouseY >= 30 and mouseY <= 70:
        if app.musicPaused: 
            app.musicPaused = False
            app.sound.play(loop=True)
        else: 
            app.musicPaused = True
            app.sound.pause()
    elif mouseX >= 100 and mouseX <= 300 and mouseY >= 300 and mouseY <= 400:
        setActiveScreen('tutorial')
    elif mouseX >= 350 and mouseX <= 550 and mouseY >= 300 and mouseY <= 400:
        setActiveScreen('ships')
    elif mouseX >= 600 and mouseX <= 800 and mouseY >= 300 and mouseY <= 400:
        setActiveScreen('shop1')

def selection_onKeyPress(app, key):
    allKeyPresses(app, key)


######### TUTORIAL SCREEN 
def tutorial_onKeyPress(app, key):
    allKeyPresses(app, key)
    
def tutorial_redrawAll(app):
    drawBackground(app)
    drawImage(app.game.tutorialStartScreen, 180, 140)
    drawLabel('Place Your Ships', app.width/2, 90, size = 30, fill = 'white', bold = True)

    drawLabel('Drag and drop ships to the board', 600, 190, size = 15, fill = 'white')

    drawLabel('Click the space bar to rotate', 600, 230, size = 15, fill = 'white')
    drawLabel('the selected ship', 600, 250, size = 15, fill = 'white')

    drawLabel("'Invalid Placement' message will ", 600, 290, size = 15, fill = 'white')
    drawLabel('appear if incorrect placement', 600, 310, size = 15, fill = 'white')

    drawImage(app.game.arrowIcon, 700, 400, rotateAngle=180)


def tutorial_onMousePress(app, mouseX, mouseY):
    if mouseX >= 825 and mouseX <= 865 and mouseY >= 30 and mouseY <= 70:
        if app.musicPaused: 
            app.musicPaused = False
            app.sound.play(loop=True)
        else: 
            app.musicPaused = True
            app.sound.pause()
    if mouseX >= 700 and mouseX <= 735 and mouseY >= 400 and mouseY <= 435:
        setActiveScreen('tutorial2')


def tutorial2_onKeyPress(app, key):
    allKeyPresses(app, key)

def tutorial2_redrawAll(app):
    drawBackground(app)
    drawImage(app.game.tutorialFireScreen, 170, 140)
    drawLabel('Fire Your Shot', app.width/2, 90, size = 30, fill = 'white', bold = True)

    drawLabel('Move your mouse and aim at a cell', 600, 190, size = 15, fill = 'white')

    drawLabel('Watch your points in the upper-left', 600, 230, size = 15, fill = 'white')

    drawLabel('Click to fire and wait for the', 600, 270, size = 15, fill = 'white')
    drawLabel('explosion or splash', 600, 290, size = 15, fill = 'white')

    drawLabel('Can apply upgrades here', 600, 330, size = 15, fill = 'white')
    drawLabel('(Click the coin to purchase anytime)', 600, 350, size = 15, fill = 'white')

    drawImage(app.game.arrowIcon, 165, 400)
    drawImage(app.game.arrowIcon, 700, 400, rotateAngle = 180)

def tutorial2_onMousePress(app, mouseX, mouseY):
    if mouseX >= 825 and mouseX <= 865 and mouseY >= 30 and mouseY <= 70:
        if app.musicPaused: 
            app.musicPaused = False
            app.sound.play(loop=True)
        else: 
            app.musicPaused = True
            app.sound.pause()

    if mouseX >= 700 and mouseX <= 735 and mouseY >= 400 and mouseY <= 435:
        setActiveScreen('tutorial3')
    elif mouseX >= 165 and mouseX <= 200 and mouseY >= 400 and mouseY <= 435:
        setActiveScreen('tutorial')


def tutorial3_onKeyPress(app, key):
    allKeyPresses(app, key)

def tutorial3_redrawAll(app):
    drawBackground(app)
    drawImage(app.game.tutorialPlayerView, 250, 120)
    drawLabel('Observe the Game', 450, 90, size = 30, fill = 'white', bold = True)

    drawLabel("Receive live information about the computer's actions", app.width/2, 390, size = 15, fill = 'white')

    drawLabel('Explosion = Hit, Wave = Miss', app.width/2, 415, size = 15, fill = 'white')


    drawImage(app.game.arrowIcon, 165, 400)
    drawImage(app.game.arrowIcon, 700, 400, rotateAngle = 180)



def tutorial3_onMousePress(ap, mouseX, mouseY):
    if mouseX >= 825 and mouseX <= 865 and mouseY >= 30 and mouseY <= 70:
        if app.musicPaused: 
            app.musicPaused = False
            app.sound.play(loop=True)
        else: 
            app.musicPaused = True
            app.sound.pause()

    if mouseX >= 700 and mouseX <= 735 and mouseY >= 400 and mouseY <= 435:
        setActiveScreen('selection')
    elif mouseX >= 165 and mouseX <= 200 and mouseY >= 400 and mouseY <= 435:
        setActiveScreen('tutorial2')



######### SHIPS SCREEN 
def ships_onKeyPress(app, key):
    allKeyPresses(app, key)

def ships_redrawAll(app):
    drawImage(app.game.oceanImage, 0, 0, opacity=40)
    drawImage(app.game.coinIcon, 10, 10)
    drawLabel(f'{app.game.points} POINTS', 95, 25, size=18, bold=True)
    
    drawImage(app.game.soundIcon, 825, 15)
    if app.musicPaused:
        drawLine(825, 15, 865, 55, fill='red')

    icons = {
        'explosion': app.game.explosionIcon, 
        'wave': app.game.waveIcon,
        'shield': app.game.shieldIcon,
        'bouncer': app.game.bouncerIcon,
        'plane bomb': app.game.planeBombIcon
    } 
    
    app.game.playerBoard.drawBoard(app.game.boardLeft1, app.game.boardTop1, 
        app.game.cellWidth, app.game.cellHeight, app.game.cellBorderWidth)

    drawShields(app, app.game.playerBoard)

    
    if app.game.computerShipsPlaced:
        app.game.computerBoard.drawBoard(app.game.boardLeft2, app.game.boardTop2, 
            app.game.cellWidth, app.game.cellHeight, app.game.cellBorderWidth)
        app.game.drawLabels()

    for ship in app.game.allShips:
        if ship.direction == 'horizontal':
            drawImage(ship.image, ship.x, ship.y)
        else:
            drawImage(ship.image, ship.x, ship.y, rotateAngle=90)

    if app.game.playerBoard and app.game.computerBoard:
        app.game.playerBoard.drawIcons(app.game.boardLeft1, app.game.boardTop1, 
        app.game.cellWidth, app.game.cellHeight, icons)

        app.game.computerBoard.drawIcons(app.game.boardLeft2, app.game.boardTop2, 
            app.game.cellWidth, app.game.cellHeight, icons)


    if app.game.invalid:
        drawLabel("INVALID PLACEMENT", app.game.width/2, app.game.height/2, 
                 fill='red', bold=True, size=30, border='maroon')

    if app.game.allShipsPlaced:
        drawRect(600, app.game.height/2 + 50, 250, 75, fill='darkBlue')
        drawLabel('Confirm Placement', 720, app.game.height/2 + 80, 
                 size=20, bold=True, fill='white')
        

    if app.game.upgrades.megaBombInUse:
        drawImage(app.game.megaBombIcon, 340, 10, width=40, height=40)
        drawLabel("MEGA BOMB ACTIVE", 475, 35, size=15, bold=True, fill='red')
        if app.game.hoveredRow != None and (app.game.hoveredCol != None):
            for drow in [-1, 0, 1]:
                for dcol in [-1, 0, 1]:
                    newRow = app.game.hoveredRow + drow
                    newCol = app.game.hoveredCol + dcol
                    if 0 <= newRow < app.game.rows and 0 <= newCol < app.game.cols:
                        cellLeft = 275 + newCol * app.game.cellWidth
                        cellTop = 50 + newRow * app.game.cellHeight
                        drawRect(cellLeft, cellTop, app.game.cellWidth, app.game.cellHeight,
                            fill='pink', opacity=40)

    if app.game.lastHit is not None:
        row, col = app.game.lastHit
        letter = chr(ord('A') + row)
        number = col + 1
        if app.game.playerBoard.computerAims[row][col] == 'X':
            drawLabel(f"Computer hit at {letter}{number}!", 
                     app.game.width/2, app.game.height - 50, 
                     size=20, bold=True, fill='red')
        else:
            drawLabel(f"Computer missed at {letter}{number}", 
                     app.game.width/2, app.game.height - 50, 
                     size=20, bold=True, fill='blue')

    if app.game.shipJustSunk != None:
        drawLabel(f"You sunk the {app.game.shipJustSunkSize}-cell battleship!", app.game.width/2, app.game.height - 30, 
                 size=20, bold=True, fill='darkGreen')


    if app.game.upgrades.shieldInUse:
        drawRect(0, 0, app.width, 60, fill='royalBlue', opacity=50)
        drawLabel("SHIELD MODE: Click a ship to protect it!", 
                 app.width/2, 30, size=24, bold=True, fill='white')
        
    
    if app.game.upgrades.selectingBouncers:
        drawRect(0, 0, app.width, 60, fill='purple', opacity=50)
        drawLabel(f"BOUNCER MODE: Select {app.game.upgrades.bouncersToPlace} more cells to protect", 
                 app.width/2, 30, size=24, bold=True, fill='white')

    for row, col in app.game.upgrades.bouncerCells:
        cellLeft = app.game.boardLeft1 + (col * app.game.cellWidth)
        cellTop = app.game.boardTop1 + (row * app.game.cellHeight)
        drawImage(app.game.bouncerIcon, 
                 cellLeft + app.game.cellWidth/4, 
                 cellTop + app.game.cellHeight/4,
                 width=app.game.cellWidth/2,
                 height=app.game.cellHeight/2)

    if app.game.upgrades.showBounceAnimation and app.game.upgrades.lastBouncerHit:
        row, col = app.game.upgrades.lastBouncerHit
        cellLeft = app.game.boardLeft1 + (col * app.game.cellWidth) 
        cellTop = app.game.boardTop1 + (row * app.game.cellHeight)
        drawRect(cellLeft, cellTop, app.game.cellWidth, app.game.cellHeight,
                fill='purple', opacity=60)
        drawLabel("BOUNCE",app.width/2, 30, fill = 'purple', size = 20, bold = True )


def drawShields(app, board):
    for row in range(board.rows):
        for col in range(board.cols):
            if isinstance(board.mainBoard[row][col], Ship):
                ship = board.mainBoard[row][col]
                if ship.name in app.game.upgrades.shieldedShips:
                    startRow = row
                    startCol = col
                    while startRow > 0 and isinstance(board.mainBoard[startRow-1][col], Ship) and board.mainBoard[startRow-1][col] == ship:
                        startRow -= 2
                    while startCol > 0 and isinstance(board.mainBoard[row][startCol-1], Ship) and board.mainBoard[row][startCol-1] == ship:
                        startCol -= 1
                        
                    cellLeft = app.game.boardLeft1 + (startCol * app.game.cellWidth)
                    cellTop = app.game.boardTop1 + (startRow * app.game.cellHeight)
                    
                    if ship.direction == 'horizontal':
                        shieldWidth = app.game.cellWidth * ship.size
                        shieldHeight = app.game.cellHeight
                    else:
                        shieldWidth = app.game.cellWidth
                        shieldHeight = app.game.cellHeight * (ship.size) 
                        if ship.size == 5:
                            shieldHeight = app.game.cellHeight * (ship.size - 1) 
                        
                    drawRect(cellLeft, cellTop, shieldWidth, shieldHeight,
                           fill=None, border='royalBlue', borderWidth=3)
                    break


def ships_onMousePress(app, mouseX, mouseY):
    app.game.upgrades.megaBombInUse = False
    app.game.hoveredRow = None
    app.game.hoveredCol = None
    app.game.shipJustSunk = None


    if app.game.upgrades.shieldInUse:
        r, c = cellinMousePlayer(app, mouseX, mouseY)
        if r is not None and c is not None:
            ship = app.game.playerBoard.mainBoard[r][c]
            if isinstance(ship, Ship) and ship.name not in app.game.upgrades.shieldedShips:
                # Add debug print
                print(f"Adding shield to ship {ship.name}")
                app.game.upgrades.shieldedShips.add(ship.name)
                app.game.upgrades.shields -= 1
                app.game.upgrades.shieldInUse = False
                return

    for ship in app.game.allShips:
        if not ship.placed:  
            shipWidth = ship.width if ship.direction == 'horizontal' else ship.height
            shipHeight = ship.height if ship.direction == 'horizontal' else ship.width
            
            if (ship.x <= mouseX <= ship.x + shipWidth and 
                ship.y <= mouseY <= ship.y + shipHeight):
                app.game.draggingShip = ship
                app.game.dragOffsetX = mouseX - ship.x
                app.game.dragOffsetY = mouseY - ship.y
                break

    if ((app.game.computerShipsPlaced) and (mouseX >= app.game.boardLeft2) and 
        (mouseX <= app.game.boardWidth + app.game.boardLeft2) and 
        (mouseY >= app.game.boardTop2) and 
        (mouseY <= app.game.boardHeight + app.game.boardTop2)):
        setActiveScreen('fire')

    if 825 <= mouseX <= 865 and 30 <= mouseY <= 70:
        if app.musicPaused: 
            app.musicPaused = False
            app.sound.play(loop=True)
        else: 
            app.musicPaused = True
            app.sound.pause()

    if (app.game.allShipsPlaced and 600 <= mouseX <= 850 and 
        app.game.height/2 + 50 <= mouseY <= app.game.height/2 + 125):
        app.game.computerShipsPlaced = True
        app.game.allShipsPlaced = False
        app.game.generateComputerBoard()
        
    app.game.upgrades.planeBombInUse = False
    app.game.upgrades.planeSelectedCells = []
    
    if mouseX >= 10 and mouseX <= 70 and mouseY >= 10 and mouseY <= 70:
        setActiveScreen('shop1')

    if app.game.upgrades.selectingBouncers:
        r, c = cellinMousePlayer(app, mouseX, mouseY)
        if r is not None and c is not None:
            if app.game.upgrades.useBouncer(r, c):
                if app.game.upgrades.bouncersToPlace == 0:
                    app.game.upgrades.selectingBouncers = False
                    app.game.upgrades.bouncerInUse = False
                return

def ships_onMouseDrag(app, mouseX, mouseY):
    if app.game.draggingShip:
        ship = app.game.draggingShip
        ship.x = mouseX - app.game.dragOffsetX
        ship.y = mouseY - app.game.dragOffsetY
        app.game.invalid = False

def ships_onMouseRelease(app, mouseX, mouseY):
    if app.game.draggingShip:
        ship = app.game.draggingShip
        cellWidth = app.game.boardWidth / app.game.cols
        cellHeight = app.game.boardHeight / app.game.rows
        col = int((mouseX - app.game.boardLeft1) // cellWidth)
        row = int((mouseY - app.game.boardTop1) // cellHeight)

        for r in range(app.game.rows):
            for c in range(app.game.cols):
                if app.game.playerBoard.mainBoard[r][c] == ship:
                    app.game.playerBoard.mainBoard[r][c] = None

        if ship.direction == 'horizontal':
            exactX = app.game.boardLeft1 + (col * cellWidth) + (app.game.cellBorderWidth * 2)
            exactY = app.game.boardTop1 + (row * cellHeight) + (cellHeight - ship.height)/2
        else:
            exactX = app.game.boardLeft1 + (col * cellWidth) + (cellWidth - ship.height)/2
            exactY = app.game.boardTop1 + (row * cellHeight) + (app.game.cellBorderWidth * 2)


        inBoard = (mouseX >= app.game.boardLeft1 and 
                  mouseX <= app.game.boardLeft1 + app.game.boardWidth and
                  mouseY >= app.game.boardTop1 and 
                  mouseY <= app.game.boardTop1 + app.game.boardHeight)

        if inBoard and app.game.isValidPlacement(ship, row, col):
            app.game.invalid = False
            app.game.playerBoard.placeShip(ship, row, col)
            ship.setPosition(exactX, exactY)
            ship.setPlaced(True)
            
        else:
            app.game.invalid = True
            ship.setPlaced(False)

        app.game.checkAllShipsPlaced()
        app.game.draggingShip = None

def cellinMousePlayer(app, mouseX, mouseY):
    if (mouseX >= app.game.boardLeft1 and mouseX <= app.game.boardLeft1 + app.game.boardWidth and
        mouseY >= app.game.boardTop1 and mouseY <= app.game.boardTop1 + app.game.boardHeight):
        row = int((mouseY - app.game.boardTop1) // app.game.cellHeight)
        col = int((mouseX - app.game.boardLeft1) // app.game.cellWidth)
        if 0 <= row < app.game.rows and 0 <= col < app.game.cols:
            return (row, col)
    return(None, None)

def cellinMouse(app, mouseX, mouseY):
    if (mouseX >= 275 and mouseX <= 275 + app.game.boardWidth and
        mouseY >= 50 and mouseY <= 50 + app.game.boardHeight):
        row = int((mouseY - 50) // app.game.cellHeight)
        col = int((mouseX - 275) // app.game.cellWidth)
        if 0 <= row < app.game.rows and 0 <= col < app.game.cols:
            return (row, col)
    return(None, None)






######### FIRE SCREEN 
def fire_onKeyPress(app, key):
    allKeyPresses(app, key)

def fire_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='lightSteelBlue')
    drawImage(app.game.coinIcon, 10, 10)
    drawLabel(f'{app.game.points} POINTS', 95, 25, size=18, bold=True)

    # if not app.game.upgrades.megaBombInUse:
    #     app.game.hoveredRow = None
    #     app.game.hoveredCol = None
    
    drawImage(app.game.soundIcon, 825, 15)
    if app.musicPaused:
        drawLine(825, 15, 865, 55, fill='red')

    for row in range(app.game.rows):
        for col in range(app.game.cols):
            cellLeft = 275 + col * app.game.cellWidth
            cellTop = 50 + row * app.game.cellHeight
            color = None
            if row == app.game.hoveredRow and col == app.game.hoveredCol:
                color = 'mistyRose'
                
            drawRect(cellLeft, cellTop, app.game.cellWidth, app.game.cellHeight,
                    fill=color, border='steelBlue', borderWidth=2)

            if app.game.computerBoard.playerAims[row][col] == 'X':
                drawImage(app.game.explosionIcon, 
                         cellLeft + (app.game.cellWidth/2) - 15, 
                         cellTop + (app.game.cellHeight/2) - 15)
            elif app.game.computerBoard.playerAims[row][col] == 'O':
                drawImage(app.game.waveIcon, 
                         cellLeft + (app.game.cellWidth/2) - 15, 
                         cellTop + (app.game.cellHeight/2) - 15)
    
    drawRect(275, 50, app.game.boardWidth, app.game.boardHeight,
            fill=None, border='steelBlue', borderWidth=2*app.game.cellBorderWidth)
    

    letter = 'A'
    for row in range(app.game.rows):
        cellTop = 50 + row * app.game.cellHeight + (app.game.cellHeight/2)  
        drawLabel(letter, 255, cellTop, size=20, fill='steelBlue', bold = True)  
        letter = chr(ord(letter) + 1)

    number = 1
    for col in range(app.game.cols):
        cellLeft = 275 + col * app.game.cellWidth + (app.game.cellWidth/2)  
        drawLabel(number, cellLeft, 35, size=20, fill='steelBlue', bold = True) 
        number += 1

    drawLine(app.game.lineX, 0, app.game.lineX, app.height, fill='steelBlue', lineWidth=5)
    drawLine(0, app.game.lineY, app.width, app.game.lineY, fill='steelBlue', lineWidth=5)
    drawImage(app.game.bombIcon, app.game.lineX - 15, app.game.lineY - 25)

    if app.game.upgrades.megaBombInUse:
        drawImage(app.game.megaBombIcon, 10, 50, width=50, height=50)
        drawLabel("MEGA BOMB ACTIVE", 150, 75, size=15, bold=True, fill='red')

    if ((app.game.upgrades.megaBombInUse == True) and (app.game.hoveredRow != None) and (app.game.hoveredCol != None)):
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                newRow = app.game.hoveredRow + drow
                newCol = app.game.hoveredCol + dcol
                if 0 <= newRow < app.game.rows and 0 <= newCol < app.game.cols:
                    cellLeft = 275 + newCol * app.game.cellWidth
                    cellTop = 50 + newRow * app.game.cellHeight
                    drawRect(cellLeft, cellTop, app.game.cellWidth, app.game.cellHeight,
                            fill='pink', opacity=40)
    

    if app.game.upgrades.planeBombInUse:
        for row, col in app.game.upgrades.planeSelectedCells:
            cellLeft = 275 + col * app.game.cellWidth
            cellTop = 50 + row * app.game.cellHeight
            drawRect(cellLeft, cellTop, app.game.cellWidth, app.game.cellHeight,
                    fill='red', opacity=40)
            drawImage(app.game.planeBombIcon, cellLeft + app.game.cellWidth /4, 
            cellTop + app.game.cellHeight / 4, width = app.game.cellWidth/2, height = app.game.cellHeight/2)
        
        remaining = 3 - len(app.game.upgrades.planeSelectedCells)
        drawLabel(f'PLANE BOMB: SELECT {remaining} MORE', app.width/2, 450, 
            size=20, bold=True, fill='red')

        


def fire_onMousePress(app, mouseX, mouseY):

    app.game.upgrades.lastBouncerHit = None
    app.game.upgrades.showBounceAnimation = False
   
    if 825 <= mouseX <= 865 and 30 <= mouseY <= 70:
        app.musicPaused = not app.musicPaused
        if app.musicPaused:
            app.sound.pause()
        else:
            app.sound.play(loop=True)
        return

    if mouseX >= 10 and mouseX <= 70 and mouseY >= 10 and mouseY <= 70:
        setActiveScreen('shop1')
        return

    r, c = cellinMouse(app, mouseX, mouseY)
    if r == None or c == None:
        return
        
    if app.game.upgrades.planeBombInUse:
        # Check if cell is already selected or previously hit
        if ((r, c) not in app.game.upgrades.planeSelectedCells and 
            app.game.computerBoard.playerAims[r][c] is None):
            if len(app.game.upgrades.planeSelectedCells) < 3:
                app.game.upgrades.planeSelectedCells.append((r, c))
                
                # When we have all 3 selections
                if len(app.game.upgrades.planeSelectedCells) == 3:
                    hitCount = 0
                    for row, col in app.game.upgrades.planeSelectedCells:
                        if app.game.computerBoard.playerFire(row, col):
                            hitCount += 1
                            app.explode.play()
                            app.game.points += 20
                        if shipHit:
                            app.game.points += 20
                            app.explode.play()
                            # Check if game is over after a hit
                            if app.game.checkAllComputerShipsSunk():
                                return
                        else:
                            app.splash.play()

                    
                    # Reset plane bomb state
                    app.game.upgrades.planeBombInUse = False
                    app.game.upgrades.planeSelectedCells = []
                    
                    # Check if game is over
                    if app.game.checkAllComputerShipsSunk():
                        return
                    
                    # Switch screens and let computer take turn
                    setActiveScreen('ships')
                    app.game.computerTurn()
                       
    else:
        if app.game.computerBoard.playerAims[r][c] is not None:
            return

        if app.game.upgrades.megaBombInUse:
            app.game.upgrades.megaBombInUse = False
            app.game.hoveredRow = None
            app.game.hoveredCol = None
            shipHit = app.game.upgrades.useMegaBomb(r, c, app.game.computerBoard)

        else:
            shipHit = app.game.computerBoard.playerFire(r, c)

        shipHit = app.game.computerBoard.playerFire(r, c)
        if shipHit:
            app.game.points += 20
            app.explode.play()
            
            # Check if ship was sunk
            shipName = app.game.computerBoard.mainBoard[r][c]
            if shipName not in app.game.hitShips:
                allCellsHit = True
                # Check all cells of this ship
                for row in range(app.game.rows):
                    for col in range(app.game.cols):
                        if (app.game.computerBoard.mainBoard[row][col] == shipName and 
                            app.game.computerBoard.playerAims[row][col] != 'X'):
                            allCellsHit = False
                            break
                if allCellsHit:
                    app.game.hitShips.append(shipName)
                    app.game.shipJustSunk = shipName
                    app.game.shipJustSunkSize = int(shipName[-1])
                    if int(shipName[-1]) == 6:
                        app.game.shipJustSunkSize = 5
                    
                    app.game.points += 50  
        else:
            app.splash.play()

        if app.game.checkAllComputerShipsSunk():
            setActiveScreen('gameOver')
            return


        setActiveScreen('ships')
        app.game.computerTurn()

def fire_onMouseMove(app, x, y):
    app.game.lineX = x
    app.game.lineY = y
    hoveredCell = cellinMouse(app, x, y)
    if hoveredCell:
        app.game.hoveredRow, app.game.hoveredCol = hoveredCell
    else:
        app.game.hoveredRow = None
        app.game.hoveredCol = None

    
######### SHOP SCREEN 
def drawBackground(app):
    drawImage(app.game.oceanImage, 0, 0, opacity=60)
    drawImage(app.game.soundIcon, 825, 15)
    if app.musicPaused:
        drawLine(825, 15, 865, 55, fill='red')
    drawImage(app.game.coinIcon, 10, 10)
    drawLabel(f'{app.game.points} POINTS', 95, 25, size=18, bold=True)
    drawRect(150, 50, app.width/2 + 150, app.height/2 + 150, 
            fill='steelBlue', opacity=90)
    drawRect(150, 50, app.width/2 + 150, app.height/2 + 150, 
            fill=None, border='white', borderWidth=3)


#mega bomb
def shop1_onKeyPress(app, key):
    allKeyPresses(app, key)

def shop1_redrawAll(app):
    drawBackground(app)

    drawLabel("MEGA BOMB", app.width/2, 80, size=45, bold=True, fill='white')
    drawImage(app.game.megaBombIcon, app.width/2 - 75, 120, width=150, height=150)

    drawRect(300, 280, 280, 70, fill='navy', opacity=40, border='white')
    drawLabel('Hit a 3x3 block of the grid', 450, 300, size=20, fill='white', bold=True)
    drawLabel('with just one play!', 450, 320, size=20, fill='white', bold=True)

    drawRect(350, 360, 200, 50, fill='navy', opacity=40, border='white')
    drawLabel(f"Cost: {20} Points", 450, 380, size=24, fill='white', bold=True)

    drawOval(650, 330, 100, 100, fill='forestGreen', border='white', borderWidth=2)
    drawLabel("BUY", 650, 330, size=24, bold=True, fill='white')

    if app.game.upgrades.megaBombs > 0:
        drawRect(170, 60, 60, 60, fill='royalBlue', border='white', borderWidth=2)
        drawLabel('USE', 197, 80, size=20, bold=True, fill='white')
        drawLabel(app.game.upgrades.megaBombs, 197, 100, fill='white', size=15, bold = True)

    drawImage(app.game.arrowIcon, 700, 400, rotateAngle=180)

    # Optional: Add highlight effects for buttons
    # You'll need to track mouse position to implement hover effects

def shop1_onMousePress(app, mouseX, mouseY):
    if 825 <= mouseX <= 865 and 30 <= mouseY <= 70:
       app.musicPaused = not app.musicPaused
       if app.musicPaused:
           app.sound.pause()
       else:
           app.sound.play(loop=True)
       return

    if distance(mouseX, mouseY, 650, 350) <= 50:
        if app.game.points >= 20:
            app.game.upgrades.megaBombs += 1
            app.game.points -= 20

    if mouseX >= 170 and mouseX <= 230 and mouseY >= 60 and mouseY <= 120:
        app.game.upgrades.megaBombInUse = True
        # app.game.upgrades.megaBombs -= 1
        setActiveScreen('fire')

    if mouseX >= 700 and mouseX <= 735 and mouseY >= 400 and mouseY <= 435:
        setActiveScreen('shop2')

#shield
def shop2_onKeyPress(app, key):
    allKeyPresses(app, key)

def shop2_redrawAll(app):
    drawBackground(app)
    drawImage(app.game.arrowIcon, 165, 400)
    drawImage(app.game.arrowIcon, 700, 400, rotateAngle = 180)

    drawLabel("SHIELD", app.width/2, 80, size=45, bold=True, fill='white')
    drawImage(app.game.shieldIcon, app.width/2 - 75, 120, width=150, height=150)

    drawRect(290, 280, 320, 70, fill='navy', opacity=40, border='white')
    drawLabel('Defend your ship(s) from getting', 450, 300, size=20, fill='white', bold=True)
    drawLabel('destroyed on the first hit!', 450, 320, size=20, fill='white', bold=True)

    drawRect(350, 360, 200, 50, fill='navy', opacity=40, border='white')
    drawLabel(f"Cost: {30} Points", 450, 380, size=24, fill='white', bold=True)

    drawOval(650, 330, 100, 100, fill='forestGreen', border='white', borderWidth=2)
    drawLabel("BUY", 650, 330, size=24, bold=True, fill='white')

    if app.game.upgrades.shields > 0:
        drawRect(170, 60, 60, 60, fill='royalBlue', border='white', borderWidth=2)
        drawLabel('USE', 197, 80, size=20, bold=True, fill='white')
        drawLabel(app.game.upgrades.shields, 197, 100, fill='white', size=15, bold = True)

def shop2_onMousePress(app, mouseX, mouseY):
    if 825 <= mouseX <= 865 and 30 <= mouseY <= 70:
       app.musicPaused = not app.musicPaused
       if app.musicPaused:
           app.sound.pause()
       else:
           app.sound.play(loop=True)
       return

    if distance(mouseX, mouseY, 650, 350) <= 50:
        if app.game.points >= 30:
            app.game.upgrades.shields += 1
            app.game.points -= 30

    if mouseX >= 170 and mouseX <= 230 and mouseY >= 60 and mouseY <= 120:
        app.game.upgrades.shieldInUse = True
        # app.game.upgrades.shields -= 1
        setActiveScreen('ships')

    if mouseX >= 700 and mouseX <= 735 and mouseY >= 400 and mouseY <= 435:
        setActiveScreen('shop3')
    elif mouseX >= 165 and mouseX <= 200 and mouseY >= 400 and mouseY <= 435:
        setActiveScreen('shop1')

#bouncer
def shop3_onKeyPress(app, key):
    allKeyPresses(app, key)

def shop3_redrawAll(app):
    drawBackground(app)
    drawImage(app.game.arrowIcon, 165, 400)
    drawImage(app.game.arrowIcon, 700, 400, rotateAngle = 180)

    drawLabel("BOUNCER", app.width/2, 80, size=45, bold=True, fill='white')
    drawImage(app.game.bouncerIcon, app.width/2 - 75, 120, width=150, height=150)

    drawRect(230, 280, 440, 70, fill='navy', opacity=40, border='white')
    drawLabel('Leave a selected cell untouched by bouncing', 450, 300, size=20, fill='white', bold=True)
    drawLabel("back an aim onto the computer's board", 450, 320, size=20, fill='white', bold=True)

    drawRect(350, 360, 200, 50, fill='navy', opacity=40, border='white')
    drawLabel(f"Cost: {40} Points", 450, 380, size=24, fill='white', bold=True)

    drawOval(650, 380, 100, 100, fill='forestGreen', border='white', borderWidth=2)
    drawLabel("BUY", 650, 380, size=24, bold=True, fill='white')

    if app.game.upgrades.bouncers > 0:
        drawRect(170, 60, 60, 60, fill='royalBlue', border='white', borderWidth=2)
        drawLabel('USE', 197, 80, size=20, bold=True, fill='white')
        drawLabel(app.game.upgrades.bouncers, 197, 100, fill='white', size=15, bold = True)


def shop3_onMousePress(app, mouseX, mouseY):
    if 825 <= mouseX <= 865 and 30 <= mouseY <= 70:
       app.musicPaused = not app.musicPaused
       if app.musicPaused:
           app.sound.pause()
       else:
           app.sound.play(loop=True)
       return

    if distance(mouseX, mouseY, 650, 380) <= 50:
        if app.game.points >= 40:
            app.game.upgrades.bouncers += 1
            app.game.points -= 40

    if mouseX >= 170 and mouseX <= 230 and mouseY >= 60 and mouseY <= 120:
        app.game.upgrades.bouncerInUse = True
        app.game.upgrades.selectingBouncers = True
        app.game.upgrades.bouncersToPlace = 3
        setActiveScreen('ships')

    if mouseX >= 700 and mouseX <= 735 and mouseY >= 400 and mouseY <= 435:
        setActiveScreen('shop4')
    elif mouseX >= 165 and mouseX <= 200 and mouseY >= 400 and mouseY <= 435:
        setActiveScreen('shop2')

#plane bomb
def shop4_onKeyPress(app, key):
    allKeyPresses(app, key)

def shop4_redrawAll(app):

    drawBackground(app)

    drawLabel("TRIPLE PLANE BOMB", app.width/2, 80, size=45, bold=True, fill='white')
    drawImage(app.game.planeBombIcon, app.width/2 - 75, 120, width=150, height=150)

    drawRect(310, 280, 280, 70, fill='navy', opacity=40, border='white')
    drawLabel('Launch a plane in one play', 450, 300, size=20, fill='white', bold=True)
    drawLabel('and fire at 3 different cells', 450, 320, size=20, fill='white', bold=True)

    drawRect(350, 360, 200, 50, fill='navy', opacity=40, border='white')
    drawLabel(f"Cost: {50} Points", 450, 380, size=24, fill='white', bold=True)

    drawOval(650, 350, 100, 100, fill='forestGreen', border='white', borderWidth=2)
    drawLabel("BUY", 650, 350, size=24, bold=True, fill='white')

    if app.game.upgrades.planeBomb > 0:
        drawRect(170, 110, 60, 60, fill='royalBlue', border='white', borderWidth=2)
        drawLabel('USE', 197, 130, size=20, bold=True, fill='white')
        drawLabel(app.game.upgrades.planeBomb, 197, 150, fill='white', size=15, bold = True)

    drawImage(app.game.arrowIcon, 165, 400)


def shop4_onMousePress(app, mouseX, mouseY):
    if 825 <= mouseX <= 865 and 30 <= mouseY <= 70:
       app.musicPaused = not app.musicPaused
       if app.musicPaused:
           app.sound.pause()
       else:
           app.sound.play(loop=True)
       return

    if distance(mouseX, mouseY, 650, 350) <= 50:
        if app.game.points >= 50:
            app.game.upgrades.planeBomb += 1
            app.game.points -= 50

    if mouseX >= 170 and mouseX <= 230 and mouseY >= 110 and mouseY <= 170:
        app.game.upgrades.planeBombInUse = True
        app.game.upgrades.planeSelectedCells = []
        app.game.upgrades.planeBomb -= 1
        setActiveScreen('fire')

    if mouseX >= 165 and mouseX <= 200 and mouseY >= 400 and mouseY <= 435:
        setActiveScreen('shop3')
    

######### GAME OVER SCREEN 
def gameOver_redrawAll(app):
    drawImage(app.game.oceanImage, 0, 0, opacity=60)
    
    if app.game.playerWon:
        drawLabel("VICTORY!", app.width/2, app.height/2-50, size=50, bold=True, fill='green')
        drawLabel("You sunk all enemy ships!", app.width/2, app.height/2+20, size=30, fill='darkGreen')
    else:
        drawLabel("DEFEAT", app.width/2, app.height/2-50, size=50, bold=True, fill='red')
        drawLabel("All your ships were sunk!", app.width/2, app.height/2+20, size=30, fill='darkRed')
    
    drawRect(app.width/2-100, app.height/2+100, 200, 50, fill='steelBlue')
    drawLabel("Play Again", app.width/2, app.height/2+125, size=25, fill='white')

def gameOver_onMousePress(app, mouseX, mouseY):
    if (mouseX >= app.width/2-100 and mouseX <= app.width/2+100 and 
        mouseY >= app.height/2+100 and mouseY <= app.height/2+150):
        resetGame(app)
        setActiveScreen('start')

def resetGame(app):
    app.game = Game(app.width, app.height)
    app.musicPaused = False
    app.sound.play(loop=True)



def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5



def main():
    runAppWithScreens('start')

main()




    


