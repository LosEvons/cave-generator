# Testing Document

## Unit test coverage
Coverage is currently at 98%. The test files, utils.py and main.py are omitted from coverage results.

## Testing strategy
Tests are split into per algorithm into four files. Each algorithm is tested against its mathematical definition. The algorithms are also tested against bad inputs. The tests try their best to check for properties of the data structures and algorithms, but also rely on reviewing against peer implementations in third party libraries, especially in mass randomized testing. The issue with the latter approach is it is harder to pinpoint the actual problem. That's why I've done my best to create tests that, when failing, help locate the source of the issue as accurately as possible.
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
8. Delaunay triangulation properties (triangle area sum) should match peer library function properties
- **Kruskal's Algorithm**
1. Empty input produces an empty output
2. For a single triangle bowyer_watson input produces a valid MST
3. For a point cloud bowyer_watson input produces a valid MST
4. For any input, the edges of the MST are a subset of the edges of the triangulation
5. Output is a valid spanning tree
6. Output satisfies the cut property
7. MST produced by mst() should match the weight of a peer library function
- **A\* Search**
1. A straight FREE grid produces the shortest path from start to goal
2. A start point equal to end point returns a single point path
3. A cheaper path around SOLID is preferred to crossing it
4. An out-of-bounds start or end raises error
5. astar() combines paths of multiple segments in the correct order
6. astar() will prefer existing hallways to carving new ones
7. astar_step() path should be contiguous, and the shortest path found should have length matching with the shortest path found with Dijkstra library function
- **Generate rooms**
1. Rect.intersects correctly handles overlapping and padding
2. carve_room only carves tiles from the room interior
3. generate_room always adheres to bounds and size constraints
4. generate_rooms validates inputs and raises correctly
5. generate_rooms is deterministic (same result for same seed)
6. generate_rooms produces a fully connected map

The tests use both fixed hand-picked inputs to check basic structural properties, such as when checking whether the output is consistent with the algorithm's definition, and randomly generated inputs with fixed seeds for general fuzz-style testing. For Bowyer-Watson the inputs come in the form of point sets, and for A* they come in the form of Matrix2D grids.
Some tests utilize networkx to calculate things like connectedness and convex hull to check results against mathematical conditions, so I don't have to write that logic myself, but can focus on the core algorithm implementation.
test_generate_rooms_produces_fully_connected_map is an example of e2e testing in this project.

Testing was furthered and slightly altered towards the very end of the project, which led to tests with mismatching styles and philosophies. I've since made sure to check that each test tests something relevant and does it in a valid way. I've tried to ensure no test fails without a good.

The tests can be reproduced with the following commands:

```
poetry install
poetry run pytest
```
