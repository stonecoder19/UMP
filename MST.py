import math
import sys


class Node:

    def __init__(self, node_id, pos):
        self.id = node_id
        self.pos = pos
        self.visited = False
        self.neighbours = {}

    def add_neighbor(self, neighbour, cost):
        """
        Adds a a node to the list of neighbours

        Args:
            neighbour(string): node_id of neighbour
            cost(float): weight of edge connection node and neighbour
        """
        self.neighbours[neighbour] = cost


    def get_neighbors(self):
        """
        Returns a list of nodes
        """
        return self.neighbours.keys()

    def remove_neighbor(self, node_id):
        """
        Removes a node with the node_id from the current node's neighbours

        Args:
            node_id(string): id of neighbour
        """
        if node_id in self.neighbours:
            self.neighbours.pop(node_id)

    def get_cost(self, node_id):
        """
        Retruns the weigth of an edge between the current node
        and the node with the node_id. If the edge does not exist
        return maxint. If the edge is to the node itself return 0

        Args:
            node_id(string): id of neighbour
        Returns:
            int: weight of edge from current node to neighbour
        """
        if self.id == node_id:
            return 0
        elif node_id not in self.neighbours:
            return sys.maxint
        return self.neighbours[node_id]

    def get_pos(self):
        """ 
        Returns the position of the node
        """
        return self.pos


class Graph:

    def __init__(self):

        #dictionary used to store the nodes in the graph
        self.node_list = {}
        self.num_vertices = 0


    def add_node(self, node_id, pos):
        """
        Adds a node to the graph at a specified position
        Args:
            node_id(string): id of node
            pos(tuple): tuple of (x,y) which are floats

        """
        self.num_vertices = self.num_vertices + 1
        new_node = Node(node_id, pos)
        self.node_list[node_id] = new_node



    def add_edge(self, node1, node2):
        """
        Adds a new edge to the graph betweeen node1 and node2
        It calculates the edge cost then adds each node to the other node's
        list of neighbours and vice versa. It first checks if both nodes are
        already nodes of the graph.

        Args:
            node1(string): id of node1
            node2(string): id of node2

        """
        if node1 in self.node_list and node2 in self.node_list:

            cost = self.calculate_edge_cost(self.node_list[node1].get_pos(),
                                            self.node_list[node2].get_pos())
            self.node_list[node2].add_neighbor(node1, cost)
            self.node_list[node1].add_neighbor(node2, cost)

    def calculate_edge_cost(self, pos1, pos2):
        """
        Returns the euclidean distance between two positions.A position is 
        represented by (x,y). The euclidean distance is calculated using the 
        forumula sqrt((x1-x2)^2 + (y1-y2)^2)
        Args:
            pos1:(tuple): tuple of (x,y) where x and y are floats
            pos2:(tuple): tuple of (x,y) where x and y are floats

        Returns:
            int: cost of edge

        """
        return math.sqrt(math.pow((pos1[0]-pos2[0]), 2) + math.pow((pos1[1]-pos2[1]), 2))
    
    def get_node(self, node_id):
        """
        Returns a node with the specified with node_id. If node with id 
        is not found it reurns None
        Args:
            node_id(string): id of node
        Returns:
            Node: node with id

        """
        if node_id in self.node_list:
            return self.node_list[node_id]
        return None
    
    def set_node_visited(self, node_id):
        """
        Sets the node with the specified node id to visited
        
        Args:
            node_id(string): id of node

        """
        if node_id in self.node_list:
            self.node_list[node_id].visited = True

    def remove_node(self, node_id):
        """
        Removes a node from the graph with the specified node if and also removes it 
        from the list of neighbours for every other node in the graph.

        Args:
            node_id(string): id of node

        """
        if node_id in self.node_list:
            for nodeid in self.get_node(node_id).get_neighbors():
                node = self.get_node(nodeid)
                node.remove_neighbor(node_id)
            self.node_list.pop(node_id)


    def find_node_from_position(self, pos):
        """
        Returns a node with the specified position

        Args:
            pos(tuple): tuple of (x,y) x and y are floats

        Returns:
            string: id of node
        
        """
        for node_id in self.node_list:
            if self.node_list[node_id].get_pos() == pos:
                return node_id
        return None

    def get_visited(self):
        """
        Returns list of nodes that have been marked as visited in the graph
        Returns:
            list: list of nodes that have been visited
        """
        visited = []
        for node_id in self.node_list:
            node = self.get_node(node_id)
            if node.visited:
                visited.append(node_id)
        return visited

    def get_visited_neighbours(self, node_id):
        """
        Get all the neighbours of the node with the specified node id that have been visited
            
        Args:
            node_id(string): id of node

        Returns:
            list: list of neigbuours of node that have been visited

        """
        visited = []
        for nodeid in self.get_node(node_id).get_neighbors():
            node = self.get_node(nodeid)
            if node.visited:
                visited.append(nodeid)
        return visited



    def get_nodes(self):
        """
        Returns a list of all the node ids
        Returns:
            list: list of node ids

        """
        return self.node_list.keys()

    def print_graph(self):
        """
        Prints out the graph in the format
        node1: neighbour1,neighbour2
        node2: neighbpur3, neighbour4
        
        """
        for node_id in self.get_nodes():
            node = self.get_node(node_id)
            print node_id + ":  "
            for i in node.get_neighbors():
                print i +":" + str(node.get_cost(i))  +","
            





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
            if min_from == -1 or min_to == -1:
                continue
            count += 1
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







