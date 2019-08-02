from grid_linebuffer import Grid

"""
Tests related to line buffer optimized grid
"""


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


def test_linebuffer_is_created_with_appropiate_width_and_always_2_lines():
    grid = Grid(width=4, height=3)

    assert len(grid.linebuffer) == 2
    assert len(grid.linebuffer[0]) == grid.width


def test_linebuffer_indexes_start_with_current_1_and_previous_0():
    grid = Grid(width=4, height=3)

    assert grid.linebuffer_index == 1
    assert grid.linebuffer_prev_index == 0


def test_indexes_swap_when_updating_the_linebuffer():
    irrelevant_y_coordinate = 1
    grid = Grid(width=4, height=3)

    grid._update_linebuffer(irrelevant_y_coordinate)
    assert grid.linebuffer_index == 0
    assert grid.linebuffer_prev_index == 1

    grid._update_linebuffer(irrelevant_y_coordinate)
    assert grid.linebuffer_index == 1
    assert grid.linebuffer_prev_index == 0

    grid._update_linebuffer(irrelevant_y_coordinate)
    assert grid.linebuffer_index == 0
    assert grid.linebuffer_prev_index == 1


def test_fills_current_index_with_y_coordinate_line():
    grid = Grid(width=3, height=3)
    setup_grid_cells(grid)

    # this also works as edge-detection case
    grid._update_linebuffer(0)
    assert grid.linebuffer[grid.linebuffer_index] == [1, 0, 0]
    # the other line should be empty

    grid._update_linebuffer(1)
    assert grid.linebuffer[grid.linebuffer_index] == [0, 1, 0]
    assert grid.linebuffer[grid.linebuffer_prev_index] == [1, 0, 0]

    grid._update_linebuffer(2)
    assert grid.linebuffer[grid.linebuffer_index] == [0, 0, 1]
    assert grid.linebuffer[grid.linebuffer_prev_index] == [0, 1, 0]


def test_its_data_becomes_invalid_if_updates_are_not_y_coordinate_consecutive():
    grid = Grid(width=3, height=3)
    setup_grid_cells(grid)
    # all fine so far
    grid._update_linebuffer(0)
    assert grid.linebuffer[grid.linebuffer_index] == [1, 0, 0]

    grid._update_linebuffer(2)
    assert grid.linebuffer[grid.linebuffer_index] == [0, 0, 1]
    # this'd be the correct value
    assert grid.linebuffer[grid.linebuffer_prev_index] != [0, 1, 0]
    # but instead has just the swapped old value, returning wrong data
    assert grid.linebuffer[grid.linebuffer_prev_index] == [1, 0, 0]
