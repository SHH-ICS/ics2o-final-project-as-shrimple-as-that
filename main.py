import pygame, random
pygame.font.init()
pygame.init()

#####################

#global variables
ScrW = 800
ScrH = 700
PlyW = 300
PlyH = 600
BlockSize = 30

TopLeftX = (ScrW - PlyW) // 2
TopLeftY = ScrH - PlyH

#surface for image



#shapes n stuff


S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

Shapes = [S, Z, I, O, J, L, T]
ShapeColors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
ShapeTextures = ['blockGreen.png', 'blockRed.png', 'blockTeal.png', 'blockYellow.png', 'blockBlue.png', 'blockOrange.png', 'blockMagenta.png']

##################

class Piece(object):
	def __init__(self, x, y, Shape):
		self.x = x
		self.y = y
		self.shape = Shape
		self.color = ShapeColors[Shapes.index(Shape)]
		self.texture = ShapeTextures[Shapes.index(Shape)]
		self.rotation = 0

def createGrid(locked_pos = {}): 
	grid = [[(0, 0, 0)for x in range(10)] for x in range(20)]

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if (j, i) in locked_pos:
				c = locked_pos[(j, i)]
				grid[i][j] = c
	return grid

def convertShapeFormat(Shape): # turns text into shapes
	positions = []
	format = Shape.shape[Shape.rotation % len(Shape.shape)]

	for i, line in enumerate(format):
		row = list(line)
		for j, column in enumerate(row):
			if column == '0':
				positions.append((Shape.x + j, Shape.y + i))

	for i, pos in enumerate(positions):
		positions[i] = (pos[0] - 2, pos[1] - 4)

	return positions
		
def validSpace(Shape, grid):#potentially may cause errors for textures \/
	accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range (20)]
	accepted_pos = [j for sub in accepted_pos for j in sub] #list flattening
	
	formatted = convertShapeFormat(Shape)

	for pos in formatted:
		if pos not in accepted_pos:
			if pos[1] > -1:
				return False
	return True

def checkLost(positions):
	for pos in positions:
		x, y = pos
		if y < 1:
			return True
	
	return False

def getShape():
	global Shapes, ShapeColors
	
	return Piece(5, 0, random.choice(Shapes))

def drawTextMiddle(surface, text, size, color):
	font = pygame.font.SysFont("Arial", size, bold=True)
	label = font.render(text, 1, color)

	surface.blit(label,(TopLeftX + PlyW/2 - (label.get_width()/2), TopLeftY + PlyH/2 - label.get_height()/2))

def drawGrid(surface, grid):
	sx = TopLeftX
	sy = TopLeftY

	for i in range(len(grid)):
		pygame.draw.line(surface, (128, 128, 128), (sx, sy+i*BlockSize), (sx+PlyW, sy+i*BlockSize))
		for j in range (len(grid[i])):
			pygame.draw.line(surface, (128, 128, 128), (sx + j*BlockSize, sy), (sx+j*BlockSize, sy+PlyH))

def clearRows(grid, locked):

	inc = 0
	for i in range(len(grid)-1, -1, -1):
		row = grid[i]
		if (0,0,0) not in row:
			inc += 1
			ind = i
			for j in range(len(row)):
				try:
					del locked[(j, i)]
				except:
					continue

	if inc > 0:
		for key in sorted(list(locked), key = lambda x: x[1])[::-1]: 
			x, y = key
			if y < ind:
				newKey = (x, y + inc)
				locked[newKey] = locked.pop(key)

	return inc

