import heapq
from typing import Iterator

from data_structures import Point, Segment
from matrix2d import Matrix2D
from utils import timeit

_DIRECTIONS = (
    (1, 0),
    (-1, 0),
    (0, -1),
    (0, 1),
) # 4 directional movement offsets

Cell = tuple[int, int]

def in_bounds(x: int, y: int, matrix: Matrix2D) -> bool:
    """Check if a cell is within the bounds of the matrix."""
    return 0 <= x < matrix.w and 0 <= y < matrix.h

def cost_function(cell: Cell, matrix: Matrix2D) -> int:
    """Calculate the cost of moving to a cell"""
    point: Point = Point(cell[0], cell[1])
    return matrix.get_cell_cost(point)

def heuristic(a: Cell, b: Cell) -> int:
    """Calculate Manhattan distance between two cells. Used as A* heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # manhattan distance

def neighbors(cell: Cell, matrix: Matrix2D) -> Iterator[Cell]:
    """Yield all in-bounds cardinally adjacent neighbor cells of a given cell."""
    x, y = cell
    for dx, dy in _DIRECTIONS:
        new_x, new_y = x + dx, y + dy
        if in_bounds(new_x, new_y, matrix):
            yield new_x, new_y


def get_path(origin: dict[Cell, Cell], current: Cell) -> list[Point]:
    """Reconstruct the path by walking the origin dictionary backwards."""
    path = [current]
    while current in origin:
        current = origin[current]
        path.append(current)
    return [Point(x, y) for x, y in reversed(path)]

def astar_step(start: Point, end: Point, matrix: Matrix2D) -> list[Point]:
    """Find the lowest-cost path between two points in a 2D matrix using A* search

    Args:
        start: Path start point (center of a room)
        end: Path end point (center of a room)
        matrix: 2D matrix representing the map

    Returns:
        The path from start to end as a list of points, including start and end themselves

    Raises:
        Value Error: If start or end point is out of bounds
        RuntimeError: If no path can be found between start and end
    """
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
            neighbor_score = g_score[current] + cost_function(neighbor, matrix)
            if neighbor_score < g_score.get(neighbor, float('inf')):
                origin[neighbor] = current
                g_score[neighbor] = neighbor_score
                heapq.heappush(open_set, (neighbor_score + heuristic(neighbor, end_cell), neighbor))

    raise RuntimeError(f"No path from {start} to {end}")


@timeit
def astar(triangulation: list[Segment], matrix: Matrix2D) -> Matrix2D:
    """Run A* search for each segment in the mst of the triangulation and return a Matrix2D map representation with the hallways carved out.

    Args:
        triangulation: Segments representing the minimum spanning tree of the triangulation
        matrix: 2D matrix representing the map
    Returns:
        The full path carved as a Matrix2D
    """
    matrix_copy = matrix.copy()
    for segment in triangulation:
        segment_path = astar_step(segment.p1, segment.p2, matrix_copy)
        for point in segment_path:
            matrix_copy.carve_cell(point)

    return matrix_copy
