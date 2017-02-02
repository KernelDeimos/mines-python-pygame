import pygame.freetype as fonts

import sys, pygame

"""
This module contains the Minesweeper board

- GameBoardTile
- GameBoard
"""

class GameBoardTile:
	def __init__(self):
		self.isMine = False
		self.isVisible = False
		self.isFlagged = False

		self.value = 0

		self.font = None

	def is_mine(self, value=None):
		"""
		Check or modify mine presence of tile

		Parameters
		----------
		value : bool
			True or False to set/unset mine, None to check
		
		Returns
		-------
		bool
			Whether mine is present, or if presence was changed
		"""
		if value is None: return self.isMine
		elif self.isMine != value:
			self.isMine = value
			return True
		else:
			return False

	def is_visible(self, value=None):
		"""
		Check or modify visibility of tile

		Parameters
		----------
		value : bool
			True or False to set/unset visible, None to check
		
		Returns
		-------
		bool
			Whether tile is visible, or if visibility was changed
		"""
		if value is None: return self.isVisible
		elif self.isVisible != value:
			self.isVisible = value
			return True
		else:
			return False

	def set_value(self, value):
		"""
		Set the number to be displayed on this tile

		Parameters
		----------
		value : int
			Number to be displayed on tile
		"""
		self.value = value
		self.is_visible(True)

	def toggle_flag(self):
		if self.isFlagged:
			self.isFlagged = False
		else:
			self.isFlagged = True

	def is_flagged(self):
		return self.isFlagged

	def draw(self, size=40):
		"""
		Render the tile given its current state

		Returns
		----------
		pygame.Surface
			Surface with a the rendered tile
		"""

		if self.font is None:
			self.font = fonts.SysFont('Courier New', size/2, True)

		# Create surface
		surf = pygame.Surface((size,size))

		# Fill Surface
		if not self.isVisible:
			surf.fill((90,90,90))
		else:
			surf.fill((255,255,255))

		# Generate text for tile
		t_surf, t_rect = None, None
		if self.isVisible:
			# Display M on an exposed mine
			if self.isMine:
				t_surf, t_rect = self.font.render('M', (255,0,0))
			# Display a value if value is set
			elif self.value != 0:
				t_surf, t_rect = self.font.render(str(self.value), (0,255,0))
		elif self.isFlagged:
			# Draw a neat flag
			xLeft = size / 5
			xRigh = 4*size/5
			points = [
				(xRigh, 1*size/5),
				(xLeft, 3*size/10),
				(xRigh, 2*size/5)
			]
			pygame.draw.polygon(surf, (255,0,0), points)
			pygame.draw.line(surf, (0,0,0),
				(xRigh,1*size/5),
				(xRigh,4*size/5),
				2
			)
			
		# Draw text on tile
		if t_surf is not None:
			y = size / 2 - t_rect[3] / 2
			x = size / 2 - t_rect[2] / 2
			surf.blit(t_surf, (x, y))

		# Draw border
		pygame.draw.rect(surf, (0,0,0), (0,0,size,size), 2)

		return surf

class GameBoard:
	def __init__(self, grid, width, height, cellSize=40):
		self.grid = grid
		self.width = width
		self.height = height

		self.cellSize = cellSize

	def get_pixel_resolution(self):
		return (
			self.width*self.cellSize,
			self.height*self.cellSize
		)

	def get_cell(self, row, col):
		return self.grid[row][col]

	def get_grid_position_from_pixel(self, x, y):
		"""
		Returns the grid coordinates at a pixel value

		Returns
		-------
		tuple
			(row,col)
		None
			If pixel coordinate is not a grid cell
		"""
		row = y / self.cellSize
		col = x / self.cellSize

		if not self._is_valid_cell(row,col):
			return None

		return (row, col)

	def click_cell(self, row, col):
		"""
		Activates the tile at given grid coordinates

		Grid coordinates must be a valid location of a
		cell with the current grid size.

		Returns
		-------
		bool
			False if not a mine, True if a mine
		"""
		cell = self.grid[row][col]

		if cell.is_flagged():
			return False

		if cell.is_mine():
			cell.is_visible(True)
			return True

		self.clear_cell(row, col)
		return False

	def flag_cell(self, row, col):
		"""
		Toggles a flag on a cell if possible
		"""
		cell = self.grid[row][col]
		if cell.is_visible(): return
		cell.toggle_flag()

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

				cellSurf = cell.draw(self.cellSize)
				surf.blit(cellSurf, (x,y))
		return surf