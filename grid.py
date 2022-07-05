import random

import pygame

from cell import Cell


class Grid:
    cells = []  # 10 columns x 22 rows (top 2 rows hidden)
    current_cell = None  # Tuple of indices for cell to move on updates, None if cell at bottom

    def __init__(self):
        for i in range(10):
            self.cells.append([])
            for _ in range(22):
                self.cells[i].append(None)


    def add_cell(self):
        # Add a cell in any empty spot in the first row
        idx = random.randint(0, 9)
        if self.cells[idx][0] is not None:
            # TODO: You lose!
            pass
        self.current_cell = [idx, 0]
        color_values = [0, 255]
        color_tuple = (random.choice(color_values), random.choice(color_values), random.choice(color_values))
        self.cells[idx][0] = Cell(color_tuple)

    
    def new_cell_needed(self):
        return self.current_cell is None


    def move_current_cell_left(self):
        # Move the cell left one column
        current_col = self.current_cell[0]
        current_row = self.current_cell[1]
        the_cell = self.cells[current_col][current_row]
        self.cells[current_col][current_row] = None
        self.current_cell[0] = max(0, self.current_cell[0] - 1)
        self.cells[self.current_cell[0]][self.current_cell[1]] = the_cell


    def move_current_cell_right(self):
        # Move the cell right one column
        current_col = self.current_cell[0]
        current_row = self.current_cell[1]
        the_cell = self.cells[current_col][current_row]
        self.cells[current_col][current_row] = None
        self.current_cell[0] = min(9, self.current_cell[0] + 1)
        self.cells[self.current_cell[0]][self.current_cell[1]] = the_cell


    def move_current_cell_down(self):
        # See if the spot directly under the current cell is occupied
        current_col = self.current_cell[0]
        current_row = self.current_cell[1]
        if self.cells[current_col][current_row + 1] is not None:
            # Occupied, we're done
            self.current_cell = None
        else:
            # Move the cell down one row
            the_cell = self.cells[current_col][current_row]
            self.cells[current_col][current_row] = None
            self.current_cell[1] = current_row + 1
            self.cells[self.current_cell[0]][self.current_cell[1]] = the_cell
            # Signal for new cell if we're at the bottom
            if self.current_cell[1] == 21:
                self.current_cell = None


    def draw(self, window):
        CELL_SIZE = 25
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if cell is None:
                    continue
                rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, cell.color, rect)


    def clear_completed_rows(self):
        for idx, row in enumerate(self.cells):
            if all(lambda cell: cell is not None for cell in row):
                for i in range(len(row)):
                    row[i] = None
                self.cells[idx] = row
