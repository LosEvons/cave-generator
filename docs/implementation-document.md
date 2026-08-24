# Implementation document

### Program structure
The program is structured as a modular pipeline, where each stage consumes the input value, and returns a new value. This makes testing and reasoning about problems easier.

The program starts by having the cli() function parse the command line arguments and call main() with them. main() directly calls generate_rooms().
generate_rooms() validates the cli inputs and then creates a 2D map representation based on them, with each cell of the map set to type SOLID. It then calls generate_room() repeatedly based on the room_count cli argument.
generate_room() randomly, within the constraints set by the min_size and max_size cli arguments, generates 2D rectangles that represent rooms on the map.
generate_rooms() validates room placement with check_placement(). If a room is invalid, it is discarded. Currently, up to room_count*8 candidates are made, so with enough invalid placements the actual number of rooms may be less than room_count. This is so that a map is generated even if the room_count is too large to fit on the specified map size.
generate_rooms() then alters the map representation by setting the cells encompassed by room rectangles to type FREE.
generate_rooms() then calls carve_hallways(), which handles creating a point set from the centers of the rooms generated previously, and handling a basic case of two rooms. It then calls boywer_watson() with the point set.
bowyer_watson() implements the Bowyer-Watson algorithm for delaunay triangulation. It returns a list of triangles, which carve_hallways() then thins out into the minimum spanning tree of the triangulation by calling mst(), which implements Kruskal's algorithm.
mst() first sorts the edges by weight (Euclidean distance between the two endpoints) and then greedily accepts any connection that doesn't create a cycle, which is checked using a union-find function that compares whether the connections already share a common root.
mst() returns a list of segments, which represents pairs of rooms that should be connected. These are then handed off by carve_hallways() to astar(), which implements the A* search algorithm. 
For A\*, the cost of a FREE cell is 0, which encourages the algorithm to use pre-existing pathways and rooms when finding optimal paths, making for a cleaner generation. astar() calls astar_step() on each segment, handling each room connection independently. It returns a list of points, which represent coordinates of cells in the 2D map that are then set to free by carve_hallways() at the end.
After carve_hallways() has carved the hallways, the map is ready and is returned to main(), which then calls print_matrix2d() to print the map to console for display, where " " is a FREE cell and "#" is a SOLID cell.

Data structures used defined in `data_tructures.py`, `generate_rooms.py` and `matrix2d.py`: `Point`, `Segment`, `Triangle`, `Circle`, `Matrix2D`, `Rect`.

### Achieved space and time complexity
- n = number of rooms, E = edges of the triangulation, V = number of grid cells (width * height)
- Bowyer-Watson triangulation: O(n^2) worst case time complexity, since for each point n, every triangle must be checked to find bad triangles. Space complexity is O(n), since the number of triangles grows linearly with the number of points.
- Kruskal's algorithm: O(E log E) time complexity from sorting the edges of the triangulation by cost, where E is the number of edges in the Delaunay triangulation, which is roughly three edges per triangle (3N). The union-find is near linear due to only having to check neighbors and only loop through the edges once. It's time complexity depends on the speed of the union-find operation, which is O(E * union_find). The total time complexity is therefore O(E log E + E * union_find). For a planar graph the edge count increases O(n) in relation to room count, so in essence the time complexity of Kruskal's algorithm is O(n log n).
- Astar search: O(E log V) time complexity for a single segment search, where V is the number of grid cells and E is approximately 4V (for the four cardinal neighbors). Space complexity is O(N) for the g_score and origin dictionaries. This is repeated for each segment, so the total time complexity is O(number of segments * V log V) in the worst case.

### Suggestions and shortcomings
- The naming and structure of the program has a few artifacts and inconsistencies, which could be clarified
- A* currently supports 4-directional movement, which could be expanded to 8 if desired.
- The data structure use and passing is inconsistent, and could be improved massively. For example, the responsibility for who sets cell types and in what form isn't exactly clear and causes an issue in cost calculation in A\*.

### Use of Large Language Models
I utilized Claude and Claude Code in sketching out program structure and requirements, as well as in debugging individual functions and calculations. No code or text was written with an LLM or copied straight from their response. I tried to keep my conversations with LLMs in the form of pseudocode when I needed clarification on something. Towards the end I also used Claude's code review capabilities to check for places to improve code quality.
I also utilized Gemini and NotebookLLM in looking up information on the algorithms and to explain the underlying logic to me, if I did not understand it by reading the source material or pseudocode.
During the writing of tests I used Claude to help me double check and work out test cases in instances where creating such cases was menial.

### Sources used:
- https://en.wikipedia.org/wiki/Delaunay_triangulation
- https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
- https://brandewinder.com/2025/04/02/delaunay-bowyer-watson-algorithm/
- https://github.com/DaveTheCelt/Triangulation
- https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
- https://pubs.ams.org/journals/proc/1956-007-01/S0002-9939-1956-0078686-7
- https://see-algorithms.com/graph/Kruskals
- https://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html
- https://en.wikipedia.org/wiki/A*_search_algorithm
- https://learngraphtheory.org/articles/a-star-search-algorithm.html