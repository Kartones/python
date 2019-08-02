from grid import Grid

"""
Game of Life kata (inside out approach)
"""

# grid setup


def test_setups_an_NxM_grid_with_width_N_4_and_height_M_3():
    grid = Grid(width=4, height=3)
    assert len(grid.matrix) == 3*4


def test_setups_an_square_3x3_grid():
    grid = Grid(width=3, height=3)
    assert len(grid.matrix) == 3*3


def test_creates_a_new_grid_filled_with_empty_cells():
    grid = Grid(width=3, height=3)
    for cell in grid.matrix:
        assert cell == 0


# populating cells


def test_on_a_1x1_grid_populates_the_position():
    grid = Grid(width=1, height=1)
    assert grid.get_cell(0, 0) == 0
    grid.populate_cells([(0, 0)])
    assert grid.get_cell(0, 0) == 1


def test_on_a_2x2_grid_populates_some_positions():
    grid = Grid(width=2, height=2)
    grid.populate_cells([(0, 1), (1, 1)])
    assert grid.get_cell(0, 0) == 0
    assert grid.get_cell(0, 1) == 1
    assert grid.get_cell(1, 0) == 0
    assert grid.get_cell(1, 1) == 1


# invididual cell evolution calculations


def test_on_a_1x1_grid_evolution_calculations_dont_error():
    grid = Grid(width=1, height=1)
    assert grid.cell_tick(0, 0) == 0


def test_on_a_2x2_grid_evolution_calculations_dont_error():
    grid = Grid(width=2, height=2)
    grid.populate_cells([(0, 1)])
    assert grid.cell_tick(0, 1) == 0


def test_on_a_3x3_grid_a_centered_cell_survives_if_has_2_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(1, 1), (0, 1), (1, 2)])
    assert grid.cell_tick(1, 1) == 1


def test_on_a_3x3_grid_a_centered_cell_survives_if_has_3_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(1, 1), (0, 1), (1, 2), (2, 2)])
    assert grid.cell_tick(1, 1) == 1


def test_on_a_3x3_grid_a_centered_cell_dies_if_has_no_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(1, 1)])
    assert grid.cell_tick(1, 1) == 0


def test_on_a_3x3_grid_a_centered_cell_dies_if_has_less_than_2_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(1, 1), (2, 2)])
    assert grid.cell_tick(1, 1) == 0


def test_on_a_3x3_grid_a_centered_cell_dies_if_has_more_than_3_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(1, 0), (1, 1), (2, 0), (2, 1), (2, 2)])
    assert grid.cell_tick(1, 1) == 0


def test_on_a_3x3_grid_a_centered_cell_space_reproduces_if_has_exactly_3_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(0, 1), (1, 2), (2, 2)])
    assert grid.cell_tick(1, 1) == 1


def test_on_a_3x3_grid_a_centered_cell_space_doesnt_reproduces_if_has_less_than_3_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(0, 1), (1, 2)])
    assert grid.cell_tick(1, 1) == 0


def test_on_a_3x3_grid_a_centered_cell_space_doesnt_reproduces_if_has_more_than_3_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(0, 1), (1, 2), (2, 1), (2, 2)])
    assert grid.cell_tick(1, 1) == 0


def test_on_a_3x3_grid_a_topleft_cell_survives_if_has_exactly_2_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(0, 0), (0, 1), (1, 0)])
    assert grid.cell_tick(0, 0) == 1


def test_on_a_3x3_grid_a_topleft_cell_survives_if_has_3_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(0, 0), (0, 1), (1, 0), (1, 1)])
    assert grid.cell_tick(0, 0) == 1


def test_on_a_3x3_grid_a_topleft_cell_dies_if_has_less_than_2_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(0, 0), (0, 1)])
    assert grid.cell_tick(0, 0) == 0


def test_on_a_3x3_grid_a_topleft_cell_dies_if_has_no_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(0, 0)])
    assert grid.cell_tick(0, 0) == 0


def test_on_a_3x3_grid_a_topleft_cell_space_reproduces_if_has_exactly_3_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(0, 1), (1, 0), (1, 1)])
    assert grid.cell_tick(0, 0) == 1


def test_on_a_3x3_grid_a_topleft_cell_space_doesnt_reproduces_if_has_less_than_3_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(0, 1), (1, 0)])
    assert grid.cell_tick(0, 0) == 0


# full grid/matrix evolution calculations


def test_given_a_1x1_grid_a_full_snapshot_tick_returns_another_1x1_grid():
    grid = Grid(width=1, height=1)
    grid.populate_cells([(0, 0)])
    new_matrix = grid.grid_tick()
    assert len(new_matrix) == 1
    assert new_matrix[0] == 0


def test_correctly_snapshot_ticks_a_3x3_grid_with_centered_cell_and_2_adjacent_cells():
    grid = Grid(width=3, height=3)
    grid.populate_cells([(0, 0), (0, 1), (1, 0)])
    new_matrix = grid.grid_tick()
    assert len(new_matrix) == 3*3
    # space at position (1,1) spawned a cell as it has 3 adjancent
    assert new_matrix == [1, 1, 0, 1, 1, 0, 0, 0, 0]
