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
"""
import random
from sympy import N, Point, Triangle, convex_hull
import numpy as np
import pytest

from algorithm import bowyer_watson

TEST_POINTS = [(0, 0), (3, 0), (3, 3), (0, 3), (1, 2), (1, 1)]

# helper to check delaunay property
def assert_is_delaunay(points, triangles, tolerance=1e-9):
    as_points = [Point(x, y) for x, y in points]
    for triangle in triangles:
        circumcircle = triangle.circumcircle
        for point in as_points:
            if point not in triangle.vertices:
                d = N(circumcircle.center.distance(point))
                r = N(circumcircle.radius)
                
                assert d >= r - tolerance, f"{point} is inside the circumcircle of {triangle.vertices}"

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
    assert len(triangles) == len(set(triangles))

def test_no_empty_triangles():
    triangles = bowyer_watson(TEST_POINTS)
    for triangle in triangles:
        assert triangle.area > 0

def test_no_overlapping_triangles():
    triangles = bowyer_watson(TEST_POINTS)
    total_area = sum(abs(triangle.area) for triangle in triangles)
    ch_area = convex_hull(*[Point(x, y) for x, y in TEST_POINTS]).area
    assert total_area == ch_area

def test_super_triangle_cleanup():
    triangles = bowyer_watson(TEST_POINTS)
    for triangle in triangles:
        for vert in triangle.vertices:
            assert vert in {Point(x, y) for x, y in TEST_POINTS}

def test_delaunay_property():
    triangles = bowyer_watson(TEST_POINTS)
    assert_is_delaunay(TEST_POINTS, triangles)

@pytest.mark.parametrize("seed", range(5))
def test_delaunay_property_random(seed):
    rng = random.Random(seed)
    points = list(
        {
            (rng.randint(0, 20), rng.randint(0, 20))
            for _ in range(10)
        }
    )
    if len(points) < 3:
        pytest.skip("Generated less thatn 3 points")
    
    triangles = bowyer_watson(points)
    assert_is_delaunay(points, triangles)
