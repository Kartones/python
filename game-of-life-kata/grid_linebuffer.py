
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
        for y in range(self.height):
            self._update_linebuffer(y)
            for x in range(self.width):
                self.set_cell(x, y, self._cell_tick(x, y))

    def get_cell(self, x, y):
        return self.matrix[self.width*y + x] if (0 <= x < self.width) and (0 <= y < self.height) else 0

    def get_cell_buffered(self, buffer_line, x):
        return self.linebuffer[buffer_line][x] if 0 <= x < self.width else 0

    def set_cell(self, x, y, value):
        self.matrix[self.width*y + x] = value

    def _cell_tick(self, x, y):
        # NOTE: Intended to only be called from advance_generation() as counting adjacents uses the linebuffer
        neighbour_count = self._count_adjacent_cells(x, y)
        if neighbour_count == 3 or (neighbour_count == 2 and self.get_cell(x, y) == 1):
            return 1
        else:
            return 0

    def _update_linebuffer(self, y):
        self.linebuffer_prev_index = self.linebuffer_index  # swap lines
        self.linebuffer_index = (self.linebuffer_index + 1) % 2
        for x in range(self.width):  # and update
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
