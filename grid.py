from collections import Counter
from copy import deepcopy
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
        # Shapes can only be cleared when the last shape is at the bottom
        #  i.e., when a new shape is needed
        if not self.new_cell_needed():
            return

        for row_num in range(22):
            # If the same row in every column is filled, it should be cleared
            if all(list(col[row_num] is not None for col in self.cells)):
                for col_num in range(len(self.cells)):
                    # Clear the row
                    self.cells[col_num][row_num] = None

                    # Move down all the cells above the cleared row in the column
                    # Move down to up so we don't overwrite cells
                    for upper_row_num in list(reversed(range(row_num))):
                        cell = self.cells[col_num][upper_row_num]
                        self.cells[col_num][upper_row_num] = None
                        self.cells[col_num][upper_row_num + 1] = cell


    def rotate_shape(self):
        # Number the cells right to left, top to bottom
        # Pivot on cell 2 (it stays in same place)
        # two of the cells will be easy (since next to cell 2)
        # Don't do anything if is a square
        # Rotate clock-wise

        # Find point p that touches two others (will always exist)
        # Align points so that three are touching (p in the middle), last is two away

        # Sort the shape so we go from top-to-bottom, right-to-left
        # https://stackoverflow.com/a/17109098
        self._align_shape_cells()

        shape_copy = deepcopy(self.current_shape)

        # TODO: Handle extra cases for 

        # Trace the shape, determine where we need to move w.r.t. pivot
        # Pivot (2) will be somewhere around us...
        if shape_copy[1][1] > shape_copy[0][1]:  # Below
            # Move cell (1) from top to the right
            new_x = shape_copy[0][0] + 1
            new_y = shape_copy[0][1] + 1
            if self._point_available(new_x, new_y):
                shape_copy[0][0] = new_x
                shape_copy[0][1] = new_y
            else:
                return  # Make no changes
        elif shape_copy[1][0] < shape_copy[0][0]:  # Left
            # Move cell (1) from right to below
            new_x = shape_copy[0][0] - 1
            new_y = shape_copy[0][1] + 1
            if self._point_available(new_x, new_y):
                shape_copy[0][0] = new_x
                shape_copy[0][1] = new_y
            else:
                return  # Make no changes
        elif shape_copy[1][0] > shape_copy[0][0]:  #  Right
            # Move cell (1) from left to above
            new_x = shape_copy[0][0] + 1
            new_y = shape_copy[0][1] - 1
            if self._point_available(new_x, new_y):
                shape_copy[0][0] = new_x
                shape_copy[0][1] = new_y
            else:
                return  # Make no changes
        else:  # Above
            # Move cell (1) from below to left
            new_x = shape_copy[0][0] - 1
            new_y = shape_copy[0][1] - 1
            if self._point_available(new_x, new_y):
                shape_copy[0][0] = new_x
                shape_copy[0][1] = new_y
            else:
                return  # Make no changes

        # Do nothing to the pivot

        # Point (3) will be near pivot (2)
        if shape_copy[2][1] > shape_copy[1][1]:  # Below
            # Move cell (3) from below to the left
            new_x = shape_copy[2][0] - 1
            new_y = shape_copy[2][1] - 1
            if self._point_available(new_x, new_y):
                shape_copy[2][0] = new_x
                shape_copy[2][1] = new_y
            else:
                return  # Make no changes
        elif shape_copy[2][0] > shape_copy[1][0]:  # Right
            # Move cell (3) from right to below
            new_x = shape_copy[2][0] - 1
            new_y = shape_copy[2][1] + 1
            if self._point_available(new_x, new_y):
                shape_copy[2][0] = new_x
                shape_copy[2][1] = new_y
            else:
                return  # Make no changes
        elif shape_copy[2][0] < shape_copy[1][0]:  # Left
            # Move cell (3) from left to above
            new_x = shape_copy[2][0] + 1
            new_y = shape_copy[2][1] - 1
            if self._point_available(new_x, new_y):
                shape_copy[2][0] = new_x
                shape_copy[2][1] = new_y
            else:
                return  # Make no changes
        else:  # Above
            # Move cell (3) from above to right
            new_x = shape_copy[2][0] + 1
            new_y = shape_copy[2][1] + 1
            if self._point_available(new_x, new_y):
                shape_copy[2][0] = new_x
                shape_copy[2][1] = new_y
            else:
                return  # Make no changes

        # Cell (4) can be anywhere from pivot... corner to 2 or two blocks away
        if shape_copy[3][0] > shape_copy[1][0] \
            and shape_copy[3][1] == shape_copy[1][1]:  # Right of pivot by two blocks
            # Move cell below by two blocks
            new_x = shape_copy[3][0] - 2
            new_y = shape_copy[3][1] + 2
            if self._point_available(new_x, new_y):
                shape_copy[3][0] = new_x
                shape_copy[3][1] = new_y
            else:
                return  # Make no changes
        elif shape_copy[3][0] < shape_copy[1][0] \
            and shape_copy[3][1] == shape_copy[1][1]:  # Left of pivot by two blocks
            # Move cell above by two blocks
            new_x = shape_copy[3][0] + 2
            new_y = shape_copy[3][1] - 2
            if self._point_available(new_x, new_y):
                shape_copy[3][0] = new_x
                shape_copy[3][1] = new_y
            else:
                return  # Make no changes
        elif shape_copy[3][1] > shape_copy[1][1] \
            and shape_copy[3][0] == shape_copy[1][0]:  # Below pivot by two blocks
            # Move cell to left by two blocks
            new_x = shape_copy[3][0] - 2
            new_y = shape_copy[3][1] - 2
            if self._point_available(new_x, new_y):
                shape_copy[3][0] = new_x
                shape_copy[3][1] = new_y
            else:
                return  # Make no changes
        elif shape_copy[3][1] < shape_copy[1][1] \
            and shape_copy[3][0] == shape_copy[1][0]:  # Above pivot by two blocks
            # Move cell to right by two blocks
            new_x = shape_copy[3][0] + 2
            new_y = shape_copy[3][1] + 2
            if self._point_available(new_x, new_y):
                shape_copy[3][0] = new_x
                shape_copy[3][1] = new_y
            else:
                return  # Make no changes
        elif shape_copy[3][1] < shape_copy[1][1] \
            and shape_copy[3][0] < shape_copy[1][0]:  # Above and left of pivot
            # Move cell to right by two blocks
            new_x = shape_copy[3][0] + 2
            new_y = shape_copy[3][1]
            if self._point_available(new_x, new_y):
                shape_copy[3][0] = new_x
                shape_copy[3][1] = new_y
            else:
                return  # Make no changes
        elif shape_copy[3][1] > shape_copy[1][1] \
            and shape_copy[3][0] < shape_copy[1][0]:  # Below and left of pivot
            # Move cell up by two blocks
            new_x = shape_copy[3][0]
            new_y = shape_copy[3][1] - 2
            if self._point_available(new_x, new_y):
                shape_copy[3][0] = new_x
                shape_copy[3][1] = new_y
            else:
                return  # Make no changes
        elif shape_copy[3][1] < shape_copy[1][1] \
            and shape_copy[3][0] > shape_copy[1][0]:  # Above and right of pivot
            # Move cell down by two blocks
            new_x = shape_copy[3][0]
            new_y = shape_copy[3][1] + 2
            if self._point_available(new_x, new_y):
                shape_copy[3][0] = new_x
                shape_copy[3][1] = new_y
            else:
                return  # Make no changes
        elif shape_copy[3][1] > shape_copy[1][1] \
            and shape_copy[3][0] > shape_copy[1][0]:  # Below and right of pivot
            # Move cell left by two blocks
            new_x = shape_copy[3][0] - 2
            new_y = shape_copy[3][1]
            if self._point_available(new_x, new_y):
                shape_copy[3][0] = new_x
                shape_copy[3][1] = new_y
            else:
                return  # Make no changes

        # Reset shape on grid
        shape_cells = []
        for cell in self.current_shape:
            shape_cells.append(self.cells[cell[0]][cell[1]])
            self.cells[cell[0]][cell[1]] = None

        for i, cell in enumerate(shape_copy):
            self.cells[cell[0]][cell[1]] = shape_cells[i]

        self.current_shape = shape_copy


    def _align_shape_cells(self):
        most_common_x = Counter([x[0] for x in self.current_shape]).most_common()
        most_common_y = Counter([x[1] for x in self.current_shape]).most_common()

        shapes_copy = deepcopy(self.current_shape)

        # if 3+ with same y, sort by x, pick middle as pivot
        if most_common_y[0][1] >= 3:
            shapes_copy.sort(key=lambda x: (x[1] == most_common_y[0][0], x[0]), reverse=True)
        # else if 3+ with same x, sort by y, pick middle as pivot
        elif most_common_x[0][1] >= 3:
            shapes_copy.sort(key=lambda x: (x[0] == most_common_x[0][0], x[1]), reverse=True)
        # else if 2 with same y, find common x, pick right as pivot (higher x)
        elif most_common_y[0][1] == 2 and most_common_y[1][1] == 2:
            shapes_copy.sort(key=lambda x: (x[1], -x[0]))
            # Sometimes we have first and last flipped...
            if self._point_distance(shapes_copy[0], shapes_copy[1]) >\
                self._point_distance(shapes_copy[1], shapes_copy[3]):
                far_point = shapes_copy[0]
                shapes_copy[0] = shapes_copy[3]
                shapes_copy[3] = far_point
        # else if 2 with same x, find common y, pick upper as pivot (lower y)
        elif most_common_x[0][1] == 2 and most_common_x[1][1] == 2:
            shapes_copy.sort(key=lambda x: (x[1], -x[0]))  # They're the same?!
            # Sometimes we have first and last flipped...
            if self._point_distance(shapes_copy[0], shapes_copy[1]) >\
                self._point_distance(shapes_copy[1], shapes_copy[3]):
                far_point = shapes_copy[0]
                shapes_copy[0] = shapes_copy[3]
                shapes_copy[3] = far_point
        else:
            exit(666)  # You're out of luck

        self.current_shape = shapes_copy


    def _point_distance(self, point_a, point_b):
        return ((point_a[1] - point_b[1])**2 + (point_a[0] - point_b[0])**2)**(1/2)


    def _point_available(self, x_value, y_value):
        return 0 <= x_value <= 9 \
            and 0 <= y_value <= 21 \
            and (self.cells[x_value][y_value] is None \
                or [x_value, y_value] in self.current_shape)
