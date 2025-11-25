import numpy as np
import copy

import matplotlib.pyplot as plt
# from matplotlib.colors import ListedColormap
import os


class Percolation:
    """
    Represents distinct instances of percolation.
    self.rows           = number of rows the square grid contains
    self.vertex_count   = number of vertices in the grid, equal to self.rows^2
    self.prob           = probability of an edge to remain after percolation
    self.seed           = numpy seed

    self.adj_dict       = dictionary, represents graph of original grid (adjacency list).
    self.perc_adj_dict  = dictionary, represents graph of grid post percolation (adjacency list).

    self.clusters_mat   = matrix, shape = (self.rows, self.rows), values represent the assigned cluster of corresponding vertex.
    self.colors_mat     = matrix, shape = (self.rows, self.rows), values represent color used for plotting
    self.colors_dict    = dictionary, keys = vertices of grid  &  values = coloring
    self.colors_used    = integer, amount of colors used
    """

    def __init__(self, rows, p, verbose=0, random_seed=True, seed=0):
        """
        If verbose = 1, prints statements.
        """
        self.colormap = {}
        self.rows = rows
        self.vertex_count = rows ** 2
        self.prob = p
        self.seed = seed

        if not random_seed:
            np.random.seed(self.seed)

        # Original Adjacency Representation
        if verbose == 1:
            print("Creates adjacency list of original graph.")
        self.adj_dict = get_adjacency_list(self.rows)

        # Percolation
        if verbose == 1:
            print("Creates adjacency list of percolated graph.")
        self.perc_adj_dict = get_percolated_adjacency_list(self.rows, self.prob)

        # Find clusters
        if verbose == 1:
            print("Finds clusters using DFS")
        temp = find_clusters(self.perc_adj_dict, self.rows)
        self.clusters_mat = copy.copy(temp)
        self.clusters_mat = np.reshape(self.clusters_mat, newshape=(self.rows, self.rows)).astype(int)

        # Calculate coloring
        if verbose == 1:
            print("Calculate coloring using Greedy Coloring Algorithm")
        self.color_dict = greedy_coloring(temp, self.adj_dict)

        # Calculate coloring matrix
        self.color_mat = get_coloring_matrix(self.clusters_mat, self.color_dict).astype(int)
        self.colors_used = self.color_mat.max()

        # Default colormap
        colors = [
            (190, 0, 0),  # Red
            (136, 0, 136),  # Magenta
            (0, 0, 160),  # Blue
            (255, 255, 0),  # Yellow
            (0, 160, 0),  # Green
            (0, 170, 255),  # Cyan
            (255, 128, 0),  # Orange
            (128, 64, 0)  # Brown
        ]
        self.colormap = self.set_colormap(colors)

    def set_colormap(self, colors):
        """
        colormap is a dictionary which defines what colors to use for the clusters.
        """

        self.colormap = {}
        for index, color in enumerate(colors):
            self.colormap[index] = color

        return self.colormap

    def set_default_colormap(self):

        colors = [
            (190, 0, 0),  # Red
            (0, 200, 0),  # Green
            (0, 0, 160),  # Blue
            (255, 255, 0),  # Yellow
            (255, 128, 0),  # Orange
            (136, 0, 136),  # Magenta
            (0, 170, 255),  # Cyan
            (128, 64, 0)  # Brown
        ]

        self.colormap = self.set_colormap(colors)

    def plot(self, use_colormap=True):
        """
        Plots percolation.
        """

        if use_colormap:

            rgb_array = np.zeros((*self.color_mat.shape, 3), dtype=np.uint8)
            for key, color in self.colormap.items():
                rgb_array[self.color_mat == key] = color

            plt.imshow(rgb_array)

        # Plot Details
        else:
            plt.imshow(self.color_mat)

        plt.title(f"Percolation for p = {self.prob} and n = {int(np.sqrt(self.vertex_count))}")
        plt.show()

    def save_fig(self, name, dpi=1200, use_colormap=True):
        if use_colormap:

            rgb_array = np.zeros((*self.color_mat.shape, 3), dtype=np.uint8)
            for key, color in self.colormap.items():
                rgb_array[self.color_mat == key] = color

            plt.imshow(rgb_array)

        # Plot Details
        else:
            plt.imshow(self.color_mat)

        plt.title(f"Percolation for p = {self.prob}, n = {int(np.sqrt(self.vertex_count))}, seed = {self.seed}")

        plt.savefig(name, dpi=dpi)
        plt.close()


def get_adjacency_list(n):
    """
    Creates square 2d grid with n*n many nodes.
    """
    grid = {}

    for row in range(n):
        for col in range(n):
            node = row*n + col
            temp = []

            # Add edges
            if col < n-1: 
                # Right neighbor exists
                temp.append(node + 1)
            if 0 < col:
                # Left neighbor exists
                temp.append(node - 1)
            if 0 < row:
                # Top neighbor exists
                temp.append(node - n)
            if row < n-1:
                # Bottom neighbor exists
                temp.append(node + n)

            grid[node] = copy.copy(temp)

    return grid


