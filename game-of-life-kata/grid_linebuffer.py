
class Grid():
    """
    This grid uses a line buffer to avoid the need of a previous grid/matrix with full state.
    Works by keeping a buffer of current and previous line of a cell (while looping through all of them).
    Note: It is meant to be called when traversing full grid in order, if you jump data will become garbled as the
          buffer won't update accordingly.
    """

    def __init__(self, width, height):
        self.matrix = self._init_matrix(width, height)
        self.width = width
        self.height = height
        self.linebuffer = self._init_linebuffer(width)
        self.linebuffer_prev_index = 0
        self.linebuffer_index = 1

    def populate_cells(self, coordinates):
        for coordinate in coordinates:
            self.set_cell(coordinate[0], coordinate[1], 1)

    def advance_generation(self):
        self._clear_linebuffer()
        for y in range(self.height):
            self._update_linebuffer(y)
            for x in range(self.width):
                self.set_cell(x, y, self.cell_tick(x, y))

    def cell_tick(self, x, y):
        if self._count_adjacent_cells(x, y) == 3 or (
           self.get_cell(x, y) == 1 and self._count_adjacent_cells(x, y) == 2):
            return 1
        else:
            return 0

    def get_cell(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return 0
        else:
            return self.matrix[self.width*y + x]

    def get_cell_buffered(self, buffer_line, x):
        if x < 0 or x >= self.width:
            return 0
        else:
            return self.linebuffer[buffer_line][x]

    def set_cell(self, x, y, value):
        self.matrix[self.width*y + x] = value

    def _update_linebuffer(self, y):
        self.linebuffer_prev_index = self.linebuffer_index          # swap lines
        self.linebuffer_index = (self.linebuffer_index + 1) % 2
        for x in range(self.width):     # and update
            self.linebuffer[self.linebuffer_index][x] = self.get_cell(x, y)

    def _count_adjacent_cells(self, x, y):
        return (self.get_cell_buffered(self.linebuffer_prev_index, x - 1) +
                self.get_cell_buffered(self.linebuffer_prev_index, x) +
                self.get_cell_buffered(self.linebuffer_prev_index, x + 1) +
                self.get_cell_buffered(self.linebuffer_index, x - 1) +
                self.get_cell_buffered(self.linebuffer_index, x + 1) +
                self.get_cell(x - 1, y + 1) +
                self.get_cell(x, y + 1) +
                self.get_cell(x + 1, y + 1))

    def _init_matrix(self, width, height):
        return [0 for pos in range(width * height)]

    def _init_linebuffer(self, width):
        return [[0 for x in range(width)] for y in range(2)]

    def _clear_linebuffer(self):
        for x in range(self.width):
            self.linebuffer[0][x] = 0
            self.linebuffer[1][x] = 0
