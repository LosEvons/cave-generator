# Specification Document
This project is a continuation of an earlier work of mine from the spring course, which was left unfinished.
### Programming language used : Python
### Other programming languages I know : C, C++, JavaScript/TypeScript
### Algorithms and data structures implemented:
- Room generation (random rectangle placement with overlap checks)
- Delaunay Triangulation with the Bowyer-Watson algorithm
- Minimum spanning tree with Kruskal's algorithm from the triangulation above
- A* search algorithm to connect the rooms with hallways 
### Problem being solved
- Creating interesting maps for games by hand is slow and takes a lot of resources.
### Program input
- Map width and height, number of rooms, and seed for the random number generator
### Target time and space complexity:
- Time complexity approximately O(n²), where n is the number of rooms.
- Space complexity approximately O(n), since the size of the triangulation grows linearly with the number of points (rooms)

### Intended sources
- https://vazgriz.com/119/procedurally-generated-dungeons/
- Descriptions of algorithm and previous implementations in the found teaching materials

### Core of the project
- Procedural generation and graph algorithms

### Other
- Bachelor's degree in Computer Science (TKT)
- English is the primary documentation language