def get_percolated_adjacency_list(n, p):
    """
    Calculates the dictionary representation of a percolated graph with n rows/cols and a probability p for each edge
    to remain.
    Given an original adjacency list of a 2d grid, keeps each edge with probability p, independently for each edge.
    """
    grid = {}

    for row in range(n):
        for col in range(n):
            node = row * n + col
            temp = []

            # Add edges with probability p when possible
            if col < n - 1:
                unif = np.random.uniform(0, 1)
                if unif <= p:
                    temp.append(node + 1)
            if 0 < col:
                unif = np.random.uniform(0, 1)
                if unif <= p:
                    temp.append(node - 1)
            if 0 < row:
                unif = np.random.uniform(0, 1)
                if unif <= p:
                    temp.append(node - n)
            if row < n - 1:
                unif = np.random.uniform(0, 1)
                if unif <= p:
                    temp.append(node + n)

            grid[node] = copy.copy(temp)

    return grid


def find_clusters(graph, rows):
    """
    Using DFS, assigns cluster number for each vertex.

    Input: Dictionary representing Graph
    Output: Array representing the grid, values are cluster numbers and indices are nodes.
    """
    result = np.zeros(len(graph))
    marked = ["unmarked" for i in range(len(graph))]
    group = 0

    for node in graph.keys():

        # If node unvisited, perform DFS starting from node. ---------------
        if marked[node] == "unmarked":

            # Node not part of already found groups.
            group += 1

            stack = [node]
            while len(stack) > 0:
                # Mark current node
                current_node = stack.pop()
                marked[current_node] = "marked"
                result[current_node] = group

                # Find all unmarked neighbors
                for neighb in graph[current_node]:
                    if marked[neighb] == "unmarked":
                        stack.append(neighb)

    return result


def greedy_coloring(clusters, grid):
    """
    Finds a valid coloring using greedy algorithm.

    Input:
    clusters            = Array of cluster numbers
    grid                = Dictionary representing the graph of the grid.

    Output:
    cluster_coloring    = dictionary, keys = vertices of grid  &  values = coloring
    """

    # Constructs graph ------------------------------------------
    # with vertices = clusters and edges = clusters neighboring each other. (DIFFERENT from grid!)

    graph = {cluster_val: [] for cluster_val in clusters.tolist()}

    # Add neighboring cluster values
    for node in grid.keys():
        cluster_val = clusters[node]

        # Add neighboring cluster values if not yet counted
        for neighbor_node in grid[node]:
            if cluster_val != clusters[neighbor_node] and clusters[neighbor_node] not in graph[cluster_val]:
                graph[cluster_val].append(clusters[neighbor_node])

    # Calculate coloring with greedy algorithm --------------

    def first_available_color(used_colors):

        # Finds first unused color
        color = 1
        while color in used_colors:
            color += 1

        return color

    cluster_coloring = {}

    for cluster_val in clusters.tolist():
        neighboring_colors = [cluster_coloring[neighbor] for neighbor in graph[cluster_val] if neighbor in cluster_coloring.keys()]
        cluster_coloring[cluster_val] = first_available_color(neighboring_colors)

    return cluster_coloring


def get_coloring_matrix(clusters_mat, cluster_coloring):
    """
    matrix is connected_groups, coloring is a dictionary, returns matrix with updated values.

    Input:
    clusters_mat        = matrix, values representing cluster numbers of vertex
    cluster_coloring    = dictionary, keys = vertex of grid  &  values = coloring used

    Output:
    color_mat           = like clusters_mat except values are representing coloring used
    """

    color_mat = copy.copy(clusters_mat)

    for cluster_val in cluster_coloring.keys():
        color_mat[clusters_mat == cluster_val] = cluster_coloring[cluster_val]

    return color_mat


def create_plots(p, path, seed, n, verbose=1):


    if not os.path.exists(f"{path}"):
        os.makedirs(f"{path}")

    perc = Percolation(n, p, random_seed=False, seed=seed, verbose=verbose)
    perc.save_fig(f"{path}/Perc_Rows_{perc.rows}_Prob_{perc.prob}_Seed_{perc.seed}.png", dpi=1200)


if __name__ == "__main__":

    import time
    start = time.perf_counter()

    # CUSTOM VARIABLES
    probabilities = [0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53]
    path = "./Generated_Plots"
    seed = 100
    n = 40

    for i, prob in enumerate(probabilities):
        print(f"\n Run {i+1} with probability {prob}")
        create_plots(prob, path, seed, n)

    end = time.perf_counter()
    
    print(f"\nDuration: {int(np.round((end - start)//60, 0))} Minutes and {int(np.round((end - start)%60, 0))} Seconds.")

