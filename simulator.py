import pygame
import random
from MST import *
from utils.util import *
from utils.gfx import *
import math
import sys

def set_up_pygame():
	"""
	Initialize objects necessary for pygame
	"""
	pygame.init()
	gameDisplay = pygame.display.set_mode((800,600))

	pygame.display.set_caption('New Window')
	clock = pygame.time.Clock()

	screenColor = (255,255,255)
	droneSprite = pygame.image.load('drone.png')

	return gameDisplay, clock, screenColor, droneSprite

def navigate(graph, drone_coordinates, poly_list, counter, way_lst):
	gameDisplay.fill(screenColor)
	draw_graph(gameDisplay, graph)

	drone_x,drone_y = drone_coordinates

	drone(gameDisplay, droneSprite, drone_x,drone_y)
	draw_polys(poly_list, gameDisplay)

	#print(graph.num_vertices)
	print("Number of Nodes: "+ str(num_nodes))
	print(counter)
	# print(tot_counter)
	if counter<len(way_lst)-1:
		if is_pos_equal((drone_x,drone_y),way_lst[counter]):
			# tot_counter+=1
			print("Im here")
			print((drone_x,drone_y))
			counter+=1
			print(counter)
			
			current_node = graph.find_node_from_position(way_lst[counter-1])
			graph.set_node_visited(current_node)
			if (len(graph.get_visited_neighbours(current_node))==len(graph.get_node(current_node).get_neighbors())):
				points_list=[]
				last_node = graph.find_node_from_position(way_lst[counter-1])
				old_graph = graph
				for node_id in graph.get_nodes():
					if(graph.get_node(node_id).visited and not graph.get_node(node_id)==last_node):
						graph.remove_node(node_id)
					else:
						points_list.append(graph.get_node(node_id).get_pos())
				points_list.append(way_lst[counter-1])
				poly_list,points = init_map(800,600,30)
				graph = create_graph_from_map(poly_list,points_list)
				
				if(not graph.has_node(last_node)):
					win_node = get_closest_node(graph,last_node)
					path = compute_path(old_graph,last_node,win_node):
					for p in path:
						win_node = None
						for poly in poly_list:
							check_if_edge_interects_poly(poly,Point(points_list[j][0],points_list[j][1]),Point(points_list[k][0],points_list[k][1])))


				
				mst = MST(graph)
				graph = mst.compute_mst()
				graph.set_node_visited(graph.find_node_from_position(way_lst[counter-1]))
				way_lst = init_mst_way_list(graph,way_lst[counter-1])
				counter = 1

	destX = way_lst[counter][0]
	destY = way_lst[counter][1]
	print(destX,destY)

	move_x,move_y = move_to(drone_x,drone_y,destX,destY,0.05)
	drone_x,drone_y = update_pos(drone_x,drone_y,move_x,move_y)
	drone_coordinates = (drone_x, drone_y)

	pygame.display.update()
	clock.tick(60)

	return graph, drone_coordinates, poly_list, counter, way_lst

if __name__ == '__main__':

	gameDisplay, clock, screenColor, droneSprite = set_up_pygame()
	crashed = False

	print("Finding Points..")
	poly_list,points = init_map(800,600,30)

	print("Creating graph")
	graph = create_graph_from_map(poly_list,points)
	mst = MST(graph)

	print("Calculating mst")
	graph = mst.compute_mst()

	print("Calculating waypoint list")
	way_lst = init_mst_way_list(graph,(-1,-1))
	graph.set_node_visited(graph.find_node_from_position(way_lst[0]))
	num_nodes = len(graph.get_nodes())

	#first waypoint on graph
	drone_x=way_lst[0][0]
	drone_y=way_lst[0][1]
	drone_coordinates = (drone_x, drone_y)

	#final waypoint on the graph
	finalX = way_lst[len(way_lst)-1][0]
	finalY = way_lst[len(way_lst)-1][1]


	counter = 1

	# stop = False
	# tot_counter = 1

	while not crashed:

		graph, drone_coordinates, poly_list, counter, way_lst = navigate(graph, drone_coordinates, poly_list, counter, way_lst)

		print "Counter {}".format(counter)

		if(pygame.QUIT in [event.type for event in pygame.event.get()]):
			print "You quit"
			crashed = True

	pygame.quit()
	quit()



