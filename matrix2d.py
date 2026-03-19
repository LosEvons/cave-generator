from dataclasses import dataclass
from enum import Enum, auto
from itertools import batched


class CellType(Enum):
    SOLID = auto()
    FREE = auto()


cell_chars = {
    CellType.SOLID: "#",
    CellType.FREE: " ",
}


@dataclass
class Matrix2D:
    w: int
    h: int
    cells: list[CellType]
    

def __matrix2d_to_string(matrix2d: Matrix2D) -> str:
    if len(matrix2d.cells) != matrix2d.w * matrix2d.h:
        raise ValueError("incorrect matrix2d cell array length for given dimensions")
    
    return "\n".join(
        "".join(cell_chars[cell] for cell in row)
        for row in batched(matrix2d.cells, matrix2d.w)
    )


def print_matrix2d(matrix2d: Matrix2D):
    print(__matrix2d_to_string(matrix2d))