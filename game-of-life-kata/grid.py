from copy import copy


class Grid():

    def __init__(self, width, height):
        self.matrix = self._init_matrix(width, height)
        self.width = width
        self.height = height

    def populate_cells(self, coordinates):
        for coordinate in coordinates:
            self.set_cell(coordinate[0], coordinate[1], 1)

    def advance_generation(self):
        self.matrix = self.grid_tick()

    def should_cell_live(self, x, y):
        if self.get_cell(x, y) == 0:
            return False
        count = self._count_adjacent_cells(x, y)
        return (count == 2 or count == 3)

    def should_cell_reproduce_here(self, x, y):
        if self.get_cell(x, y) == 1:
            return False
        count = self._count_adjacent_cells(x, y)
        return count == 3

    def cell_tick(self, x, y):
        if self.should_cell_live(x, y) or self.should_cell_reproduce_here(x, y):
            return 1
        else:
            return 0

    # Whole board evolves at once
    def grid_tick(self):
        new_matrix = copy(self.matrix)
        for y in range(self.height):
            for x in range(self.width):
                self.set_cell(x, y, self.cell_tick(x, y), new_matrix)
        return new_matrix

    def get_cell(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return 0
        else:
            return self.matrix[self.width*y + x]

    def set_cell(self, x, y, value, matrix=None):
        matrix = self.matrix if not matrix else matrix
        matrix[self.width*y + x] = value

    def _count_adjacent_cells(self, x, y):
        count = 0
        count += self.get_cell(x - 1, y - 1)
        count += self.get_cell(x, y - 1)
        count += self.get_cell(x + 1, y - 1)
        count += self.get_cell(x - 1, y)
        count += self.get_cell(x + 1, y)
        count += self.get_cell(x - 1, y + 1)
        count += self.get_cell(x, y + 1)
        count += self.get_cell(x + 1, y + 1)
        return count

    def _init_matrix(self, width, height):
        matrix = []
        for pos in range(width * height):
            matrix.append(0)
        return matrix
