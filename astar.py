import heapq
from typing import Generator, Iterator

from data_structures import Point, Segment
from matrix2d import CellType, Matrix2D
from utils import xy_to_i, timeit

_DIRECTIONS = (
    (1, 0),
    (-1, 0),
    (0, -1),
    (0, 1),
)

Cell = tuple[int, int]

def in_bounds(x: int, y: int, matrix: Matrix2D) -> bool:
    return 0 <= x < matrix.w and 0 <= y < matrix.h

def cost_function(cell: Cell, matrix: Matrix2D, solid_cost: int, free_cost: int) -> int:
    x, y = cell
    return (
        free_cost if matrix.cells[xy_to_i(x, y, matrix.w)] is CellType.FREE
        else solid_cost
    )

def heuristic(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # manhattan distance

def neighbors(cell: Cell, matrix: Matrix2D) -> Iterator[Cell]:
    x, y = cell
    for dx, dy in _DIRECTIONS:
        new_x, new_y = x + dx, y + dy
        if in_bounds(new_x, new_y, matrix):
            yield new_x, new_y


def get_path(origin: dict[Cell, Cell], current: Cell) -> list[Point]:
    path = [current]
    while current in origin:
        current = origin[current]
        path.append(current)
    return [Point(x, y) for x, y in reversed(path)]

def astar_step(start: Point, end: Point, matrix: Matrix2D, solid_cost: int, free_cost: int) -> list[Point]:
    start_cell = (int(start.x), int(start.y))
    end_cell = (int(end.x), int(end.y))

    # check in bounds
    if not in_bounds(start_cell[0], start_cell[1], matrix) or not in_bounds(end_cell[0], end_cell[1], matrix):
        raise ValueError("Start or end point is out of bounds")

    open_set: list[tuple[int, Cell]] = [(0, start_cell)]
    origin: dict[Cell, Cell] = {}
    g_score: dict[Cell, int] = {start_cell: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end_cell:
            return get_path(origin, current)

        for neighbor in neighbors(current, matrix):
            neighbor_score = g_score[current] + cost_function(neighbor, matrix, solid_cost, free_cost)
            if neighbor_score < g_score.get(neighbor, float('inf')):
                origin[neighbor] = current
                g_score[neighbor] = neighbor_score
                heapq.heappush(open_set, (neighbor_score + heuristic(neighbor, end_cell), neighbor))

    raise RuntimeError(f"No path from {start} to {end}")


@timeit
def astar(triangulation: list[Segment], matrix: Matrix2D, solid_cost: int = 3, free_cost: int = 1) -> list[Point]:
    path: list[Point] = []
    for segment in triangulation:
        path.extend(astar_step(segment.p1, segment.p2, matrix, solid_cost, free_cost))
    return path