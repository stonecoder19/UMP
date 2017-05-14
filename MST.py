import math
import sys
from utils.Graph import Graph

class MST:
    
    def __init__(self, graph):
        self.graph = graph

    def compute_mst(self):
        
        """
        Computes a minimum spanning tree from the graph using Prim's algorithm
        Choose an arbitrary node n.
        Initialize two sets, U={n} and V=G \{n}.
 
        Repeat for (N-1) steps:
            Choose the minimum cost edge (a,b) between U and V such that a belongs to 
            U and b belongs to V. Remove b from V and add b to U.
        Returns:
            Graph: new graph from minimum spanning tree

        """

        new_graph = Graph()
        visited = []
        adjacency_matrix = {}
        
        #iterates over each node in graph and adds only nodes with neighbours to the new graph
        for node in self.graph.get_nodes():
            if self.graph.get_node(node).get_neighbors():
                new_graph.add_node(node, self.graph.get_node(node).get_pos())
        
        #add first node to visited
        current_node = self.graph.get_nodes()[0]
        visited.append(current_node)
        
        count = 1 #used as a terminator for the loop
        
        while count < len(self.graph.get_nodes()):
            neighbours = self.graph.get_node(current_node).get_neighbors()
            row = {}
            for j in neighbours:
                row[j] = self.graph.get_node(current_node).get_cost(j)
                
            adjacency_matrix[current_node] = row

            min_from, min_to = self.select_min_edge(adjacency_matrix, visited)
            count += 1
            if min_from == -1 or min_to == -1:
                continue
            new_graph.add_edge(min_from, min_to)
            current_node = min_to
            visited.append(current_node)
        return new_graph

    
    def select_min_edge(self, matrix, visited):
        """
        Finds the edge with the least cost in the graph and returns
        the two nodes connecting that edge

        Args:
            matrix(dict): adjaceny matrix of graph
            visited(list): list of nodes that have been marked off

        Returns:
            int,int: nodes that have minimum edge in the graph

        """
        prev_min = sys.maxint #upper bound value
        min_from = -1
        min_to = -1
        for row in matrix:
            for column in matrix[row]:
                if column not in visited and matrix[row][column] < prev_min:
                    prev_min = matrix[row][column]
                    min_from = row
                    min_to = column

        return min_from, min_to


    def compute_adjacency_matrix(self):
        """
        Returns adjacency matrix of graph. Example shown below
          A B C D E
        A 4 3 2 1 2
        B 2 5 6 2 1
        C 3 2 1 3 1
        D 4 4 5 6 3
        E 2 3 2 2 1

        Returns:
            dict: adjaceny matrix
        """
        matrix = {}
        for node_id in self.graph.get_nodes():
            node = self.graph.get_node(node_id)
            row_matrix = {}
            for neighbour_id in self.graph.get_nodes():
                cost = node.get_cost(neighbour_id)
                row_matrix[neighbour_id] = cost
            matrix[node_id] = row_matrix
        return matrix



def main():

    """
    Creates a graph and computes the minimum spanning tree
    and prints the graph

    """

    graph = Graph()

    graph.add_node('A', (2, 3))
    graph.add_node('B', (4, 5))
    graph.add_node('C', (2, 6))
    graph.add_node('D', (3, 5))
    graph.add_node('E', (6, 5))

    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('A', 'D')
    graph.add_edge('A', 'E')
    graph.add_edge('B', 'C')
    graph.add_edge('B', 'D')
    graph.add_edge('B', 'E')
    graph.add_edge('D', 'C')
    graph.add_edge('D', 'E')
    graph.add_edge('C', 'E')

    

    graph.print_graph()

    mst = MST(graph)
    new_graph = mst.compute_mst()
    new_graph.print_graph()



if __name__ == "__main__":
    main()







