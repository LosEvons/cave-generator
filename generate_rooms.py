from dataclasses import dataclass
from functools import reduce
from itertools import product
import random
from typing import Tuple

from data_structures import Point, Segment

from algorithm import bowyer_watson, mst
from astar import astar
from matrix2d import CellType, Matrix2D
from utils import xy_to_i

@dataclass
class Rect:
    """A representation of a 2D rectangle with integer position and size"""
    x: int
    y: int
    w: int
    h: int
    
    @property
    def center_x(self) -> int:
        """Return the x-coordinate of the center of the rectangle"""
        return self.x + self.w // 2

    @property
    def center_y(self) -> int:
        """Return the y-coordinate of the center of the rectangle"""
        return self.y + self.h // 2

    @property
    def x2(self) -> int:
        """Return the x-coordinate of the right edge of the rectangle"""
        return self.x + self.w
    
    @property
    def y2(self) -> int:
        """Return the y-coordinate of the bottom edge of the rectangle"""
        return self.y + self.h
    
    @property
    def inside(self) -> Tuple[slice, slice]:
        """Return slices representing the interior of the rectangle, excluding the edges"""
        return slice(
            self.x + 1, self.x2
        ), slice(
            self.y + 1, self.y2
        )

    def intersects(self, other: "Rect", padding: int = 1) -> bool:
        """Check if this rectangle intersects with another rectangle, with optional padding"""
        return not(
            self.x2 + padding <= other.x
            or
            self.x >= other.x2 + padding
            or
            self.y2 + padding <= other.y
            or
            self.y >= other.y2 + padding
        )      


def carve_room(cells: list[CellType], w: int, room: Rect) -> list[CellType]:
    """Carve out a room in a given matrix by creating a new list of cells with the room area set to free

    Args:
        cells (list[CellType]): List of cells representing the matrix
        w (int): The width of the matrix
        room (Rect): The rectangle representing the room to carve out

    Returns:
        A new list of cells with the room area set to free
    """
    result = list(cells)
    xs, ys = room.inside
    for x, y in product(range(xs.start, xs.stop), range(ys.start, ys.stop)):
        result[xy_to_i(x, y, w)] = CellType.FREE
    return result


def carve_hallways(matrix: Matrix2D, rooms: list[Rect]) -> Matrix2D:
    """Connect room centers with hallways using A* on an MST of a triangulation of room centers and carve them into the matrix

    Args:
        matrix (Matrix2D): The matrix to carve hallways into
        rooms (list[Rect]): List of rectangles representing the rooms

    Returns:
        The updated matrix with hallways carved into it
    """
    if len(rooms) < 2:
        return matrix

    points = [Point(room.center_x, room.center_y) for room in rooms]

    if len(points) == 2: # only one possible solution, no triangulation needed
        tree = [Segment(*points)]
    else:
        triangulation = bowyer_watson([(int(p.x), int(p.y)) for p in points])
        tree = mst(triangulation)

    return astar(tree, matrix)


# Generate a random room rectangle within the given width and height constraints
def generate_room(
    rng: random.Random,
    w: int, 
    h: int, 
    min_size: int,
    max_size: int
    ) -> Rect:
    """Generate a room of ranzom size and position within the given constraints

    Args:
        rng (random.Random): Random number generator instance
        w (int): Width of the matrix
        h (int): Height of the matrix
        min_size (int): Minimum size of the room
        max_size (int): Maximum size of the room
    Returns:
        A Rect object representing the room
    """
    rw = rng.randint(min_size, max_size)
    rh = rng.randint(min_size, max_size)
    rx = rng.randint(1, w - rw - 1)
    ry = rng.randint(1, h - rh - 1)
    return Rect(rx, ry, rw, rh)


def generate_rooms(
    w: int, 
    h: int, 
    room_count: int = 10,
    seed: int | None = None,
    min_size: int = 5,
    max_size: int = 10
    ) -> Matrix2D:
    """
    Generate a 2D matrix with randomly placed rooms and hallways between them, ensuring no overlaps.

    Args:
        w (int): Width of the matrix.
        h (int): Height of the matrix.
        room_count (int): Number of rooms to generate. 10 by default.
        seed (int | None): Seed for the random number generator. None by default.
        min_size (int): Minimum size of the rooms. 5 by default.
        max_size (int): Maximum size of the rooms. 10 by default.

    Returns:
        A Matrix2D representing the generated map.
    """

    if min_size > max_size:
        raise ValueError("min_size must be less than or equal to max_size")

    if min_size < 1:
        raise ValueError("min_size must be greater than or equal to 1")

    if w < max_size + 2 or h < max_size + 2:
        raise ValueError("width and height must be greater than max_size + 2")

    if room_count <= 0:
        raise ValueError("room_count must be greater than 0")

    if w <= 0 or h <= 0:
        raise ValueError("width and height must be greater than 0")

    rng = random.Random(seed) # Set seed of rng generation
    cells = [CellType.SOLID] * (w * h) # Initialize all cells as solid
    iterations = room_count * 8 # Number of iterations to attempt room placement, allowing for retries in case of overlaps
    candidates = (
        room
        for _ in range(iterations)
        if (room := generate_room(rng, w, h, min_size, max_size)) is not None
    ) # Generate room candidates
    
    # Helper to check if room placement is valid
    def check_placement(rooms: list[Rect], candidate: Rect) -> list[Rect]:
        if len(rooms) >= room_count:
            return rooms
        if any(candidate.intersects(room) for room in rooms):
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
