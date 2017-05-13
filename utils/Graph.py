import math
from Node import Node

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

    def has_node(self,node_id):
        return self.node_list.has(node_id)

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