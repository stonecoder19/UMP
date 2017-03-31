class Node:

	def __init__(self,node_id,pos):
		self.id = node_id
		self.pos = pos
		self.neighbours={}

	def add_neighbor(self,neighbour,cost):
		self.neighbours[neighbour] = cost

	def get_weight(self,neighbor):
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


	def compute_MST():
		pass






