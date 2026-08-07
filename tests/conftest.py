import itertools
from collections.abc import Iterable

import networkx as nx
from data_structures import Point, Segment, Triangle

from algorithm import Edge

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

def brute_force_weight(edges: set[Edge], vertices: set[Point]):
    n_edges = len(vertices) - 1
    best = None
    for combination in itertools.combinations(edges, n_edges):
        if is_spanning_tree(set(combination), vertices):
            weight = sum(edge_length(e) for e in combination)
            if best is None or weight < best:
                best = weight
    return best


def has_cut_property(mst_edges: set[Edge], all_edges: set[Edge]) -> bool:
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
