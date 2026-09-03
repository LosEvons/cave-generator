"""
Conditions to be tested against:
1. Input of three points should produce a single triangle
2. Every input point should appear in the output
3. No duplicate triangles
4. No empty triangles
5. No overlapping triangles exist
6. A set of points should produce a triangulation
    such that no point is contained in the circumcircle of any triangle
7. The super triangle is cleaned up after triangulation is done
8. Delaunay triangulation properties (triangle area sum) should match peer library function properties
"""
import random

import pytest
from scipy.spatial import QhullError
from sympy import convex_hull
from sympy import Point as SympyPoint
from data_structures import Point

from algorithm import bowyer_watson
from conftest import assert_is_delaunay, random_points, hull_area_check

TEST_POINTS = [(0, 0), (3, 0), (3, 3), (0, 3), (1, 2), (1, 1)]

def test_empty_input():
    assert bowyer_watson([]) == []

def test_three_points_produce_single_triangle():
    points = [(0, 0), (1, 0), (0, 1)]
    triangles = bowyer_watson(points)
    assert len(triangles) == 1
    assert set(triangles[0].vertices) == {Point(0, 0), Point(1, 0), Point(0, 1)}

def test_all_input_points_in_output():
    triangles = bowyer_watson(TEST_POINTS)
    start_vert = {v for triangle in triangles for v in triangle.vertices}
    end_vert = {Point(x, y) for x, y in TEST_POINTS}
    assert start_vert == end_vert

def test_no_duplicate_triangles():
    triangles = bowyer_watson(TEST_POINTS)
    vertexs = [frozenset(triangle.vertices) for triangle in triangles]
    assert len(vertexs) == len(set(vertexs)) # rotated triangles won't match, so compare vertexes instead

def test_no_empty_triangles():
    triangles = bowyer_watson(TEST_POINTS)
    for triangle in triangles:
        assert abs(triangle.area) > 0

def test_triangle_area_sum_equals_convex_hull_area_of_points():
    triangles = bowyer_watson(TEST_POINTS)
    total_area = sum(abs(triangle.area) for triangle in triangles)
    # A point-set triangulation is guaranteed to cover the convex hull of the point set, so comparing to the convex hull is guaranteed to ensure there's no triangle overlap
    ch_area = convex_hull(*[SympyPoint(x, y) for x, y in TEST_POINTS]).area # Using sympy's point representation as an exception to easily use the convex_hull function
    # The sum of the areas of the triangle being equivalent with the convex hull of the point set also means there are no empty areas inside the triangulation
    assert total_area == pytest.approx(ch_area)

def test_super_triangle_cleanup():
    triangles = bowyer_watson(TEST_POINTS)
    for triangle in triangles:
        for vert in triangle.vertices:
            assert vert in {Point(x, y) for x, y in TEST_POINTS}

def test_delaunay_property():
    triangles = bowyer_watson(TEST_POINTS)
    assert_is_delaunay(TEST_POINTS, triangles)

@pytest.mark.parametrize("seed", range(100))
def test_delaunay_property_random(seed):
    rng = random.Random(seed)
    points = list(
        {
            (rng.randint(0, 20), rng.randint(0, 20))
            for _ in range(10)
        }
    )
    if len(points) < 3:
        pytest.skip("Generated less than 3 points")
    
    triangles = bowyer_watson(points)
    assert_is_delaunay(points, triangles)


@pytest.mark.parametrize("seed", range(100))
def test_delaunay_matches_scipy(seed):
    points = random_points(seed)
    if len(points) < 3:
        pytest.skip("less than 3 points for delaunay matching, which is too few")

    try:
        area = hull_area_check(points)
    except QhullError:
        pytest.skip("Collinear input generated, skipping delaunay matching...")

    triangles = bowyer_watson(points)
    assert_is_delaunay(points, triangles) # check circumcircle property
    assert sum(abs(triangle.area) for triangle in triangles) == pytest.approx(area) # triangle area sum matches peer library function hull size