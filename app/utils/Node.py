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