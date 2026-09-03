"""
Conditions to be tested against:
1. A straight FREE grid produces the shortest path from start to goal
2. A start point equal to end point returns a single point path
3. A cheaper path around SOLID is preferred to crossing it
4. An out-of-bounds start or end raises error
5. astar() combines paths of multiple segments in the correct order
6. astar() will prefer existing hallways to carving new ones
7. astar_step() path should be contiguous, and the shortest path found should have length matching with the shortest path found with Dijkstra library function
"""

import pytest
import random
import networkx as nx

from astar import astar, astar_step
from data_structures import Point, Segment
from matrix2d import CellType, Matrix2D

from conftest import cost_graph, path_is_contiguous, path_cost

def make_matrix(w, h, fill=CellType.FREE):
    return Matrix2D(w=w, h=h, cells=[[fill] * w for _ in range(h)])

def make_random_matrix(seed, solid_cell_ratio=0.3):
    rng = random.Random(seed)
    w, h = rng.randint(5, 10), rng.randint(5, 10)
    cells = [
        [CellType.SOLID if rng.random() < solid_cell_ratio else CellType.FREE
         for _ in range(w)]
        for _ in range(h)
    ]
    return Matrix2D(w=w, h=h, cells=cells), rng

def test_straight_free_grid():
    matrix = make_matrix(5, 1)
    path = astar_step(Point(0, 0), Point(4, 0), matrix)
    assert path == [Point(x, 0) for x in range(5)]

def test_start_equals_end():
    matrix = make_matrix(5, 1)
    path = astar_step(Point(0, 0), Point(0, 0), matrix)
    assert path == [Point(0, 0)]


@pytest.mark.parametrize("start, end, wall, gap", [ # Tested for each movement direction
    (Point(0, 0), Point(2, 0), [Point(1, 0), Point(1, 1)], Point(1, 2)), # down
    (Point(0, 2), Point(2, 2), [Point(1, 2), Point(1, 1)], Point(1, 0)), # up
    (Point(0, 0), Point(0, 2), [Point(0, 1), Point(1, 1)], Point(2, 1)), # right
    (Point(2, 0), Point(2, 2), [Point(2, 1), Point(1, 1)], Point(0, 1)), # left
])
def test_path_around_solid_preferred(start, end, wall, gap):
    matrix = make_matrix(3, 3)
    for cell in wall:
        matrix.set_cell(cell, CellType.SOLID)
    path = astar_step(start, end, matrix)
    assert path[0] == start and path[-1] == end
    assert gap in path, "A* should use a free gap in a wall instead of going through a solid cell"
    assert all(matrix.get_cell(cell) == CellType.FREE for cell in path), "In the preset testing configuration A* path should only include free cells"
    assert path_is_contiguous(path), "A* path should be contiguous"


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

    assert len(cells) == 7, f"A* should always prefer using existing paths to creating new ones."

@pytest.mark.parametrize("seed", range(100))
def test_astar_matches_dijkstra(seed):
    matrix, rng = make_random_matrix(seed)
    cells = [Point(x, y) for y in range(matrix.h) for x in range(matrix.w)]
    start, end = rng.choice(cells), rng.choice(cells)

    astar_path = astar_step(start, end, matrix)
    dijkstra_path_cost = nx.dijkstra_path_length(cost_graph(matrix), (start.x, start.y), (end.x, end.y))

    assert astar_path[0] == start and astar_path[-1] == end, f"Invalid A* start or end."
    assert path_is_contiguous(astar_path), f"A* path must be contiguous."
    assert path_cost(astar_path, matrix) == dijkstra_path_cost, f"A* path cost must match with shortest path found with dijkstra."