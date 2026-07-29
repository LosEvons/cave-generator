from dataclasses import dataclass
from functools import reduce
from itertools import product
import random
from typing import Tuple
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
def carve_room(cells: list[CellType], w: int, room: Rect) -> None:
    xs, ys = room.inside
    for x, y in product(range(xs.start, xs.stop), range(ys.start, ys.stop)):
        cells[xy_to_i(x, y, w)] = CellType.FREE

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
    
    # Helper to ensure adherence to room count and no overlaps
    def check_placement(candidate: Rect, rooms: list[Rect]) -> bool:
        return all(not candidate.intersects(room) for room in rooms) and len(rooms) < room_count
    
    # Helper to attempt room placement, returning updated room list if successful
    def try_place(rooms: list[Rect], candidate: Rect) -> list[Rect]:
        if not check_placement(candidate, rooms):
            return rooms
        carve_room(cells, w, candidate)
        return [*rooms, candidate]
    reduce(try_place, candidates, [])
    
    return Matrix2D(w, h, cells)
