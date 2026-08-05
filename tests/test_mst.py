"""
Conditions to be tested against:
1. Empty input produces an empty output
2. For a single triangle bowyer_watson input produces a valid MST
3. For a point cloud bowyer_watson input produces a valid MST
4. For any input, the edges of the MST are a subset of the edges of the triangulation
5. Output is a valid spanning tree
6. Output satisfies the cut property
"""

import pytest
from sympy import Point, Segment, Triangle, Expr
import itertools
from collections.abc import Iterable
import networkx as nx

from algorithm import bowyer_watson, mst

MOCK_POINTS = {
    "triangle": [(0, 0), (3, 0), (0, 4)],
    "cloud": [(0, 0), (4, 0), (4, 4), (0, 4), (2, 2)],
    "grid": [(x, y) for x in range(3) for y in range(3)] # equal weights for all edges
}

def get_vertices(triangles: list[Triangle]) -> set[Point]:
    return {v for t in triangles for v in t.vertices}

def get_edges(triangles: list[Triangle]) -> set[frozenset[Point]]:
    return {frozenset(e.points) for t in triangles for e in t.sides}

def edge_length(edge: frozenset[Point]) -> Expr:
    a, b = tuple(edge)
    return Segment(a, b).length

def total_weight(edges: Iterable[Segment]) -> Expr:
    return sum(e.length for e in edges)

def build_graph(edges: set[frozenset[Point]]) -> nx.Graph:
    graph = nx.Graph()
    for e in edges:
        a, b = tuple(e)
        graph.add_edge(a, b, weight=Segment(a, b).length)
    return graph

def is_spanning_tree(edges: set[frozenset[Point]], vertices: set[Point]) -> bool:
    graph = build_graph(edges)
    graph.add_nodes_from(vertices) # catch isolated vertices
    return set(graph.nodes) == vertices and nx.is_tree(graph)

def brute_force_weight(edges: set[frozenset[Point]], vertices: set[Point]) -> Expr:
    n_edges = len(vertices) - 1
    best = None
    for combination in itertools.combinations(edges, n_edges):
        if is_spanning_tree(set(combination), vertices):
            weight = sum(edge_length(e) for e in combination)
            if best is None or weight < best:
                best = weight
    return best

def has_cut_property(mst_edges: set[frozenset[Point]], all_edges: set[frozenset[Point]]) -> bool:
    graph = build_graph(mst_edges)
    for e in all_edges - mst_edges:
        a, b = tuple(e)
        path = nx.shortest_path(graph, a, b)
        path_edges = [frozenset((path[i], path[i + 1])) for i in range(len(path) - 1)]
        if any(edge_length(path_edge) > edge_length(e) for path_edge in path_edges):
            return False
    return True

def test_empty_input():
    assert mst([]) == []

def test_single_triangle_weight():
    triangles = bowyer_watson(MOCK_POINTS["triangle"])
    tree = mst(triangles)
    assert sorted(n.length for n in tree) == [3, 4]

def test_cloud_weight():
    triangles = bowyer_watson(MOCK_POINTS["cloud"])
    raw_edges = get_edges(triangles)
    vertices = get_vertices(triangles)
    tree = mst(triangles)
    assert total_weight(tree) == brute_force_weight(raw_edges, vertices)

@pytest.mark.parametrize("points", MOCK_POINTS.values(), ids=MOCK_POINTS.keys())
def test_edges_are_subset_of_triangulation(points):
    triangles = bowyer_watson(points)
    raw_edges = get_edges(triangles)
    tree = mst(triangles)
    assert all(frozenset(e.points) in raw_edges for e in tree)

@pytest.mark.parametrize("points", MOCK_POINTS.values(), ids=MOCK_POINTS.keys())
def test_mst_result_is_valid_spanning_tree(points):
    triangles = bowyer_watson(points)
    vertices = get_vertices(triangles)
    tree = mst(triangles)
    mst_edges = {frozenset(e.points) for e in tree}
    assert is_spanning_tree(mst_edges, vertices)

@pytest.mark.parametrize("points", MOCK_POINTS.values(), ids=MOCK_POINTS.keys())
def test_mst_result_has_cut_property(points):
    triangles = bowyer_watson(points)
    edges = get_edges(triangles)
    tree = mst(triangles)
    mst_edges = {frozenset(e.points) for e in tree}
    assert has_cut_property(mst_edges, edges)