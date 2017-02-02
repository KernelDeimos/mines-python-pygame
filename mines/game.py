import sys, pygame
import pygame.freetype as fonts

import time

import minesboard

# import Tkinter # For error dialogs
import Tkinter, tkMessageBox

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

		self.running = True

		self.resolution = 1280, 1024
	def run(self):
		win = False

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: return
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Get grid position
					row, col = self.board.get_grid_position_from_pixel(
						event.pos[0], event.pos[1]
					)

					# Clear button
					if event.button == 1:
						# Attempt to clear that tile
						result = self.board.click_cell(row, col)

						# If a mine was chosen, end the game
						if result == True:
							self.running = False

					# Flag button
					elif event.button == 3:
						self.board.flag_cell(row, col)

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

		# Clear the screen
		self.screen.fill((0,0,0))

		# Display win/lose message
		font = self.font = fonts.SysFont('Courier New', 60, True)

		message, colour = None, None

		if win:
			message = "You Win!"
			colour = (0,255,0)
		else:
			message = "You Lose :/"
			colour = (255,0,0)

		# Draw Text
		t_surf, t_rect = self.font.render(message,colour)
		y = self.resolution[1] / 2 - t_rect[3] / 2
		x = self.resolution[0] / 2 - t_rect[2] / 2
		self.screen.blit(t_surf, (x, y))

		# Flip the screen
		pygame.display.flip()

		# Wait a few seconds
		time.sleep(2)
