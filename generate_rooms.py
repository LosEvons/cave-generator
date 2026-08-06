from dataclasses import dataclass
from functools import reduce
from itertools import product
import random
from typing import Tuple

from sympy import Point, Segment

from algorithm import bowyer_watson, mst
from astar import astar
from matrix2d import CellType, Matrix2D
from utils import xy_to_i

# A representation of a 2D rectangle and its properties
@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int
    
    @property
    def center_x(self) -> int:
        return self.x + self.w // 2

    @property
    def center_y(self) -> int:
        return self.y + self.h // 2

    @property
    def x2(self) -> int:
        return self.x + self.w
    
    @property
    def y2(self) -> int:
        return self.y + self.h
    
    @property
    def inside(self) -> Tuple[slice, slice]:
        return slice(
            self.x + 1, self.x2
        ), slice(
            self.y + 1, self.y2
        )

    def intersects(self, other: "Rect", padding: int = 1) -> bool:
        return not(
            self.x2 + padding <= other.x
            or
            self.x >= other.x2 + padding
            or
            self.y2 + padding <= other.y
            or
            self.y >= other.y2 + padding
        )      

# Change tile type to free for all cells inside the given room rectangle
def carve_room(cells: list[CellType], w: int, room: Rect) -> list[CellType]:
    result = list(cells)
    xs, ys = room.inside
    for x, y in product(range(xs.start, xs.stop), range(ys.start, ys.stop)):
        result[xy_to_i(x, y, w)] = CellType.FREE
    return result

# Change tile type to free for all A* cells
def carve_hallways(matrix: Matrix2D, rooms: list[Rect]) -> Matrix2D:
    if len(rooms) < 2:
        return matrix

    points = [Point(room.center_x, room.center_y) for room in rooms]

    if len(points) == 2: # only one possible solution, no triangulation needed
        tree = [Segment(*points)]
    else:
        triangulation = bowyer_watson([(int(p.x), int(p.y)) for p in points])
        tree = mst(triangulation)

    path = astar(tree, matrix)
    result = list(matrix.cells)
    for cell in path:
        result[xy_to_i(int(cell.x), int(cell.y), matrix.w)] = CellType.FREE
    return Matrix2D(matrix.w, matrix.h, result)

# Generate a random room rectangle within the given width and height constraints
def generate_room(
    rng: random.Random,
    w: int, 
    h: int, 
    min_size: int = 5, 
    max_size: int = 10
    ) -> Rect | None:
    rw = rng.randint(min_size, max_size)
    rh = rng.randint(min_size, max_size)
    rx = rng.randint(1, w - rw - 1)
    ry = rng.randint(1, h - rh - 1)
    return Rect(rx, ry, rw, rh)

# Generate a 2D matrix with randomly placed rooms, ensuring no overlaps and adhering to the specified room count
def generate_rooms(
    w: int, 
    h: int, 
    room_count: int = 10,
    seed: int | None = None
    ) -> Matrix2D:
    rng = random.Random(seed) # Set seed of rng generation
    cells = [CellType.SOLID] * (w * h) # Initialize all cells as solid
    iterations = room_count * 8 # Number of iterations to attempt room placement, allowing for retries in case of overlaps
    candidates = (
        room
        for _ in range(iterations)
        if (room := generate_room(rng, w, h)) is not None
    ) # Generate room candidates
    
    # Helper to check if room placement is valid
    def check_placement(rooms: list[Rect], candidate: Rect) -> list[Rect]:
        if not all(not candidate.intersects(room) for room in rooms) and len(rooms) < room_count:
            return rooms
        return [*rooms, candidate]

    rooms = reduce(check_placement, candidates, [])
    for room in rooms:
        cells = carve_room(cells, w, room)

    matrix = carve_hallways(
        Matrix2D(w, h, cells),
        rooms
    )

    return matrix
