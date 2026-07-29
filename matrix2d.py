from dataclasses import dataclass
from enum import Enum, auto
from itertools import batched

# A representation of different types of cells
class CellType(Enum):
    SOLID = auto()
    FREE = auto()

# Map CellType to their corresponding character representations
cell_chars = {
    CellType.SOLID: "#",
    CellType.FREE: " ",
}

# A representation of a 2D matrix of CellType
@dataclass
class Matrix2D:
    w: int
    h: int
    cells: list[CellType]
    
# Convert a Matrix2D to a string representation
def __matrix2d_to_string(matrix2d: Matrix2D) -> str:
    if len(matrix2d.cells) != matrix2d.w * matrix2d.h:
        raise ValueError("incorrect matrix2d cell array length for given dimensions")
    
    return "\n".join(
        "".join(cell_chars[cell] for cell in row)
        for row in batched(matrix2d.cells, matrix2d.w)
    )

# Print a Matrix2D to the console
def print_matrix2d(matrix2d: Matrix2D):
    print(__matrix2d_to_string(matrix2d))