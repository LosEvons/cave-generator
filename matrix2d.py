from dataclasses import dataclass
from enum import Enum, auto

from data_structures import Point


class CellType(Enum):
    """The three possible states of a cell in a Matrix2D: SOLID (wall), FREE (empty space of rooms), and HALLWAY (empty space of hallways, which has lower A* cost than FREE)"""
    SOLID = auto()
    FREE = auto()

# Map CellType to their corresponding character representations
cell_chars = {
    CellType.SOLID: "#",
    CellType.FREE: " ",
}

# Set A* traverse costs for cell types
cell_costs = {
    CellType.SOLID: 10,  # High cost for walls
    CellType.FREE: 1,   # Zero cost for free space
}

@dataclass
class Matrix2D:
    """A row-major 2D grid of cells (CellType) with width w and height h.
    """
    w: int
    h: int
    cells: list[list[CellType]]

    def carve_cell(self, point: Point) -> None:
        """Sets the cell type of cell in the matrix to FREE"""
        self.cells[point.y][point.x] = CellType.FREE

    def get_cell(self, point: Point) -> CellType:
        """Returns the CellType of a cell in the matrix for a Point"""
        return self.cells[point.y][point.x]

    def set_cell(self, point: Point, cell: CellType) -> None:
        """Sets the CellType of a cell in the matrix for a Point"""
        self.cells[point.y][point.x] = cell

    def get_cell_cost(self, point: Point) -> int:
        """Returns the traversal cost of a cell in the matrix for a Point"""
        return cell_costs.get(self.get_cell(point), 0)

    def copy(self):
        """Returns a copy of this Matrix2D"""
        return Matrix2D(self.w, self.h, [row[:] for row in self.cells])

    @property
    def as_string(self) -> str:
        """Returns a string representation of this Matrix2D"""
        return "\n".join(
            "".join(cell_chars[cell] for cell in row)
            for row in self.cells
        )
