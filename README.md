# TL;DR
Creates plots of percolation on square lattices using matplotlib. The user can control the parameter p and the row/column count. 

# Percolation
Given a graph G = (V, E) with vertices and edges (e.g. a 2d grid) and a given probability p with 0 < p < 1, we transform the graph G in the following way: Each edge e remains with probability p (or gets deleted with probability 1-p). Whether a given edge remains or not is independent of the others. This is percolation. 

The resulting graph contains multiple clusters of connected vertices ("Connected components"). If the graph G contains infinitely many vertices, mathematicians are interested whether a cluster with infinitely many vertices exists. In the example of the square lattice, this is always true when p >= 0.5 and always false when p < 0.5

For more information, check out https://en.wikipedia.org/wiki/Percolation_theory

# This program
From now on, consider G = (V, E) to be the square lattice, where each vertex has 4 neighbors (except for the edge cases). One can plot a percolated graph by representing each vertex as a pixel. A neighboring vertex has the same color if and only if it is connected. This way, the different connected components can be visualized.

The following code generates percolated square lattices and plots them using matplotlib. The amount of rows and columns, the probability p and the seed can be adjusted manually. The generated plots can be saved in a custom folder. 

# How to use
main.py and Percolation.py need to be in the same folder. Percolation.py contains all the functionality for defining lattices, creating percolated graphs etc. while main.py is a simple console application to do test runs. You can either use main.py to create one percolated graph (with different parameters) at a time or use the functions provided in Percolation.py directly.

# Examples

https://github.com/BanachBranch/Percolation/blob/main/Example%20Plots/Perc_Rows_600_Prob_0.47_Seed_100.png
