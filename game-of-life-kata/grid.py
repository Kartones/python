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

    def cell_tick(self, x, y):
        if self._count_adjacent_cells(x, y) == 3 or (
           self.get_cell(x, y) == 1 and self._count_adjacent_cells(x, y) == 2):
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
        return self.matrix[self.width * y + x] if (0 <= x < self.width) and (0 <= y < self.height) else 0

    def set_cell(self, x, y, value, matrix=None):
        matrix = self.matrix if not matrix else matrix
        matrix[self.width * y + x] = value

    def _count_adjacent_cells(self, x, y):
        return (self.get_cell(x - 1, y - 1) +
                self.get_cell(x, y - 1) +
                self.get_cell(x + 1, y - 1) +
                self.get_cell(x - 1, y) +
                self.get_cell(x + 1, y) +
                self.get_cell(x - 1, y + 1) +
                self.get_cell(x, y + 1) +
                self.get_cell(x + 1, y + 1))

    def _init_matrix(self, width, height):
        return [0 for pos in range(width * height)]
