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
		
		visited = []


		for n in adjacency_matrix.keys():


			if(i<self.graph.num_vertices-1):

				win_node = self.min_neighbor(n,adjacency_matrix[n])
				#new_graph.add_node(win_node,self.graph.get_node(win_node).get_pos())
				row = adjacency_matrix[win_node]
				row.pop(n)
				adjacency_matrix[win_node] = row
				print(adjacency_matrix)
				#print(n)
				#print(win_node)
				new_graph.add_edge(n,win_node)
				#new_graph.print_graph()
				#print("__________________________")
				i=i+1
		print(i)
		return new_graph

	def computeMST(self):
		new_graph = Graph()
		visited = []
		adjacency_matrix={}
		
		for node in self.graph.get_nodes():
			new_graph.add_node(node,self.graph.get_node(node).get_pos())
		
		current_node = self.graph.get_nodes()[0]
		visited+=[current_node]
		for i in range(1,len(self.graph.get_nodes())):
			if(len(visited)<len(self.graph.get_nodes())):
				neighbours = self.graph.get_node(current_node).get_neighbors()
				row={}
				for j in neighbours:
					row[j] = self.graph.get_node(current_node).get_cost(j)
				adjacency_matrix[current_node] = row
				win_from,win_to = self.select_min_edge(adjacency_matrix,visited)
				new_graph.add_edge(win_from,win_to)
				current_node = win_to
				visited += [current_node]
		return new_graph

	
	def select_min_edge(self,matrix,visited):
		prev_min = 999999999999999999
		for row in matrix.keys():
			for column in matrix[row].keys():
				if column not in visited and matrix[row][column]<prev_min:
					prev_min = matrix[row][column]
					win_from = row
					win_to = column
		return win_from,win_to





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
	new_graph = mst.computeMST()
	new_graph.print_graph()



if __name__ == "__main__":


    main()







