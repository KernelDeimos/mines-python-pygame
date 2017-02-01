import sys, pygame
import math

import minesboard

class GameMenu:
	pass

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
				tile = minesboard.GameBoardTile()
				cells.append(tile)

		# Create board object
		board = minesboard.GameBoard(rows, col, row)

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
