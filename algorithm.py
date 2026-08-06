from sympy import Point, Triangle, N, Segment
from utils import timeit
Edge = frozenset[Point]

@timeit
def bowyer_watson(points: list[tuple[int, int]]) -> list[Triangle]:
    if not points: # Check if input is empty
        return []

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
    
        e_counts: dict[Edge, int] = {}
        e_points: dict[Edge, tuple[Point, Point]] = {}
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

@timeit
def mst(triangles: list[Triangle]) -> list[Segment]:
    if not triangles: # Check if input is empty
        return []

    # Union-find initial state and tracker
    parent: dict[Point, Point] = {}

    # Helper function to find sets and perform path compression.
    # Follow links in parent until you find a vertex that points to itself.
    # If roots are equal, the vertices are in the same set and linking them would create a cycle.
    def find_set(v: Point) -> Point:
        parent.setdefault(v, v) # initialize every vertex to be its own root by default lazily
        r = v
        while parent[r] != r: # find root
            r = parent[r]
        while parent[v] != r: # path compression
            parent[v], v = r, parent[v]
        return r

    # Convert triangulation to an edge set
    raw_edges: set[Edge] = {
        frozenset(side.points) for triangle in triangles for side in triangle.sides
    }

    # Sort edge set
    sorted_edges: list[Edge] = sorted(
        raw_edges,
        key=lambda edge: tuple(edge)[0].distance(tuple(edge)[1])
    )

    # Use Kruskal's algorithm to find the minimum spanning tree
    result: list[Segment] = []
    for edge in sorted_edges:
        a, b = tuple(edge)
        root_a, root_b = find_set(a), find_set(b)
        if root_a != root_b: # are a and b in different sets.
            result.append(Segment(a, b))
            parent[root_a] = root_b

    return result

