import mines.minesboard
import unittest

class TestClearingAlgorithm(unittest.TestCase):

	def test_detection_of_surrounding_cells(self):
		"""Test detection of surrounding cells"""

		# Create testing board
		board = self._create_test_board(8,8)

		# Test 8 surrounding a middle square
		middle = board._get_surrounding_cells(4,4)
		self.assertEqual(len(middle),8)

		# Test 5 surrounding an edge square
		edge = board._get_surrounding_cells(0,4)
		self.assertEqual(len(edge),5)

		# Test 3 surrounding a corner square
		corner = board._get_surrounding_cells(0,0)
		self.assertEqual(len(corner),3)

	def test_correct_number_of_mines(self):
		"""Test counting of surrounding mines"""
		# Create testing board
		board = self._create_test_board(8,8)
		self._add_mines_sample_1(board)

		# Test one mine around 4,4
		cells = board._get_surrounding_cells(4,4)
		mines = board._get_mine_count(cells)
		self.assertEqual(mines,1)

		# Test 3 mines around 3,1
		cells = board._get_surrounding_cells(3,1)
		mines = board._get_mine_count(cells)
		self.assertEqual(mines,3)


	def _create_test_board(self, row=8, col=8):
		row = 8
		col = 8
		# Generate the grid
		rows = []
		for r in range(row):
			cells = []
			rows.append(cells)

			for c in range(col):
				tile = mines.minesboard.GameBoardTile()
				cells.append(tile)
		# Create game board
		board = mines.minesboard.GameBoard(rows,row,col)
		return board

	def _add_mines_sample_1(self, board):
		mine_coordinates = [
			(0,4),(2,0),(2,1),
			(3,0),(5,0),(5,1),
			(5,5),(5,6),(6,5),
			(7,2)
			]
		for coord in mine_coordinates:
			cell = board.get_cell(coord[0],coord[1])
			cell.is_mine(True)

if __name__ == '__main__':
 	unittest.main()
