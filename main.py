 
import sys, pygame
import pygame.freetype as fonts
import random
import math

class GameMenu:
	pass

class GameBoardTile:
	def __init__(self):
		self.isMine = False
		self.isVisible = False

		self.value = 0

		self.font = fonts.SysFont('Courier New', 20, True)
	def is_mine(self, value=None):
		if value is None: return self.isMine
		elif self.isMine != value:
			self.isMine = value
			return True
		else:
			return False
	def set_value(self, value):
		self.value = value
		self.is_visible(True)
	def is_visible(self, value=None):
		if value is None: return self.isVisible
		elif self.isVisible != value:
			self.isVisible = value
			return True
		else:
			return False
	def draw(self, size=40):

		# Create surface
		surf = pygame.Surface((size,size))
		# Fill Surface
		if not self.isVisible:
			surf.fill((90,90,90))
		else:
			surf.fill((255,255,255))
		# Draw Number
		t_surf, t_rect = None, None
		if self.isMine:
			t_surf, t_rect = self.font.render('M', (255,0,0))
		if self.isVisible:
			if self.isMine:
				t_surf, t_rect = self.font.render('M', (255,0,0))
			elif self.value != 0:
				t_surf, t_rect = self.font.render(str(self.value), (0,255,0))
		if t_surf is not None:
			y = size / 2 - t_rect[3] / 2
			x = size / 2 - t_rect[2] / 2
			surf.blit(t_surf, (x, y))

		# Draw border
		pygame.draw.rect(surf, (0,0,0), (0,0,size,size), 2)

		return surf

class GameBoard:
	def __init__(self, grid, width, height):
		self.grid = grid
		self.width = width
		self.height = height

		self.cellSize = 40
	def get_cell(self, row, col):
		return self.grid[row][col]
	def click_cell_at_pixel(self, x, y):
		row = y / self.cellSize
		col = x / self.cellSize

		if not self._is_valid_cell(row,col):
			return

		self.click_cell(row, col)

	# precondition: valid cell
	def click_cell(self, row, col):
		cell = self.grid[row][col]
		if cell.is_mine():
			cell.is_visible(True)
			return True

		self.clear_cell(row, col)

	def clear_cell(self, row, col):
		# Fetch surrounding cells
		surrounding = self._get_surrounding_cells(row, col)
		# Count mines and update this cell
		mine_count = self._get_mine_count(surrounding)
		cell = self.get_cell(row, col)
		cell.set_value(mine_count)
		cell.is_visible(True)
		# If no mines around, clear surrounding cells
		if mine_count == 0:
			self.clear_cells(surrounding)

	def clear_cells(self, cells):
		for cellTuple in cells:
			row = cellTuple[0]
			col = cellTuple[1]
			cell = self.get_cell(row, col)
			if not cell.is_visible():
				self.clear_cell(row, col)

	def _is_valid_cell(self, row, col):
		if row < self.height and col < self.width \
		and row >= 0 and col >= 0:
			return True
		return False

	def _get_surrounding_cells(self, row, col):
		cells = []
		for i in (-1,0,1):
			for j in (-1,0,1):
				# No not include surrounded cell
				if i == j == 0:
					continue
				# Get position of neighbour
				r, c = row+i, col+j
				if not self._is_valid_cell(r, c):
					continue
				else:
					cells.append((row+i,col+j))
		return cells

	# @param cells  Surrounding cells
	def _get_mine_count(self, cells):
		mines = 0
		for cellTuple in cells:
			row = cellTuple[0]
			col = cellTuple[1]
			cell = self.get_cell(row,col)
			if cell.is_mine():
				mines += 1
		return mines

	def _set_number(self, row, col):
		if row >= self.height or col >= self.width \
		or row < 0 or col < 0:
			return

		checks = []
		mines = 0
		for i in (-1,0,1):
			for j in (-1,0,1):
				if i == j == 0: continue
				cell = self.get_cell(row,col)
				checks.append((row+i,col+j,cell))
				if cell.is_mine():
					mines += 1

		thisCell = self.get_cell(row, col)
		thisCell.set_value(mines)

		if mines == 0:
			for check in checks:
				row = check[0]
				col = check[1]
				cell = check[2]
				if not cell.is_visible():
					self._set_number(row,col)

	def draw(self):
		width, height, size = self.width, self.height, self.cellSize
		surf = pygame.Surface((size*width,size*height))
		for r, row in enumerate(self.grid):
			for c, cell in enumerate(row):
				y = r*size
				x = c*size

				cellSurf = cell.draw()
				surf.blit(cellSurf, (x,y))
		return surf

class GameInstanceBuilder:
	DIFFICULTY_EASY = 1
	DIFFICULTY_MEDIUM = 2
	DIFFICULTY_HARD = 3
	DIFFICULTY_EXPERT = 4

	def __init__(self, rand, screen, clock):
		self.rand = rand
		self.screen = screen
		self.clock = clock

	def make_instance(self, difficulty):
		# Determine board configuration
		row, col, mines = None, None, None
		if difficulty == self.DIFFICULTY_EASY:
			row, col, mines = 8, 8, 10
		elif difficulty == self.DIFFICULTY_MEDIUM:
			row, col, mines = 16, 16, 40
		elif difficulty == self.DIFFICULTY_HARD:
			row, col, mines = 16, 30, 99
		elif difficulty == self.DIFFICULTY_EXPERT:
			row, col, mines = 24, 30, 200
		else:
			raise Exception ("Invalid board difficulty!")

		# Generate the grid
		rows = []
		for r in range(row):
			cells = []
			rows.append(cells)

			for c in range(col):
				tile = GameBoardTile()
				cells.append(tile)

		# Create board object
		board = GameBoard(rows, col, row)

		# Populate board with mines
		placedMines = 0
		while placedMines < mines:
			ro = self.rand.randrange(0,row)
			co = self.rand.randrange(0,col)

			if board.get_cell(ro,co).is_mine(True):
				placedMines += 1

		return GameInstance(board, self.screen, self.clock)

class GameInstance:
	def __init__(self, board, screen, clock):
		self.board = board
		self.screen = screen
		self.clock = clock
	def run(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: return
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.board.click_cell_at_pixel(
						event.pos[0], event.pos[1]
					)
			# Clear the screen
			self.screen.fill((0,0,0))
			# Draw the board
			boardSurf = self.board.draw()
			# Blit the board
			self.screen.blit(boardSurf,(0,0))
			# Flip the screen
			pygame.display.flip()
			# Wait a little
			self.clock.tick(60)

class Application:
	def main(self):
		pygame.init()
		self.resolution = 600, 800

		self.screen = pygame.display.set_mode(self.resolution)

		rec = pygame.Rect(100,100,40,40)
		speed = [2,2]

		width = self.resolution[0]
		height = self.resolution[1]

		clock = pygame.time.Clock()

		builder = GameInstanceBuilder(random, self.screen, clock)
		gameInstance = builder.make_instance(GameInstanceBuilder.DIFFICULTY_EASY)

		gameInstance.run()

		# while 1:
		# 	for event in pygame.event.get():
		# 		if event.type == pygame.QUIT: sys.exit()

		# 	rec = rec.move(speed)
		# 	if rec.left < 0 or rec.right > width: speed[0] = -speed[0]
		# 	if rec.top < 0 or rec.bottom > height: speed[1] = -speed[1]

		# 	self.screen.fill((0,0,0))
		# 	pygame.draw.rect(self.screen, (255,255,255), rec)
		# 	pygame.display.flip()
		# 	clock.tick(60)

if __name__ == '__main__':
	app = Application()
	app.main()