def drawNextShape(Shape, surface):

	
	font = pygame.font.SysFont('comicsans', 30)
	label = font.render('Next Shape', 1, (255,255,255))

	sx = TopLeftX + PlyW + 50
	sy = TopLeftY + PlyH/2 - 100
	
	format = Shape.shape[Shape.rotation % len(Shape.shape)]

	for i, line in enumerate(format):
		row = list(line)
		for j, column in enumerate(row):
			if column == '0':
				pygame.draw.rect(surface, Shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

	surface.blit(label, (sx + 10, sy- 30))
	
def updateScore(nscore):

	score = highScore()
	
	with open('scores.txt', 'r') as f:
		lines = f.readlines()
		score = lines[0].strip('\n')

	with open('scores.txt', 'w') as f:
		if int(score) > nscore:
			f.write(str(score))
		else:
			f.write(str(nscore))

def highScore():
	with open('scores.txt', 'r') as f:
		lines = f.readlines()
		score = lines[0].strip('\n')

	return score

def drawWindow(surface, grid, score=0, hScore = 0):
	surface.blit(imgSur, (0, 0))

	pygame.font.init()
	font = pygame.font.SysFont('comicsans', 60)
	label = font.render('BlockFall', 1, (255,255,255))

	surface.blit(label, (TopLeftX + PlyW/2 - (label.get_width()/2), 30))

	sx = TopLeftX + PlyW + 50
	sy = TopLeftY + PlyH/2 - 100
	
	pygame.font.init()
	font = pygame.font.SysFont('comicsans', 30)
	label = font.render('Score: ' + str(score), 1, (255,255,255))

	surface.blit(label, (sx - PlyW - 200, sy - 120))

	pygame.font.init()
	font = pygame.font.SysFont('comicsans', 30)
	label = font.render('High Score: ' + str(hScore), 1, (255,255,255))

	surface.blit(label, (sx - PlyW - 200, sy - 90))
	
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			pygame.draw.rect(surface, grid[i][j], (TopLeftX + j*BlockSize, TopLeftY + i*BlockSize, BlockSize, BlockSize), 0)

	pygame.draw.rect(surface, (254, 1, 1), (TopLeftX, TopLeftY, PlyW, PlyH), 4)
	
	drawGrid(surface, grid)
	
#def textureShape(surface, piece): 
	#ArrayColors = pygame.PixelArray[x, y]
	
	#imgLoad = pygame.image.load(piece.texture).convert()
	#surface.blit(imgLoad, (piece.x, piece.y))

def main(win):
	disHighScore = highScore()
	
	locked_positions = {}
	grid = createGrid(locked_positions)
	
	changePiece = False
	run = True
	currentPiece = getShape()
	nextPiece = getShape()
	clock = pygame.time.Clock()
	fallTime = 0
	fallSpeed = 0.27
	levelTime = 0
	score = 0

	while run:
		grid = createGrid(locked_positions)
		fallTime += clock.get_rawtime()
		levelTime += clock.get_rawtime()
		clock.tick()

		if levelTime/1000 > 5:
			levelTime = 0
			if fallSpeed > 0.12:
				fallSpeed -= 0.005
		
		if fallTime/1000 > fallSpeed:
			fallTime=0
			currentPiece.y += 1
			if not(validSpace(currentPiece, grid)) and currentPiece.y > 0:
				currentPiece.y -= 1
				changePiece = True
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.display.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					currentPiece.x -= 1
					if not (validSpace(currentPiece, grid)):
						currentPiece.x += 1
				if event.key == pygame.K_RIGHT:
					currentPiece.x += 1
					if not (validSpace(currentPiece, grid)):
						currentPiece.x -= 1
				if event.key == pygame.K_DOWN:
					currentPiece.y += 1
					if not (validSpace(currentPiece, grid)):
						currentPiece.y -= 1
				if event.key == pygame.K_UP:
					currentPiece.rotation += 1
					if not(validSpace(currentPiece, grid)):
						currentPiece.rotation -=1
				if event.key == pygame.K_SPACE:
					while validSpace(currentPiece, grid):
						currentPiece.y += 1
					currentPiece.y -= 1

		ShapePos = convertShapeFormat(currentPiece) #adds color, probably can use this for textures with some fancy shmanchy stuff (replace colors in ShapeColors with texture files, should automate it all with slight tweaking)
		
		for i in range(len(ShapePos)):
			x, y = ShapePos[i]
			if y > -1:
				grid[y][x] = currentPiece.color

		if changePiece:
			for pos in ShapePos:
				p = (pos[0], pos[1])
				locked_positions[p] = currentPiece.color
			currentPiece = nextPiece
			nextPiece = getShape()
			changePiece = False
			#textureShape(win, nextPiece)
			score += clearRows(grid, locked_positions) ** 2 * 10

		
		
		drawWindow(win, grid, score, disHighScore)
		drawNextShape(nextPiece, win)
		pygame.display.update()

		if checkLost(locked_positions):
			drawTextMiddle(win, "YOU SUCK", 80, (255,255,255))
			pygame.display.update()
			pygame.time.delay(1500)
			run = False
			updateScore(score)
		
def mainMenu(win):
	run = True
	while run:
		win.fill((0, 0, 0))
		drawTextMiddle(win, 'Press any key to start', 60, (255,255,255))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				main(win)
	
	pygame.display.quit

win = pygame.display.set_mode((ScrW, ScrH))
imgSur = pygame.display.set_mode((ScrW, ScrH))
imgSur = pygame.image.load("tetrisBG.png").convert()
pygame.display.set_caption('BlockFall')

mainMenu(win)
