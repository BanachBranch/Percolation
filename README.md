# TL;DR
Creates plots of percolation on square lattices using matplotlib. The user can control the parameter p and the row/column count. 

# Percolation
Given a graph G = (V, E) with vertices and edges (e.g. a 2d grid) and a given probablity p with 0 < p < 1, we transform the graph G in the following way: Each edge e remains with probability p (or gets deleted with probablity 1-p). Whether a given edge remains or not is independent from the others. This is percolation. 

The resulting graph contains multiple clusters of connected vertices ("Connected components"). If the graph G contains infinitely many vertices, mathematicians may study whether a cluster with infinitely many vertices exists. In the example of the square lattice, this is always true when p >= 0.5 and always false when p < 0.5

For more information, check out https://en.wikipedia.org/wiki/Percolation_theory

# This program
From now on, consider G = (V, E) to be the square lattice, where each vertex has 4 neighbors (except for the edge cases). One can plot a percolated graph by representing each vertex as a pixel. A neighboring vertex has the same color if and only if it is connected. This way, the different connected components can be visualized.

The following code generates percolated square lattices and plots them using matplotlib. The amount of rows and columns, the probability p and the seed can be adjusted manually. The generated plots can be saved in a custom folder. 
