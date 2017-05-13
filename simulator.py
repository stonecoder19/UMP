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
	No longer used.
	"""
	pygame.init()
	gameDisplay = pygame.display.set_mode((800,600))

	pygame.display.set_caption('New Window')
	clock = pygame.time.Clock()

	screenColor = (255,255,255)
	droneSprite = pygame.image.load('drone.png')

	return gameDisplay, clock, screenColor, droneSprite

def logic(graph, visited, poly_list, counter, way_lst):
	drone_x,drone_y = drone_coordinates
	if counter<len(way_lst)-1:
		counter+=1
		
		current_node = graph.find_node_from_position(way_lst[counter-1])
		graph.set_node_visited(current_node)
		visited += [graph.get_node(current_node).get_pos()]
		if (len(graph.get_visited_neighbours(current_node))==len(graph.get_node(current_node).get_neighbors())):
			points_list=[]
			for node_id in graph.get_nodes():
				if(graph.get_node(node_id).visited):
					graph.remove_node(node_id)
				else:
					points_list.append(graph.get_node(node_id).get_pos())
			points_list.append(way_lst[counter-1])
			graph = create_graph_from_map(poly_list,points_list)
			mst = MST(graph)
			graph = mst.compute_mst()
			graph.set_node_visited(graph.find_node_from_position(way_lst[counter-1]))
			way_lst = init_mst_way_list(graph,way_lst[counter-1])
			counter = 1
	return graph, visited, poly_list, counter, way_lst

def navigate(graph, drone_coordinates, poly_list, counter, way_lst):
	"""
	No longer used. See logic(graph, visited, poly_list, counter, way_lst)
	"""
	gameDisplay.fill(screenColor)
	draw_graph(gameDisplay, graph)

	drone_x,drone_y = drone_coordinates

	drone(gameDisplay, droneSprite, drone_x,drone_y)
	draw_polys(poly_list, gameDisplay)

	print("Number of Nodes: "+ str(num_nodes))
	print "Counter: {}".format(counter)
	if counter<len(way_lst)-1:
		if is_pos_equal((drone_x,drone_y),way_lst[counter]):
			print "Im here: ({}, {})".format(drone_x,drone_y)
			counter+=1
			print "Counter: {}".format(counter)
			
			current_node = graph.find_node_from_position(way_lst[counter-1])
			graph.set_node_visited(current_node)
			if (len(graph.get_visited_neighbours(current_node))==len(graph.get_node(current_node).get_neighbors())):
				points_list=[]
				for node_id in graph.get_nodes():
					if(graph.get_node(node_id).visited):
						graph.remove_node(node_id)
					else:
						points_list.append(graph.get_node(node_id).get_pos())
				points_list.append(way_lst[counter-1])
				poly_list,points = init_map(800,600,30)
				graph = create_graph_from_map(poly_list,points_list)
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

	crashed = False

	# print("Finding Points..")
	poly_list,points = init_map(800,600,30)

	# print("Creating graph")
	graph = create_graph_from_map(poly_list,points)
	mst = MST(graph)

	# print("Calculating mst")
	graph = mst.compute_mst()

	# print("Calculating waypoint list")
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

	visited = []

	while not crashed:

		graph, visited, poly_list, counter, way_lst = logic(graph, visited, poly_list, counter, way_lst)

		if not counter<len(way_lst)-1:
			crashed = True
			print visited

	quit()



