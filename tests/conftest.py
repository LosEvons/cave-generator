import itertools
import random
from collections.abc import Iterable

import networkx as nx
import numpy as np
from scipy.spatial import Delaunay, ConvexHull
from data_structures import Point, Segment, Triangle

from algorithm import Edge

def random_points(seed, n=13, lo=0, hi=25):
    """A list of random integer (x, y) points"""
    rng = random.Random(seed)
    return list(
        {
            (rng.randint(lo, hi), rng.randint(lo, hi))
            for _ in range(n)
        }
    )

def get_vertices(triangles: list[Triangle]) -> set[Point]:
    return {v for t in triangles for v in t.vertices}

def get_edges(triangles: list[Triangle]) -> set[Edge]:
    return {frozenset(e.points) for t in triangles for e in t.sides}

def edge_length(edge: Edge):
    a, b = tuple(edge)
    return Segment(a, b).length

def total_weight(edges: Iterable[Segment]):
    return sum(e.length for e in edges)

def build_graph(edges: set[Edge]) -> nx.Graph:
    graph = nx.Graph()
    for e in edges:
        a, b = tuple(e)
        graph.add_edge(a, b, weight=Segment(a, b).length)
    return graph

def is_spanning_tree(edges: set[Edge], vertices: set[Point]) -> bool:
    graph = build_graph(edges)
    graph.add_nodes_from(vertices)
    return set(graph.nodes) == vertices and nx.is_tree(graph)

def mst_weight_check(edges):
    return nx.minimum_spanning_tree(build_graph(edges)).size(weight="weight")

def hull_area_check(points):

    return ConvexHull(np.asarray(points, dtype=float)).volume
def triangle_count_check(points):
    return len(
        Delaunay(np.asarray(points, dtype=float)).simplices
    )

def has_cycle_property(mst_edges: set[Edge], all_edges: set[Edge]) -> bool:
    graph = build_graph(mst_edges)
    for e in all_edges - mst_edges:
        a, b = tuple(e)
        path = nx.shortest_path(graph, a, b)
        path_edges = [frozenset((path[i], path[i + 1])) for i in range(len(path) - 1)]
        if any(edge_length(path_edge) > edge_length(e) for path_edge in path_edges):
            return False
    return True


def assert_is_delaunay(points, triangles, tolerance=1e-9):
    as_points = [Point(x, y) for x, y in points]
    for triangle in triangles:
        circumcircle = triangle.circumcircle
        for point in as_points:
            if point not in triangle.vertices:
                d = circumcircle.center.distance(point)
                r = circumcircle.radius

                assert d >= r - tolerance, f"{point} is inside the circumcircle of {triangle.vertices}"


def cost_graph(matrix) -> nx.Graph:
    """A 4 neighbor grid with edge weight being cell cost of target cell. Mirrors astar.cost_function. Used for comparison with library function."""
    graph = nx.grid_2d_graph(matrix.w, matrix.h).to_directed()
    for a, b in graph.edges:
        graph.edges[a,b]["weight"] = matrix.get_cell_cost(Point(*b))
    return graph

def path_cost(path, matrix) -> int:
    return sum(matrix.get_cell_cost(p) for p in path[1:])

def path_is_contiguous(path) -> bool:
    """Make sure path has no interruptions"""
    return all(
        abs(a.x - b.x) + abs(a.y - b.y) == 1 for a, b in zip(path, path[1:])
    )