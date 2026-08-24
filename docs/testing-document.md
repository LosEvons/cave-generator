# Testing Document

## Unit test coverage
Coverage is currently at 65%, which is mostly caused by the project skeleton in generate_rooms.py not being tested currently. The test files and main.py are omitted from coverage results.
Coverage is run every time tests are run.

## Testing strategy
Tests are split into per algorithm into three files. Each algorithm is tested against its mathematical definition. The algorithms are also tested against bad inputs.
Here's a comprehensive breakdown of the conditions tested for each algorithm:
- **Bowyer-Watson**
1. Input of three points should produce a single triangle
2. Every input point should appear in the output
3. No duplicate triangles
4. No empty triangles
5. No overlapping triangles exist
6. A set of points should produce a triangulation
    such that no point is contained in the circumcircle of any triangle
7. The super triangle is cleaned up after triangulation is done
- **Kruskal's Algorithm**
1. Empty input produces an empty output
2. For a single triangle bowyer_watson input produces a valid MST
3. For a point cloud bowyer_watson input produces a valid MST
4. For any input, the edges of the MST are a subset of the edges of the triangulation
5. Output is a valid spanning tree
6. Output satisfies the cut property
- **A\* Search**
1. A straight FREE grid produces the shortest path from start to goal
2. A start point equal to end point returns a single point path
3. A cheaper path around SOLID is preferred to crossing it
4. An out-of-bounds start or end raises error
5. astar() combines paths of multiple segments in the correct order

The tests use both fixed hand-picked inputs to check basic structural properties, such as when checking whether the output is consistent with the algorithm's definition, and randomly generated inputs with fixed seeds for general fuzz-style testing. For Bowyer-Watson the inputs come in the form of point sets, and for A* they come in the form of Matrix2D grids.

The tests can be reproduced with the following commands:

```
poetry install
poetry run pytest
```
