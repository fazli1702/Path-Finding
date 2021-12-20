# Path Finding Visualisation

This is a path finding algorithm animation which helps visualise how the path finding algorithms works.
There are 4 algorithm included and they are
- A Star (A*)
- Dijkstra's
- Depth First Search (DFS)
- Breadth First Search (BFS)

The program also can display how a maze can be generated using recursive backtracking.

This program is coded in python and uses the pygame library as the GUI.

***

## Algorithms

**Dijkstra's** algorithm is one of the most famous path finding algorithm and is
also the foundation for many other algorithms. It uses a priority queue to
sort out the nodes in the graph and find the end node. 

**A star** or A* algorithm is an improved version of the Dijkstra's algorithm
where it reduce redundancy by calculating the distance of the current node
to the end node. This ensures that the algorithm does not serach in the direction
that is going away from the end node. 

**DFS** algorithm starts at the root node (selecting some arbitrary node as the root
node in the case of a graph) and explores as far as possible along each branch before
backtracking.

**BFS** algorithm is largely similar to Dijkstra's but uses a regular queue instead
of a priority queue.

**Recursive Backtracking** algorithm works by firstly choosing a random start node and
check if its neighbouring nodes have been visited. If there are nodes that have not been
visited, randomly visit and unvisited node and mark it as visited. Repeat this until
it reaches a node that has no unvisited neighbours, where the algorithm will then
backtrack to the last node that still have unvisited neighbours. The algorithm stops
once it reaches the start node.

***

## Running the program

Before running the program, ensure that pygame have been installed.
This can be done by running   
`pip install pygame` or `python -m pip install pygame`

To run the program, execute `main.py`
```
$ python main.py
```

Right click
- Set start / end node (first 2 click respectively)
- Set wall nodes
- Set algorithm (select at bottom)

Left click
- Remove start / end node
- Remove wall node

Press `m` to generate maze  
Press `r` to reset graph
***

## References
- https://www.youtube.com/watch?v=GC-nBgi9r0U&t=104s

### Dijkstra's
- https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm  
- https://www.youtube.com/watch?v=GazC3A4OQTE&t=17s


### A*
- https://en.wikipedia.org/wiki/A*_search_algorithm
- https://www.youtube.com/watch?v=ySN5Wnu88nE&t=223s
- https://www.youtube.com/watch?v=-L-WgKMFuhE&t=116s
- https://www.youtube.com/watch?v=JtiK0DOeI4A (main reference for code)

### DFS
- https://en.wikipedia.org/wiki/Depth-first_search#:~:text=Depth%2Dfirst%20search%20(DFS),along%20each%20branch%20before%20backtracking.
- https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
- https://www.hackerearth.com/practice/algorithms/graphs/depth-first-search/tutorial/
- https://www.youtube.com/watch?v=7fujbpJ0LB4&t=294s

### BFS
- https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
- https://www.youtube.com/watch?v=oDqjPvD54Ss

### Recursive Backtracking
- http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking