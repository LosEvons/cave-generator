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

from algorithm import bowyer_watson, mst
from conftest import (
    get_vertices,
    get_edges,
    total_weight,
    is_spanning_tree,
    brute_force_weight,
    has_cut_property,
)

MOCK_POINTS = {
    "triangle": [(0, 0), (3, 0), (0, 4)],
    "cloud": [(0, 0), (4, 0), (4, 4), (0, 4), (2, 2)],
    "grid": [(x, y) for x in range(3) for y in range(3)]
}

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