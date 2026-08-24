"""
Conditions to be tested against:
1. Rect.intersects correctly handles overlapping and padding
2. carve_room only carves tiles from the room interior
3. generate_room always adheres to bounds and size constraints
4. generate_rooms validates inputs and raises correctly
5. generate_rooms is deterministic (same result for same seed)
6. generate_rooms produces a fully connected map
"""
import random

import pytest

import networkx as nx

from data_structures import Point
from generate_rooms import generate_rooms, Rect, generate_room, carve_room
from matrix2d import CellType

@pytest.mark.parametrize("a, b, padding, expected", [
    (Rect(0, 0, 4, 4), Rect(2, 2, 4, 4), 1, True), # overlap
    (Rect(0, 0, 4, 4), Rect(10, 10, 4, 4), 1, False), # apart
    (Rect(0, 0, 4, 4), Rect(4, 0, 4, 4), 0, False), # edges touch, no padding
    (Rect(0, 0, 4, 4), Rect(4, 0, 4, 4), 1, True), # edges touch, with padding
    (Rect(0, 0, 4, 4), Rect(0, 0, 4, 4), 1, True), # identical
])
def test_rect_intersects(a, b, padding, expected):
    assert a.intersects(b, padding) is expected


def test_carve_room_only_carves_interior():
    w, h = 6, 6
    cells = [[CellType.SOLID] * w for _ in range(h)]
    room = Rect(0, 0, 3, 3)
    result = carve_room(cells, room)
    for y in range(h):
        for x in range(w):
            x_slice, y_slice = room.inside
            if x in range(x_slice.start, x_slice.stop) and y in range(y_slice.start, y_slice.stop):
                assert result[y][x] == CellType.FREE
            else:
                assert result[y][x] == CellType.SOLID


@pytest.mark.parametrize("seed", range(10))
def test_generate_room_adhering_to_bounds(seed):
    rng = random.Random(seed)
    w, h, min_size, max_size = 50, 50, 5, 10
    room = generate_room(rng, w, h, min_size, max_size)
    assert min_size <= room.w <= max_size
    assert min_size <= room.h <= max_size
    assert 0 <= room.x and w >= room.x2
    assert 0 <= room.y and h >= room.y2


@pytest.mark.parametrize("args", [
    dict(w=100, h=100, min_size=10, max_size=5), # min > max
    dict(w=100, h=100, min_size=0, max_size=5), # min > 1
    dict(w=5, h=5, min_size=5, max_size=10), # w/h < max_size
    dict(w=100, h=100, room_count=0), # room count = 0
    dict(w=0, h=100), # dimension (w/h) = 0
])
def test_generate_rooms_on_invalid_input(args):
    with pytest.raises(ValueError):
        generate_rooms(**args)


def test_generate_rooms_for_deterministic_seed():
    a = generate_rooms(w=100, h=100, room_count=8, seed=67)
    b = generate_rooms(w=100, h=100, room_count=8, seed=67)
    assert a.cells == b.cells

@pytest.mark.parametrize("seed", range(5))
def test_generate_rooms_produces_fully_connected_map(seed):
    matrix = generate_rooms(w=100, h=100, room_count=30, seed=seed)
    free = {
        (x, y) for y in range(matrix.h) for x in range(matrix.w)
        if matrix.get_cell(Point(x, y)) == CellType.FREE
    }
    assert free, "some free space expected"

    grid = nx.grid_2d_graph(matrix.w, matrix.h)
    assert nx.is_connected(grid.subgraph(free))
