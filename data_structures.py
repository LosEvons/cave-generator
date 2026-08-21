import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    """A 2D floating-point coordinate"""
    x: float
    y: float

    def distance(self, other) -> float:
        """Return the Euclidian distance between this point and another point"""
        return math.hypot(other.x - self.x, other.y - self.y)


@dataclass(frozen=True)
class Segment:
    """A 2D line segment defined by two Points"""
    p1: Point
    p2: Point

    @property
    def points(self) -> tuple[Point, Point]:
        """Return the two segment endpoints as an (p1, p2) tuple"""
        return self.p1, self.p2

    @property
    def length(self) -> float:
        """Return the length of the segment"""
        return self.p1.distance(self.p2)


@dataclass(frozen=True)
class Circle:
    """A 2D circle defined by a center Point and a floating point radius"""
    center: Point
    radius: float


@dataclass(frozen=True)
class Triangle:
    """A 2D triangle defined by three vertices (Points)"""
    a: Point
    b: Point
    c: Point

    @property
    def sides(self) -> tuple[Segment, Segment, Segment]:
        """Return the three triangle sides as an (ab, bc, ca) tuple"""
        return Segment(self.a, self.b), Segment(self.b, self.c), Segment(self.c, self.a)

    @property
    def vertices(self) -> tuple[Point, Point, Point]:
        """Return the three triangle vertices as an (a, b, c) tuple"""
        return self.a, self.b, self.c

    @property
    def circumcircle(self) -> Circle:
        """Return the circumcircle of the triangle"""
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
        return Circle(center, r)


    @property
    def area(self) -> float:
        """Return the area of the triangle"""
        ax, ay = self.a.x, self.a.y
        bx, by = self.b.x, self.b.y
        cx, cy = self.c.x, self.c.y
        return (
                (ax * (by - cy)
                 + bx * (cy - ay)
                 + cx * (ay - by))
                / 2
        )
