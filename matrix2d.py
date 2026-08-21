from dataclasses import dataclass
from enum import Enum, auto
from itertools import batched

class CellType(Enum):
    """The three possible states of a cell in a Matrix2D: SOLID (wall), FREE (empty space of rooms), and HALLWAY (empty space of hallways, which has lower A* cost than FREE)"""
    SOLID = auto()
    FREE = auto()
    HALLWAY = auto()

# Map CellType to their corresponding character representations
cell_chars = {
    CellType.SOLID: "#",
    CellType.FREE: " ",
    CellType.HALLWAY: " ",
}

cell_costs = {
    CellType.SOLID: 3,  # High cost for walls
    CellType.FREE: 1,      # Low cost for free space
    CellType.HALLWAY: 0,   # No cost for existing hallways
}

@dataclass
class Matrix2D:
    """A flat, row-major 2D grid of cells (CellType) with width w and height h.
    cells is a flattened list of length w * h. Use utils.xy_to_i and i_to_xy to convert
    between (x, y) coordinates and the flattened index
    """
    w: int
    h: int
    cells: list[CellType]

def __matrix2d_to_string(matrix2d: Matrix2D) -> str:
    """Convert a Matrix 2D to a string representation according to the cell_chars mapping"""
    if len(matrix2d.cells) != matrix2d.w * matrix2d.h:
        raise ValueError("incorrect matrix2d cell array length for given dimensions")
    
    return "\n".join(
        "".join(cell_chars[cell] for cell in row)
        for row in batched(matrix2d.cells, matrix2d.w)
    )


def print_matrix2d(matrix2d: Matrix2D):
    """Alias to convert and print a Matrix2D to the console"""
    print(__matrix2d_to_string(matrix2d))