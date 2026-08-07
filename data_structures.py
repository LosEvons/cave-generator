import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Edge:
    start: Point
    end: Point

    @property
    def length(self) -> float:
        return math.hypot(self.start.x - self.end.x, self.start.y - self.end.y)


@dataclass(frozen=True)
class Triangle:
    a: Point
    b: Point
    c: Point

    @property
    def _edges(self) -> tuple[Edge, Edge, Edge]:
        return Edge(self.a, self.b), Edge(self.b, self.c), Edge(self.c, self.a)

    @property
    def circumcircle(self) -> tuple[Point, float]:
        ax, ay = self.a.x, self.a.y
        bx, by = self.b.x, self.b.y
        cx, cy = self.c.x, self.c.y

        determinant = 2 * (
                ax * (by - cy)
                + bx * (cy - ay)
                + cx * (ay - by)
        )
        if determinant == 0:
            raise ValueError("no circumcircle exists")

        ux = (
        (ax**2 + ay**2) * (by - cy)
        + (bx**2 + by**2) * (cy - ay)
        + (cx**2 + cy**2) * (ay - by)
        ) / determinant

        uy = (
        (ax**2 + ay**2) * (cx - bx)
        + (bx**2 + by**2) * (ax - cx)
        + (cx**2 + cy**2) * (bx - ax)
        ) / determinant

        center = Point(ux, uy)
        r = math.hypot(ax - ux, ay - uy)
        return center, r
