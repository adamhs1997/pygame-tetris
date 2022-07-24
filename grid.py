import random

import pygame

from cell import Cell


class Grid:
    cells = []  # 10 columns x 22 rows (top 2 rows hidden)
    current_shape = None  # Tuple of indices for cell to move on updates, None if cell at bottom

    def __init__(self):
        for i in range(10):
            self.cells.append([])
            for _ in range(22):
                self.cells[i].append(None)


    def generate_shape(self):
        # Dumb and inefficient...
        shape_cells = []
        seed_cell = [random.randint(0, 9), 0]
        for _ in range(4):
            if self.cells[seed_cell[0]][seed_cell[1]] is not None:
                # TODO: You lose!
                pass
            else:
                shape_cells.append(seed_cell)
                # Search for valid neighbor, never look up since will never be valid
                step_candidates = [
                    [seed_cell[0] - 1, seed_cell[1]],  # Left
                    [seed_cell[0] + 1, seed_cell[1]],  # Right
                    [seed_cell[0], seed_cell[1] + 1]   # Down
                ]
                for _ in range(3):
                    step_idx = random.randint(0, len(step_candidates) - 1)
                    step_candidate = step_candidates[step_idx]
                    if not (0 <= step_candidate[0] <= 9)\
                        or not step_candidate[1] > 0\
                        or self.cells[step_candidate[0]][step_candidate[1]] is not None\
                        or step_candidate in shape_cells:
                        del(step_candidates[step_idx])
                    else:
                        seed_cell = step_candidate
                        break
        return shape_cells


    def add_shape(self):
        # Add a cell in any empty spot in the first row
        idx = random.randint(0, 9)
        if self.cells[idx][0] is not None:
            # TODO: You lose!
            pass
        self.current_shape = self.generate_shape()
        valid_colors = [[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255]]
        color_tuple = random.choice(valid_colors)
        for cell in self.current_shape:
            self.cells[cell[0]][cell[1]] = Cell(color_tuple)

    
    def new_cell_needed(self):
        return self.current_shape is None


    def move_current_cell_left(self):
        # Check that each cell can be moved left
        for current_cell in self.current_shape:
            current_col = current_cell[0]
            current_row = current_cell[1]

            # Check that the shape isn't at the left side
            if current_col == 0:
                return

            # Check to see if the next cell is occupied AND make sure
            #  that cell isn't part of this shape
            if self.cells[current_col - 1][current_row] is not None\
                and [current_col - 1, current_row] not in self.current_shape:
                # Occupied, we're done
                return

        # Sort the shape so we move the left side first
        # This prevents me from overwriting cells that were already moved
        self.current_shape.sort(key=lambda cell: cell[0])

        # Update the current shape
        for i, current_cell in enumerate(self.current_shape):
            # Move the cell over left
            current_col = current_cell[0]
            current_row = current_cell[1]
            the_cell = self.cells[current_col][current_row]
            self.cells[current_col][current_row] = None
            self.current_shape[i][0] = current_col - 1
            self.cells[self.current_shape[i][0]][self.current_shape[i][1]] = the_cell
            

    def move_current_cell_right(self):
        # Check that each cell can be moved right
        for current_cell in self.current_shape:
            current_col = current_cell[0]
            current_row = current_cell[1]

            # Check that the shape isn't at the right side
            if current_col == 9:
                return

            # Check to see if the next cell is occupied AND make sure
            #  that cell isn't part of this shape
            if self.cells[current_col + 1][current_row] is not None\
                and [current_col + 1, current_row] not in self.current_shape:
                # Occupied, we're done
                return

        # Sort the shape so we move the right side first
        # This prevents me from overwriting cells that were already moved
        self.current_shape.sort(reverse = True, key=lambda cell: cell[0])

        # Update the current shape
        for i, current_cell in enumerate(self.current_shape):
            # Move the cell over right
            current_col = current_cell[0]
            current_row = current_cell[1]
            the_cell = self.cells[current_col][current_row]
            self.cells[current_col][current_row] = None
            self.current_shape[i][0] = current_col + 1
            self.cells[self.current_shape[i][0]][self.current_shape[i][1]] = the_cell


    def move_current_cell_down(self):
        # Check that each cell can be moved down
        for current_cell in self.current_shape:
            current_col = current_cell[0]
            current_row = current_cell[1]
            # Check to see if the next lower cell is occupied AND make sure
            #  that cell isn't part of this shape
            if self.cells[current_col][current_row + 1] is not None\
                and [current_col, current_row + 1] not in self.current_shape:
                # Occupied, we're done
                self.current_shape = None
                return

        # Sort the shape so we move the bottom first
        # This prevents me from overwriting cells that were already moved
        self.current_shape.sort(reverse = True, key=lambda cell: cell[1])

        # Update the current shape
        for i, current_cell in enumerate(self.current_shape):
            # Move the cell down one row
            current_col = current_cell[0]
            current_row = current_cell[1]
            the_cell = self.cells[current_col][current_row]
            self.cells[current_col][current_row] = None
            self.current_shape[i][1] = current_row + 1
            self.cells[self.current_shape[i][0]][self.current_shape[i][1]] = the_cell

        # Signal for new cell if we're at the bottom (if any cell at position 21)
        if any(map(lambda cell: cell[1] == 21, self.current_shape)):
            self.current_shape = None


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
