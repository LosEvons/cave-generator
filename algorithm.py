from sympy import Point, Triangle, N

def bowyer_watson(points: list[tuple[int, int]]) -> list[Triangle]:
    # Format input points into correct data form
    points = [Point(x, y) for x, y in points]

    # Create a super triangle that encompasses all input points
    min_x, max_x = min(p.x for p in points), max(p.x for p in points)
    min_y, max_y = min(p.y for p in points), max(p.y for p in points)
    dx, dy = max_x - min_x, max_y - min_y
    d = max(dx, dy, 1) * 10 # Just a very big number to ensure triangle encompasses all points
    super_triangle = Triangle(
        Point(min_x - d, min_y - d),
        Point(min_x + 2 * d + dx, min_y - d),
        Point(min_x - d, min_y + 2 * d + dy)
    )

    triangles: set[Triangle] = {super_triangle}

    # Iteratively add points to the triangulation
    for point in points:
        # Check and collect bad triangles
        bad_triangles = {
            t for t in triangles
            if N(t.circumcircle.center.distance(point)) <= N(t.circumcircle.radius)
        }
    
        e_counts: dict[frozenset, int] = {}
        e_points: dict[frozenset, tuple[Point, Point]] = {}
        for triangle in bad_triangles:
            for edge in triangle.sides:
                k = frozenset(edge.points)
                e_counts[k] = e_counts.get(k, 0) + 1
                e_points[k] = edge.points

        bound = [e_points[k] for k, i in e_counts.items() if i == 1]

        for triangle in bad_triangles:
            triangles.discard(triangle)
        
        for a, b in bound:
            triangles.add(Triangle(a, b, point))
    
    return [
        triangle for triangle in triangles
        if not set(triangle.vertices) & set(super_triangle.vertices)
    ] # Remove super triangle and attached triangles


#def msp(triangles: list[Triangle]) -> list[Edge]:
    # triangles to weighted edges by distance
    # figure out algo to use for this
    # TODO

#def astar(edge: Edge) -> list[Point]:
    # find and return path for a single edge per call
    # TODO