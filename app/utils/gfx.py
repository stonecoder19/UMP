import pygame

def draw_waypoint(gameDisplay, node):
	if (node.visited==True):
		color = (0,0,255)
	else:
		color = (255,0,0)
	pygame.draw.circle(gameDisplay,color,node.get_pos(),2)

def draw_waypoints(gameDisplay,points_list):
	for point in points_list:
		pygame.draw.circle(gameDisplay,(0,0,255),point,2)

def draw_polys(poly_list, gameDisplay):
	for polygon in poly_list:
		draw_polygon(gameDisplay, polygon)

def draw_polygon(gameDisplay, polygon):
	#print(polygon.get_vert_list())
	pygame.draw.polygon(gameDisplay,(255,0,0),polygon.get_vert_list())

# def draw_map(wapoint_list,polygon_list):
# 	for point in wapoint_list:
# 		draw_waypoint(point)

# 	for polygon in polygon_list:
# 		draw_polygon(polygon)

def draw_line(gameDisplay, point1,point2):
	pygame.draw.line(gameDisplay, (0,255,0), [point1[0], point1[1]], [point2[0],point2[1]], 1)

def draw_graph(gameDisplay, graph):

	for n in graph.get_nodes():
		node = graph.get_node(n)
		draw_waypoint(gameDisplay, node)
		for neighbor_id in node.get_neighbors():
			neighbour_node = graph.get_node(neighbor_id)
			draw_line(gameDisplay, node.get_pos(),neighbour_node.get_pos())

def create_graph():
	g = Graph()

	g.add_node('A',(300,500))
	g.add_node('B',(150,400))
	
	g.add_node('D',(600,100))
	g.add_node('E',(400,300))
	g.add_node('C',(400,100))

	g.add_edge('A','B')
	g.add_edge('A','C')
	g.add_edge('A','D')
	g.add_edge('A','E')

	g.add_edge('B','C')
	g.add_edge('B','D')
	g.add_edge('B','A')
	g.add_edge('B','E')

	g.add_edge('D','A')
	g.add_edge('D','C')
	g.add_edge('D','B')
	g.add_edge('D','E')

	g.add_edge('C','B')
	g.add_edge('C','A')
	g.add_edge('C','D')
	g.add_edge('C','E')

	g.add_edge('E','B')
	g.add_edge('E','A')
	g.add_edge('E','D')
	g.add_edge('E','C')

	return g