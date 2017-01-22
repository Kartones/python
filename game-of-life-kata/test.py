from expects import *
from doublex import *
from doublex_expects import *

from grid import *


with description("Game of Life kata (inside out approach)"):
    with context("grid setup"):
        with it("setups an NxM grid with width N=4 and height M=3"):
            grid = Grid(width=4, height=3)
            expect(len(grid.matrix)).to(equal(3*4))

        with it("setups an square 3x3 grid"):
            grid = Grid(width=3, height=3)
            expect(len(grid.matrix)).to(equal(3*3))

        with it("creates a new grid filled with empty cells (value 0)"):
            grid = Grid(width=3, height=3)
            for cell in grid.matrix:
                expect(cell).to(equal(0))

    with context("populating cells"):
        with it("on a 1x1 grid, populates the position"):
            grid = Grid(width=1, height=1)
            expect(grid.get_cell(0, 0)).to(equal(0))
            grid.populate_cells([(0, 0)])
            expect(grid.get_cell(0, 0)).to(equal(1))

        with it("on a 2x2 grid, populates some positions"):
            grid = Grid(width=2, height=2)
            grid.populate_cells([(0, 1), (1, 1)])
            expect(grid.get_cell(0, 0)).to(equal(0))
            expect(grid.get_cell(0, 1)).to(equal(1))
            expect(grid.get_cell(1, 0)).to(equal(0))
            expect(grid.get_cell(1, 1)).to(equal(1))

    with context("invididual cell evolution calculations"):
        with it("on a 1x1 grid, evolution calculations don't error"):
            grid = Grid(width=1, height=1)
            expect(grid.cell_tick(0, 0)).to(equal(0))

        with it("on a 2x2 grid, evolution calculations don't error"):
            grid = Grid(width=2, height=2)
            grid.populate_cells([(0, 1)])
            expect(grid.cell_tick(0, 1)).to(equal(0))

        with it("on a 3x3 grid, a centered cell survives if has 2 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(1, 1), (0, 1), (1, 2)])
            expect(grid.cell_tick(1, 1)).to(equal(1))

        with it("on a 3x3 grid, a centered cell survives if has 3 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(1, 1), (0, 1), (1, 2), (2, 2)])
            expect(grid.cell_tick(1, 1)).to(equal(1))

        with it("on a 3x3 grid, a centered cell dies if has no adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(1, 1)])
            expect(grid.cell_tick(1, 1)).to(equal(0))

        with it("on a 3x3 grid, a centered cell dies if has less than 2 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(1, 1), (2, 2)])
            expect(grid.cell_tick(1, 1)).to(equal(0))

        with it("on a 3x3 grid, a centered cell dies if has more than 3 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(1, 0), (1, 1), (2, 0), (2, 1), (2, 2)])
            expect(grid.cell_tick(1, 1)).to(equal(0))

        with it("on a 3x3 grid, a centered cell space reproduces if has exactly 3 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(0, 1), (1, 2), (2, 2)])
            expect(grid.cell_tick(1, 1)).to(equal(1))

        with it("on a 3x3 grid, a centered cell space doesn't reproduces if has less than 3 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(0, 1), (1, 2)])
            expect(grid.cell_tick(1, 1)).to(equal(0))

        with it("on a 3x3 grid, a centered cell space doesn't reproduces if has more than 3 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(0, 1), (1, 2), (2, 1), (2, 2)])
            expect(grid.cell_tick(1, 1)).to(equal(0))

        with it("on a 3x3 grid, a top-left cell survives if has exactly 2 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(0, 0), (0, 1), (1, 0)])
            expect(grid.cell_tick(0, 0)).to(equal(1))

        with it("on a 3x3 grid, a top-left cell survives if has 3 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(0, 0), (0, 1), (1, 0), (1, 1)])
            expect(grid.cell_tick(0, 0)).to(equal(1))

        with it("on a 3x3 grid, a top-left cell dies if has less than 2 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(0, 0), (0, 1)])
            expect(grid.cell_tick(0, 0)).to(equal(0))

        with it("on a 3x3 grid, a top-left cell dies if has no adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(0, 0)])
            expect(grid.cell_tick(0, 0)).to(equal(0))

        with it("on a 3x3 grid, a top-left cell space reproduces if has exactly 3 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(0, 1), (1, 0), (1, 1)])
            expect(grid.cell_tick(0, 0)).to(equal(1))

        with it("on a 3x3 grid, a top-left cell space doesn't reproduces if has less than 3 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(0, 1), (1, 0)])
            expect(grid.cell_tick(0, 0)).to(equal(0))

    with context("full grid/matrix evolution calculations"):
        with it("given a 1x1 grid, a full snapshot tick returns another 1x1 grid"):
            grid = Grid(width=1, height=1)
            grid.populate_cells([(0, 0)])
            new_matrix = grid.grid_tick()
            expect(len(new_matrix)).to(equal(1))
            expect(new_matrix[0]).to(equal(0))

        with it("correctly snapshot-ticks a 3x3 grid with centered cell and 2 adjacent cells"):
            grid = Grid(width=3, height=3)
            grid.populate_cells([(0, 0), (0, 1), (1, 0)])
            new_matrix = grid.grid_tick()
            expect(len(new_matrix)).to(equal(3*3))
            # space at position (1,1) spawned a cell as it has 3 adjancent
            expect(new_matrix).to(equal([1, 1, 0, 1, 1, 0, 0, 0, 0]))
