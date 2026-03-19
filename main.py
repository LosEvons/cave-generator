import argparse
from dataclasses import dataclass
from enum import Enum, auto
from itertools import batched


class CellType(Enum):
    SOLID = auto()
    FREE = auto()


cell_chars = {
        CellType.SOLID: "#",
        CellType.FREE:  " ",
    }


@dataclass
class Matrix2D:
    w: int
    h: int
    cells: list[CellType]
    

def matrix2d_to_string(matrix2d: Matrix2D) -> str:
    if len(matrix2d.cells) != matrix2d.w * matrix2d.h:
        raise ValueError("incorrect matrix2d cell array length for given dimensions")
    
    return "\n".join(
        "".join(cell_chars[cell] for cell in row)
        for row in batched(matrix2d.cells, matrix2d.w)
    )


def print_matrix2d(matrix2d: Matrix2D):
    print(matrix2d_to_string(matrix2d))
    

def main(w: int, h: int, seed: int | None):
    print(f"width={w}, height={h}, seed={seed}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", "-W", type=int, default = 100, required=True, help="Map width")
    parser.add_argument("--height", "-H", type=int, default = 100, required=True, help="Map height")
    parser.add_argument("--seed", "-s", type=int, default=None, help="Random seed (optional)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.width,
         args.height,
         args.seed)