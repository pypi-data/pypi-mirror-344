from tokyo import TokyoGrid


def test_init_grid():
    grid = TokyoGrid()
    assert grid.grid_width == 100
    assert grid.grid_height == 75
