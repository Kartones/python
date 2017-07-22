from expects import *
from doublex import *
from doublex_expects import *

from grid_linebuffer import Grid


def setup_grid_cells(grid):
    """
    Populates top-left corner of grid (X means "previous value"):
    1 X X
    X 1 X
    X X 1
    """
    cells = []
    cells.append((0, 0))
    cells.append((1, 1))
    cells.append((2, 2))
    grid.populate_cells(cells)


with description("Tests related to line buffer optimized grid"):
    with context("grid setup"):
        with it("linebuffer is created with appropiate width and always 2 lines"):
            grid = Grid(width=4, height=3)
            expect(len(grid.linebuffer)).to(equal(2))
            expect(len(grid.linebuffer[0])).to(equal(grid.width))

        with it("linebuffer indexes start with current=1, previous=0"):
            grid = Grid(width=4, height=3)
            expect(grid.linebuffer_index).to(equal(1))
            expect(grid.linebuffer_prev_index).to(equal(0))

        with it("when updating the linebuffer, indexes swap"):
            irrelevant_y_coordinate = 1
            grid = Grid(width=4, height=3)

            grid._update_linebuffer(irrelevant_y_coordinate)
            expect(grid.linebuffer_index).to(equal(0))
            expect(grid.linebuffer_prev_index).to(equal(1))

            grid._update_linebuffer(irrelevant_y_coordinate)
            expect(grid.linebuffer_index).to(equal(1))
            expect(grid.linebuffer_prev_index).to(equal(0))

            grid._update_linebuffer(irrelevant_y_coordinate)
            expect(grid.linebuffer_index).to(equal(0))
            expect(grid.linebuffer_prev_index).to(equal(1))

        with it("fills current index with y coordinate line"):
            grid = Grid(width=3, height=3)
            setup_grid_cells(grid)

            # this also works as edge-detection case
            grid._update_linebuffer(0)
            expect(grid.linebuffer[grid.linebuffer_index]).to(equal([1, 0, 0]))
            # the other line should be empty

            grid._update_linebuffer(1)
            expect(grid.linebuffer[grid.linebuffer_index]).to(equal([0, 1, 0]))
            expect(grid.linebuffer[grid.linebuffer_prev_index]).to(equal([1, 0, 0]))

            grid._update_linebuffer(2)
            expect(grid.linebuffer[grid.linebuffer_index]).to(equal([0, 0, 1]))
            expect(grid.linebuffer[grid.linebuffer_prev_index]).to(equal([0, 1, 0]))

        with it("its data becomes invalid if updates are not y-coordinate consecutive"):
            grid = Grid(width=3, height=3)
            setup_grid_cells(grid)
            # all fine so far
            grid._update_linebuffer(0)
            expect(grid.linebuffer[grid.linebuffer_index]).to(equal([1, 0, 0]))

            grid._update_linebuffer(2)
            expect(grid.linebuffer[grid.linebuffer_index]).to(equal([0, 0, 1]))
            # this'd be the correct value
            expect(grid.linebuffer[grid.linebuffer_prev_index]).not_to(equal([0, 1, 0]))
            # but instead has just the swapped old value, returning wrong data
            expect(grid.linebuffer[grid.linebuffer_prev_index]).to(equal([1, 0, 0]))
