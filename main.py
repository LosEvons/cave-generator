import argparse
from dataclasses import dataclass
from enum import Enum, auto

class CellType(Enum):
    SOLID = auto()
    FREE = auto()


@dataclass
class Matrix2D:
    w: int
    h: int
    cells: list[CellType]
    

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