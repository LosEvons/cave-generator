"""
Conditions to be tested against:
1. A straight FREE grid produces the shortest path from start to goal
2. A start point equal to end point returns a single point path
3. A cheaper path around SOLID is preferred to crossing it
4. An out-of-bounds start or end raises error
5. astar() combines paths of multiple segments in the correct order
6. astar() will prefer existing hallways to carving new ones
"""

import pytest

from astar import astar, astar_step
from data_structures import Point, Segment
from matrix2d import CellType, Matrix2D

def make_matrix(w, h, fill=CellType.FREE):
    return Matrix2D(w=w, h=h, cells=[[fill] * w for _ in range(h)])

def test_straight_free_grid():
    matrix = make_matrix(5, 1)
    path = astar_step(Point(0, 0), Point(4, 0), matrix)
    assert path == [Point(x, 0) for x in range(5)]

def test_start_equals_end():
    matrix = make_matrix(5, 1)
    path = astar_step(Point(0, 0), Point(0, 0), matrix)
    assert path == [Point(0, 0)]

def test_path_around_solid_preferred():
    matrix = make_matrix(3, 3)
    # S # E
    # . # .
    # . . .
    for y in (0, 1):
        matrix.set_cell(Point(1, y), CellType.SOLID)
    path = astar_step(Point(0, 0), Point(2, 0), matrix)
    assert Point(1, 2) in path
    assert Point(1, 0) not in path
    assert Point(1, 1) not in path


@pytest.mark.parametrize("start, end",
                         [
                             (Point(-1, 0), Point(1, 1)),
                             (Point(0, 0), Point(5, 5))
                         ]
                         )
def test_out_of_bounds_raises_error(start, end):
    matrix = make_matrix(3, 3)
    with pytest.raises(ValueError):
        astar_step(start, end, matrix)

def test_astar_combines_multiple_segments_in_order():
    matrix = make_matrix(5, 1)
    segments = [
        Segment(Point(0, 0), Point(1, 0)),
        Segment(Point(1, 0), Point(2, 0)),
        Segment(Point(2, 0), Point(3, 0)),
        Segment(Point(3, 0), Point(4, 0))
    ]
    result = astar(segments, matrix)
    assert all([result.get_cell(Point(x, 0)) == CellType.FREE for x in range(5)])

def test_astar_reuses_existing_corridor():
    matrix = make_matrix(5, 3, fill=CellType.SOLID)
    # E2 # # # #
    # S1 # # # E1
    # #  # # # S2
    segments = [
        Segment(Point(0, 1), Point(4, 1)),
        Segment(Point(0, 0), Point(4, 2)),
    ]

    result = astar(segments, matrix)

    cells = {
        Point(x, y) for y in range(3) for x in range(5)
        if result.get_cell(Point(x, y)) == CellType.FREE
    }

    assert len(cells) == 7, (f"A* should always prefer using existing paths to creating new ones.")