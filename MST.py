class Node:

	def __init__(self,node_id,pos):
		self.id = node_id
		self.pos = pos
		self.neighbours={}

	def add_neighbor(self,neighbour,cost):
		self.neighbours[neighbour] = cost

	def get_weight(self,neighbor):
		return self.neighbours[neighbour]

	def get_cost(self,node_id):
		if self.id == node_id:
			return 0
		else if node_id not in self.neighbours.keys
			return 999999999
		else:
			return self.neighbours[neighbour]

	def get_pos:
		return self.pos


class Graph

	def __init__(self):
		self.node_list = {}
		self.num_vertices = 0


	def add_node(self,node_id,pos):
		self.num_vertices = self.num_vertices + 1
		new_node = Node(node_id,pos)
		self.node_list[node] = new_node



	def add_edge(self,node1,node2,cost):
		if node1 not in self.node_list:
			self.add_node(node1)

		if node2 not in self.node_list:
			self.add_node(node2)

		self.node_list[node1].add_neighbor(node2,cost)
		self.node_list[node2].add_neighbor(node1,cost)

	def get_node(self,node_id):
		if node_id in node_list:
			return self.node_list[node_id]
		else:
			return None

	def get_nodes(self):
		return self.node_list.keys()


def min_neighbor(node,edge_list):
	
	prev_min = 999999999999999999
	win_node = None
	for n in edge_list.keys
		if(node!=n):
			if(edge_list[n]<prev_min):
				prev_min = edge_list[n]
				win_node = n
	return win_node


def compute_MST(G):
	new_graph = Graph()

	for n in adjacency_matrix.keys()
		new_graph.add_node(n)

	adjacency_matrix = compute_adjacency_matrix(G)

	for n in adjacency_matrix.keys()
		win_node = min_neighbor(n,adjacency_matrix[n])
		new_graph.add_neighbor(n,win_node)

	return new_graph		


def compute_adjacency_matrix(Graph):
	matrix={}
	for i in Graph.get_nodes
		node = Graph.get_node(j)
		row_matrix={}
		for j in Graph.get_nodes
			cost = node.get_cost(j)
			row_matrix[j] = cost
		matrix[i] = row_matrix
	return matrix 







