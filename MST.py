import math


class Node:

	def __init__(self,node_id,pos):
		self.id = node_id
		self.pos = pos
		self.neighbours={}

	def add_neighbor(self,neighbour,cost):

		self.neighbours[neighbour] = cost

	def get_weight(self,neighbor):
		return self.neighbours[neighbour]

	def get_neighbors(self):
		return self.neighbours.keys()

	def get_cost(self,node_id):
		if self.id == node_id:
			return 0
		elif node_id not in self.neighbours.keys():
			return 999999999
		else:
			return self.neighbours[node_id]

	def get_pos(self):
		return self.pos


class Graph:

	def __init__(self):
		self.node_list = {}
		self.num_vertices = 0


	def add_node(self,node_id,pos):
		#print(node_id)
		self.num_vertices = self.num_vertices + 1
		new_node = Node(node_id,pos)
		self.node_list[node_id] = new_node



	def add_edge(self,node1,node2):
		'''if node1 not in self.node_list.keys():
			self.add_node(node1,(0,0))

		if node2 not in self.node_list.keys():
			self.add_node(node2,(0,0))'''
		
		cost = self.calculate_edge_cost(self.node_list[node1].get_pos(),self.node_list[node2].get_pos())
		#print(cost)
		self.node_list[node2].add_neighbor(node1,cost)
		self.node_list[node1].add_neighbor(node2,cost)

	def calculate_edge_cost(self,pos1,pos2):
		return math.sqrt(math.pow((pos1[0]-pos2[0]),2) + math.pow((pos1[1]-pos2[1]),2))
	
	def get_node(self,node_id):
		if node_id in self.node_list:
			return self.node_list[node_id]
		else:
			return None

	def get_nodes(self):
		return self.node_list.keys()

	def print_graph(self):
		for n in self.get_nodes():
			node  = self.get_node(n)
			print(n + ":  ")
			for i in node.get_neighbors():
				print(i +":" + str(node.get_cost(i))  +",")
			#print("\n")







	










class MST:
	
	def __init__(self,graph):
		self.graph = graph

	def compute_MST(self):
		new_graph = Graph() 
		adjacency_matrix = self.compute_adjacency_matrix()
		print("Computing MST...")
		i=0

		for n in adjacency_matrix.keys():
			new_graph.add_node(n,self.graph.get_node(n).get_pos())
		
		for n in adjacency_matrix.keys():

			if(i<self.graph.num_vertices-1):
				win_node = self.min_neighbor(n,adjacency_matrix[n])
				#new_graph.add_node(win_node,self.graph.get_node(win_node).get_pos())
				row = adjacency_matrix[win_node]
				row.pop(n)
				adjacency_matrix[win_node] = row
				#print(adjacency_matrix)
				#print(n)
				#print(win_node)
				new_graph.add_edge(n,win_node)
				#new_graph.print_graph()
				#print("__________________________")
				i=i+1
		return new_graph

	def min_neighbor(self,node,edge_list):
	
		prev_min = 999999999999999999
		win_node = None
		for n in edge_list.keys():
			if(node!=n):
				if(edge_list[n]<prev_min):
					prev_min = edge_list[n]
					win_node = n
		return win_node

	def compute_adjacency_matrix(self):
		matrix={}
		for i in self.graph.get_nodes():
			#print(i)
			node = self.graph.get_node(i)
			row_matrix={}
			for j in self.graph.get_nodes():
				cost = node.get_cost(j)
				row_matrix[j] = cost
			matrix[i] = row_matrix
		return matrix

def calculate_edge_cost(pos1,pos2):
		return math.sqrt(math.pow((pos1[0]-pos2[0]),2) + math.pow((pos1[1]-pos2[1]),2))


def main():
	#print(calculate_edge_cost((5,2),(3,2)))
	#print(calculate_edge_cost((3,2),(5,2)))

	g = Graph()

	g.add_node('A',(2,3))
	g.add_node('B',(4,5))
	g.add_node('C',(2,6))
	g.add_node('D',(3,5))
	g.add_node('E',(6,5))

	g.add_edge('A','B')
	g.add_edge('A','C')
	g.add_edge('A','D')
	g.add_edge('A','E')

	g.add_edge('B','C')
	g.add_edge('B','D')
	#g.add_edge('B','A')
	g.add_edge('B','E')

	#g.add_edge('D','A')
	g.add_edge('D','C')
	#g.add_edge('D','B')
	g.add_edge('D','E')

	#g.add_edge('C','B')
	#g.add_edge('C','A')
	#g.add_edge('C','D')
	g.add_edge('C','E')

	#g.add_edge('E','B')
	#g.add_edge('E','A')
	#g.add_edge('E','D')
	#g.add_edge('E','C')

	

	g.print_graph()

	mst = MST(g)
	new_graph = mst.compute_MST()
	new_graph.print_graph()



if __name__ == "__main__":


    main()







