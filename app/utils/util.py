import sys, math
from Polygon import Polygon
from Point import Point
from Graph import Graph
from Rect import Rect
from MST import *
import time
import math
import sys
import copy
import random
from gfx import *
import pygame


def init_waypoint_list(graph):
	lst = []
	for n in graph.get_nodes():
		node = graph.get_node(n)
		lst.append(node.get_pos())
	return lst

def init_radius_points(width,height,radius):
	pos_lst=[]
	num_rows = height/(radius*2)
	num_cols = width/(radius*2)
	for i in range(0,num_rows):
		for j in range(0,num_cols):
			pos_lst.append(((j*(radius*2)+(radius)),(i*(radius*2))+(radius)))

	fringe_nodes = []
	space_left_width = width - (num_rows * radius*2)
	space_left_height = height - (num_cols * radius * 2)
	pos_x = (num_cols * radius * 2) + (space_left_width/2)
	pos_y = (num_rows * radius * 2) + (space_left_height/2)

	for k in range(0,num_cols-1):
		pos_lst.append((k*(radius*2)+radius,pos_y))

	for l in range(0,num_rows-1):
		pos_lst.append((pos_x,l*(radius*2)+radius))

	pos_lst.append(((num_cols*radius*2)+(space_left_width/2),(num_rows*radius*2)+(space_left_height/2)))


	return pos_lst

def remove_points(square_list,points_list):
	lst=[]
	for p in points_list:
		point = Point(p)
		for square in square_list:
			if is_in_bounds(square,point):
				return
		lst.append(point)
	return lst

def create_rect_from_poly(polygon):
	pos = Point(polygon.get_far_left(),polygon.get_far_top())
	rect = Rect(pos,polygon.get_width(),polygon.get_height())
	return rect

def is_in_bounds(rect,pos):
	if((pos.x>=rect.top_left.x) and (pos.x<=rect.top_right.x) and (pos.y <= rect.bottom_right.y) and (pos.y>=rect.top_left.y)):
		return True
	else:
		return False

def is_in_poly(polygon,point):
	ref_point = Point(0,0)
	intersect_count = 0
	for i in range(0,len(polygon.vertices)):
		first = polygon.vertices[i]
		if(i==len(polygon.vertices)-1):
			second = polygon.vertices[0]
		else:
			second = polygon.vertices[i+1]
		if (check_intersect(ref_point,point,first,second)):
			intersect_count+=1
	if (intersect_count%2==0):
		return False
	else:
		return True

def init_mst_way_list(mst_graph,start_pos):
	current_node = mst_graph.find_node_from_position(start_pos)
	if(current_node==None):
		current_node = mst_graph.get_nodes()[0]
	prev_node = current_node
	visited=[]
	way_lst=[]
	way_lst.append(mst_graph.get_node(current_node).get_pos())
	visited.append(current_node)

	while(len(visited)<len(mst_graph.get_nodes())):
		next_node = get_closest_unvisited_neighbour(mst_graph,visited,current_node)
		if(next_node==None):
			next_node = get_closest_unvisited_node(mst_graph,visited,current_node)
			if(next_node not in visited):
				visited.append(next_node)
				path = compute_path(mst_graph,current_node,next_node)
				
				if path == None:
						return None
				for n in path:
					
					if n not in visited:
						visited.append(n)
					way_lst.append(mst_graph.get_node(n).get_pos())
		else:
			if(next_node not in visited):
				visited.append(next_node)
			way_lst.append(mst_graph.get_node(next_node).get_pos())
		
		#print(len(visited))
		#print(current_node)
		current_node = next_node
	return way_lst

def calc_euclidean_distance(pos1,pos2):
	return math.sqrt(math.pow((pos1[0]-pos2[0]),2) + math.pow((pos1[1]-pos2[1]),2))

def get_closest_unvisited_neighbour(graph,visited,node):
	min_node=None
	prev_min = sys.maxint
	alt_lst=[]
	for node_id in graph.get_node(node).get_neighbors():
		if(node_id not in visited):
			if(graph.get_node(node).get_cost(node_id)<prev_min):
				prev_min = graph.get_node(node).get_cost(node_id)
				min_node = node_id
				alt_lst=[]
			elif(graph.get_node(node).get_cost(node_id)==prev_min):
				alt_lst.append(node_id)
	if(len(alt_lst)>0):
		alt_lst.append(min_node)
		prev_min=sys.maxint
		min_el=None
		for el in alt_lst:
			if(count_unvisited_neighbours(graph,el,visited)<prev_min):
				prev_min = count_unvisited_neighbours(graph,el,visited)
				min_el = el
		return min_el
	else:
		return min_node

def count_unvisited_neighbours(graph,node,visited):
	unvisited=0
	for neighbor_id in graph.get_node(node).get_neighbors():
		if neighbor_id not in visited:
			unvisited+=1
	return unvisited



def compute_path_cost(graph,path):
	total_cost = 0
	for i in range(0,len(path)-1):
		total_cost+=calc_euclidean_distance(graph.get_node(path[i]).get_pos(),graph.get_node(path[i+1]).get_pos())
	return total_cost




def shortest_path_cost_unvisited(graph,pos,visited):
	prev_min = sys.maxint
	min_path_node_pair = None
	start_node = graph.find_node_from_position(pos)
	for goal_node in graph.get_nodes():
		if(goal_node not in visited and not goal_node==start_node):
			path = compute_path(graph,start_node,goal_node)
			path_cost = compute_path_cost(graph,path)
			if(path_cost < prev_min):
				prev_min = path_cost
				min_path_node_pair = (path,goal_node)
	print str(min_path_node_pair)
	return min_path_node_pair[0],min_path_node_pair[1]



def get_closest_unvisited_node(graph,visited,node):
	min_node = None
	prev_min = sys.maxint
	for i in range(0,len(graph.get_nodes())):
		n = graph.get_nodes()[i]
		if(n not in visited):
			dist = calc_euclidean_distance(graph.get_node(n).get_pos(),graph.get_node(node).get_pos())
			if(dist<prev_min):
				prev_min = dist
				min_node = n
	return min_node

def get_closest_node(graph,pos):
	min_node = None
	prev_min = sys.maxint
	for node_id in graph.get_nodes():
		node = graph.get_node(node_id)
		dist = calc_euclidean_distance(pos,node.get_pos())
		if(dist<prev_min):
			prev_min = dist
			min_node = node_id
	return min_node

#compute shortest path from start goal to goal node using A*
def compute_path(graph,start_node,goal_node):
	closed = []
	openSet=[]
	openSet.append(start_node)
	cameFrom = {}
	
	gScore = {}
	for node in graph.get_nodes():
		gScore[node] = sys.maxint

	gScore[start_node] = 0
	
	fScore = {}
	for n in graph.get_nodes():
		fScore[n] = sys.maxint
	
	fScore[start_node] = calc_euclidean_distance(graph.get_node(start_node).get_pos(),graph.get_node(goal_node).get_pos())

	while len(openSet) > 0:
		current_node = lowest_fscore(openSet,fScore)
		if current_node == goal_node:
			return reconstruct_path(cameFrom,current_node)
		
		openSet = list(filter(lambda x: x!= current_node, openSet))
		closed.append(current_node)
		for neighbor in graph.get_node(current_node).get_neighbors():
			if neighbor in closed:
				continue
			temp_gScore = gScore[current_node] + graph.get_node(current_node).get_cost(neighbor)
			if neighbor not in openSet:
				openSet.append(neighbor)
			elif temp_gScore >= gScore[neighbor]:
				continue

			cameFrom[neighbor] = current_node
			gScore[neighbor] = temp_gScore
			fScore[neighbor] = gScore[neighbor] + calc_euclidean_distance(graph.get_node(neighbor).get_pos(),graph.get_node(goal_node).get_pos())
	return None

def lowest_fscore(openSet,fScore):
	prev_min = sys.maxint
	min_node = None
	for node in openSet:
		if(fScore[node]<prev_min):
			prev_min = fScore[node]
			min_node = node
	return min_node

def reconstruct_path(cameFrom,current):
	total_path = [current]
	while current in cameFrom.keys():
		current = cameFrom[current]
		total_path.append(current)
	total_path.reverse()
	return total_path

#checks if point2 is on the line segment between point1 and point3
def onLine(point1,point2,point3):
	if(point2.x <= max(point1.x,point3.x) and point2.x >= min(point1.x,point3.x) and point2.y <= max(point1.y,point3.y) and point2.y >=min(point1.y,point3.y)):
		return True

	return False

def orientation(point1,point2,point3):

	val = (point2.y-point1.y) * (point3.x - point2.x) - (point2.x-point1.x) * (point3.y-point2.y)
	if(val==0):
		return 0

	if(val >0):
		return 1
	else:
		return -1

#checks if line segment point1point2 intersects with line segment point3point4
def check_intersect(point1,point2,point3,point4):

	o1 = orientation(point1,point2,point3)
	o2 = orientation(point1,point2,point4)
	o3 = orientation(point3,point4,point1)
	o4 = orientation(point3,point4,point2)

	if(o1!= o2 and o3 != o4):
		return True

	if(o1 == 0 and onLine(point1,point3,point2)):
		return True

	if(o2 == 0 and onLine(point1,point4,point2)):
		return True

	if(o3==0 and onLine(point3,point1,point4)):
		return True

	if(o4 == 0 and onLine(point3,point2,point4)):
		return True
	
	return False


def init_polys():
	poly_list=[]
	
	polygon1 = Polygon("red")
	polygon1.add_vert(Point(40,50))
	polygon1.add_vert(Point(150,50))
	polygon1.add_vert(Point(20,150))
	polygon1.add_vert(Point(40,5))

	polygon2 = Polygon("green")
	polygon2.add_vert(Point(200,250))
	polygon2.add_vert(Point(220,270))
	polygon2.add_vert(Point(260,290))
	polygon2.add_vert(Point(190,200))

	polygon3 = Polygon("green")
	polygon3.add_vert(Point(550,250))
	polygon3.add_vert(Point(570,270))
	polygon3.add_vert(Point(610,290))
	polygon3.add_vert(Point(540,200))

	polygon4 = Polygon("green")
	polygon4.add_vert(Point(450,400))
	polygon4.add_vert(Point(450,500))
	polygon4.add_vert(Point(550,500))
	polygon4.add_vert(Point(550,400))

	polygon5 = Polygon("green")
	polygon5.add_vert(Point(250,400))
	polygon5.add_vert(Point(250,500))
	polygon5.add_vert(Point(350,500))
	polygon5.add_vert(Point(350,400))

	polygon6 = Polygon("green")
	polygon6.add_vert(Point(350,500))
	polygon6.add_vert(Point(350,600))
	polygon6.add_vert(Point(450,600))
	polygon6.add_vert(Point(450,500))


	polygon7 = Polygon("green")
	polygon7.add_vert(Point(350,100))
	polygon7.add_vert(Point(350,200))
	polygon7.add_vert(Point(450,200))
	polygon7.add_vert(Point(450,100))
	'''polygon3 = Polygon("blue")
	polygon1.add_vert(Point(40,50))
	polygon1.add_vert(Point(40,50))
	polygon1.add_vert(Point(40,50))
	polygon1.add_vert(Point(40,50))'''

	poly_list.append(polygon1)
	poly_list.append(polygon2)
	poly_list.append(polygon3)
	poly_list.append(polygon4)
	poly_list.append(polygon5)
	poly_list.append(polygon6)
	poly_list.append(polygon7)

	return poly_list

def init_map(width,height,drone_radius,poly_list):
	points_list = init_radius_points(width,height,drone_radius)
	new_points_list=[]
	for p in points_list:
		inBounds = False
		for poly in poly_list:
			#rect = create_rect_from_poly(poly)
			if (is_in_poly(poly,Point(p[0],p[1]))):
				inBounds=True
				break
		if(inBounds==False):
			new_points_list.append(p)

	return new_points_list

def init_map_with_border(width,height,drone_radius,poly_list,border):
	points_list = init_radius_points(width,height,drone_radius)
	new_points_list=[]
	for p in points_list:
		if(is_in_poly(border,Point(p[0],p[1]))):
			inBounds = False
			for poly in poly_list:
				#rect = create_rect_from_poly(poly)
				if (is_in_poly(poly,Point(p[0],p[1]))):
					inBounds=True
					break
			if(inBounds==False):
				new_points_list.append(p)

	return new_points_list

def check_if_edge_interects_poly_rect(polygon,point1,point2):
	rect = create_rect_from_poly(polygon)

	if(check_intersect(point1,point2,rect.top_left,rect.top_right)):
		return True
	
	if(check_intersect(point1,point2,rect.top_left,rect.bottom_left)):
		return True
	
	if(check_intersect(point1,point2,rect.bottom_left,rect.bottom_right)):
		return True
	
	if(check_intersect(point1,point2,rect.top_right,rect.bottom_right)):
		return True

	return False

def check_if_edge_interects_poly(polygon,point1,point2):
	for i in range(0,len(polygon.vertices)):
		first = polygon.vertices[i]
		if(i==len(polygon.vertices)-1):
			second = polygon.vertices[0]
		else:
			second = polygon.vertices[i+1]
		if (check_intersect(point1,point2,first,second)):
			return True
	return False

def create_graph_from_map(border_poly,poly_list,points_list):
	
	graph = Graph()
	
	for i in range(0,len(points_list)):
		graph.add_node(str(i),points_list[i])

	tot_count = len(points_list) * len(points_list)
	count = 0
	for j in range(0,len(points_list)):
		for k in range (0, len(points_list)):
			count+=1
			if(k>j):
				if(j!=k):
					isIntersect = False
					for poly in poly_list:
						if(check_if_edge_interects_poly(poly,Point(points_list[j][0],points_list[j][1]),Point(points_list[k][0],points_list[k][1]))):
							isIntersect = True
							break

					if(isIntersect==False and not check_if_edge_interects_poly(border_poly,Point(points_list[j][0],points_list[j][1]),Point(points_list[k][0],points_list[k][1]))):
						graph.add_edge(str(j),str(k))
					

	for node_id in graph.get_nodes():
		node = graph.get_node(node_id)
		if(len(node.get_neighbors())<=0):
			graph.remove_node(node_id)
	

	return graph


def create_poly_from_coords(coords):
	polygon = Polygon("poly")
	for coord in coords:
		polygon.add_vert(Point(coord[0],coord[1]))
	return polygon


def find_latlng_by_start_point_bearing(startloc,distance,bearing):
	start_lat = math.radians(startloc[0])
	start_lng = math.radians(startloc[1])
	R = 6371000.00
	lat2 = math.asin(math.sin(start_lat) * math.cos(distance/R) + math.cos(start_lat) * math.sin(distance/R) * math.cos(math.radians(bearing)))
	lng2 = start_lng + math.atan2(math.sin(math.radians(bearing))	 * math.sin(distance/R) * math.cos(start_lat),math.cos(distance/R) - math.sin(start_lat) * math.sin(lat2))

	return (math.degrees(lat2),math.degrees(lng2))

def calculate_haversine_distance(loc1,loc2):
	lat1 = loc1[0]
	lng1 = loc1[1]
	lat2 = loc2[0]
	lng2 = loc2[1]
	R = 6371000
	lat1_rad = math.radians(lat1)
	lat2_rad = math.radians(lat2)
	delta_lat_rad = math.radians(lat2-lat1)
	delta_lng_rad = math.radians(lng2 - lng1)

	a = math.sin(delta_lat_rad/2) * math.sin(delta_lat_rad/2) + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng_rad/2) * math.sin(delta_lng_rad/2)

	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

	distance = R * c

	return distance #in meters


def geo_to_int(geo_coord):
	s = '%.10f' % geo_coord
	s_split = s.split('.')
	new_s = s_split[0]+s_split[1]
	return int(new_s)

def int_to_geo(coord):
	coord_s = str(int(coord))
	coord_f = float(str(coord_s[:-10])+'.'+str(coord_s[-10:]))
	return coord_f


def convert_180_to_360(geo_coord):
	lat = geo_to_int(geo_coord[0])
	lng = geo_to_int(geo_coord[1])
	x = 1800000000000+lng
	y = 1800000000000-lat
	return (x,y) 

def convert_coord_to_geo(euc_coord):
	x = euc_coord[0]
	y = euc_coord[1]
	lng_i = x - 1800000000000
	lat_i = 1800000000000 - y
	return (int_to_geo(lat_i),int_to_geo(lng_i))


def polygon_area(polygon):
	area = 0
	num_verts = len(polygon.vertices)
	j = num_verts-1
	for i in range(0,num_verts):
		area += ( polygon.vertices[j].x+polygon.vertices[i].x) * (polygon.vertices[j].y-polygon.vertices[i].y)
		j = i
	return area/2


def convert_json_to_polys(outerbounds,innerbounds1,innerbounds2):
    outer_coord_list = []
    for coord in outerbounds:
    	lat = coord['lat']
    	lon = coord['lng']
    	outer_coord_list.append((lon,lat))
	
	incoord1_list = []
	
	for incoord1 in innerbounds1:
		lat1 = incoord1['lat']
		lon1 = incoord1['lng']
		incoord1_list.append((lon1,lat1))

	incoord2_list=[]
	for incoord2 in innerbounds2:
		lat2 = incoord2['lat']
		lon2 = incoord2['lng']
		incoord2_list.append((lon2,lat2))
	inner_poly_coords = []
	inner_poly_coords.append(incoord1_list)
	inner_poly_coords.append(incoord2_list)
    
    return outer_coord_list,inner_poly_coords




def convert_coords_geo_to_euclidean(outer_coord_list,inner_poly_coords,radius_dist):

	outer_poly = create_poly_from_coords(outer_coord_list)
	max_y_coord = outer_poly.get_far_bottom()
	min_y_coord = outer_poly.get_far_top()
	max_x_coord = outer_poly.get_far_right()
	min_x_coord = outer_poly.get_far_left()

	print("Min X coord: " + str(min_x_coord))
	print("Min Y coord: " + str(min_y_coord))
	print("Max X coord: " + str(max_x_coord))
	print("Max Y coord: " + str(max_y_coord))



	outer_height = calculate_haversine_distance((max_y_coord,min_x_coord),(min_y_coord,min_x_coord))
	outer_width = calculate_haversine_distance((max_y_coord,min_x_coord),(max_y_coord,max_x_coord))
	print(outer_height)
	print(outer_width)

	geo_rect = Rect(Point(min_x_coord,max_y_coord),outer_width,outer_height)
	
	max_width = 0
	if(outer_width > outer_height):
		max_width = 800
		max_height = int((outer_height/outer_width) * 800)
	else:
		max_height = 800
		max_width = int((outer_width/outer_height)* 800)

	new_outer_coord_list = []
	for coord in outer_coord_list:
		x = int((calculate_haversine_distance((max_y_coord,min_x_coord),(max_y_coord,coord[0])) / outer_width) * max_width)
		y = int((calculate_haversine_distance((max_y_coord,min_x_coord),(coord[1],min_x_coord)) / outer_height) * max_height)
		new_outer_coord_list.append((x,y))
	
	euc_poly = create_poly_from_coords(new_outer_coord_list)
	euc_rect = create_rect_from_poly(euc_poly)



	new_inner_polys=[]
	for inner_coord_lst in inner_poly_coords:
		inner_poly = create_poly_from_coords(inner_coord_lst)
		#poly_rect = create_rect_from_poly(inner_poly)
		new_inner_poly_coord_lst = []
		for coord in inner_coord_lst:
			x = int((calculate_haversine_distance((max_y_coord,min_x_coord),(max_y_coord,coord[0])) / outer_width) * max_width)
			y = int((calculate_haversine_distance((max_y_coord,min_x_coord),(coord[1],min_x_coord)) / outer_height) * max_height)
			new_inner_poly_coord_lst.append((x,y))
		new_inner_polys.append(new_inner_poly_coord_lst)

	radius_euc = int((radius_dist / outer_width) * max_width)
	return new_outer_coord_list,new_inner_polys,geo_rect,euc_rect,radius_euc



def convert_euclidean_path_to_geo(path,euc_rect,geo_rect,radius):
	
	screen_width = euc_rect.width
	screen_height = euc_rect.height
	geo_path = []
	for waypoint in path:
		x = waypoint[0]
		y = waypoint[1]
		lat = find_latlng_by_start_point_bearing((geo_rect.top_left.y,geo_rect.top_left.x),((float(y)/screen_height) * geo_rect.height),180.0)[0]  
		lng = find_latlng_by_start_point_bearing((geo_rect.top_left.y,geo_rect.top_left.x),((float(x)/screen_width) * geo_rect.width),90.0)[1]  
		geo_path.append((lat,lng))
	
	#sense_range_lat = geo_rect.top_left.y
	#sense_range_lng = find_latlng_by_start_point_bearing((geo_rect.top_left.y,geo_rect.top_left.x),((float(radius)/screen_width) * geo_rect.width),90.0)[1]  

	#origin_lat = geo_rect.top_left.y
	#origin_lng = geo_rect.top_left.x

	return geo_path





	
def get_final_path(outerbounds,innerbounds1,innerbounds2,radius):
	# print("Finding Points..")
	#poly_list = init_polys()
	#points = init_map(800,600,30,poly_list)
	#outer_coord_list,inner_poly_coords = convert_json_to_polys(outerbounds,innerbounds1,innerbounds2)
	outer_coord_list,inner_poly_coords = convert_json_to_polys(outerbounds,innerbounds1,innerbounds2)
	print(outer_coord_list)
	
	new_outer_coord_list, new_inner_polys,geo_rect,border_rect,radius_euc = convert_coords_geo_to_euclidean(outer_coord_list,inner_poly_coords,radius)
	print(new_outer_coord_list)
	border_poly = create_poly_from_coords(new_outer_coord_list)
	print(border_poly.get_vert_list())
	poly_list = []
	for poly in new_inner_polys:
		poly_list.append(create_poly_from_coords(poly))

	
	points = init_map_with_border(int(border_rect.width),int(border_rect.height),radius_euc,poly_list,border_poly)


	# print("Creating graph")
	graph = create_graph_from_map(border_poly,poly_list,points)
	connected_graph = copy.deepcopy(graph)
	mst = MST(graph)

	# print("Calculating mst")
	graph = mst.compute_mst()

	# print("Calculating waypoint list")
	way_lst = init_mst_way_list(graph,(-1,-1))
	graph.set_node_visited(graph.find_node_from_position(way_lst[0]))
	num_nodes = len(graph.get_nodes())

	counter = 1
	visited = []
	print("Computing..")
	visited = calc_path(graph,connected_graph,poly_list,counter,way_lst,border_poly)
	#geo_path,radius,origin = convert_euclidean_path_to_geo(visited,border_rect,geo_rect,radius)
	geo_path = convert_euclidean_path_to_geo(visited,border_rect,geo_rect,radius)
	return geo_path


def calc_path(graph,connected_graph,poly_list, counter, way_lst,border_poly):
	visited=[]
	visited.append(way_lst[0])
	while (counter<len(way_lst)-1):
		counter+=1
		
		current_node = graph.find_node_from_position(way_lst[counter-1])
		last_pos = way_lst[counter-1]
		graph.set_node_visited(current_node)
		visited += [graph.get_node(current_node).get_pos()]
		if (len(graph.get_visited_neighbours(current_node))==len(graph.get_node(current_node).get_neighbors())):
			points_list=[]
			last_node = current_node
			old_graph = copy.deepcopy(graph)
			removed = []
			unvisited = []
			for node_id in graph.get_nodes():
				if(graph.get_node(node_id).visited):
					graph.remove_node(node_id)
					removed.append(node_id)
				else:
					unvisited.append(node_id)
					points_list.append(graph.get_node(node_id).get_pos())
			
			points_list.append(way_lst[counter-1])
			unvisited.append(current_node)

			for node_id in connected_graph.get_nodes():
				if connected_graph.get_node(node_id).get_pos() not in points_list:
					connected_graph.remove_node(node_id)

			graph = copy.deepcopy(connected_graph)
			
			


			orphaned=[]
			for node_id in unvisited:
				if graph.find_node_from_position(old_graph.get_node(node_id).get_pos())==None:
					orphaned.append(node_id)

			if(len(orphaned)>0):
				print("Edge Case")
				for orphan in orphaned:
						path,closest_node = shortest_path_cost_unvisited(old_graph,old_graph.get_node(orphan).get_pos(),removed)
						closest_pos = old_graph.get_node(closest_node).get_pos()
						count = 0
						for p in path:
							is_intersect = False
							for poly in poly_list:
								pos = old_graph.get_node(p).get_pos()
								is_intersect = check_if_edge_interects_poly(poly,Point(pos[0],pos[1]),Point(closest_pos[0],closest_pos[1])) or check_if_edge_interects_poly(border_poly,Point(pos[0],pos[1]),Point(closest_pos[0],closest_pos[1]))
								if is_intersect == True:
									break
							
							if count > 0:
								position = old_graph.get_node(p).get_pos()

								if position not in points_list:
									points_list.append(position)
								
							if is_intersect==False:
								break
							
							count+=1

				for node_id in connected_graph.get_nodes():
					if connected_graph.get_node(node_id).get_pos() not in points_list:
						connected_graph.remove_node(node_id)
				graph = copy.deepcopy(connected_graph)
				

			
			mst = MST(graph)
			#print("Computing tree")
			graph = mst.compute_mst()
			#print("Done Computing tree")
			graph.set_node_visited(graph.find_node_from_position(way_lst[counter-1]))
			way_lst = init_mst_way_list(graph,way_lst[counter-1])

			#disjoint graph case
			if(way_lst == None):
				print("Disjoint")
				count =0
				if(len(removed) > 0):
					while(count<(len(removed))):
						print("Removed " + str(len(removed)))
						print("Count " + str(count))
						node_id = removed[count]
						points_list.append(old_graph.get_node(node_id).get_pos())

						for node_id in connected_graph.get_nodes():
							if connected_graph.get_node(node_id).get_pos() not in points_list:
								connected_graph.remove_node(node_id)
						graph = copy.deepcopy(connected_graph)
						mst = MST(graph)
						graph = mst.compute_mst()
						count+=1
						graph.set_node_visited(graph.find_node_from_position(last_pos))
						way_lst = init_mst_way_list(graph,last_pos)
						if not way_lst == None:
							break
					

					


					# Random sampling
					



			counter = 1
	final_node = graph.find_node_from_position(way_lst[counter])
	visited.append(graph.get_node(final_node).get_pos())
	return visited


def reconnect_nodes_with_graph(graph,old_graph,revived,poly_list,border_poly):
	for node_id in revived:
		
		pos1 = old_graph.get_node(node_id).get_pos()
		graph.add_node(node_id,pos1)
		for possible_neighbour in graph.get_nodes():
			pos2 = graph.get_node(possible_neighbour).get_pos()
			if(not possible_neighbour == node_id):
				isIntersect = False
				for poly in poly_list:
					if(check_if_edge_interects_poly(poly,Point(pos1[0],pos1[1]),Point(pos2[0],pos2[1]))):
						isIntersect = True
						break

				if(isIntersect==False and not check_if_edge_interects_poly(border_poly,Point(pos1[0],pos1[1]),Point(pos2[0],pos2[1]))):
					graph.add_edge(node_id,possible_neighbour)
	return graph


def test_line_segment_intersect_circle(point1,point2,circle_center,radius):
	return ((math.fabs((point2.x-point1.x)*circle_center.x + (point1.y-point2.y)*circle_center.y + (point1.x-point2.x)*point1.y + point2.x*(point2.y-point1.y)))/(math.sqrt(math.pow((point2.x-point1.x),2)+math.pow((point1.y-point2.y),2)))) < radius				


def points_of_segment_intersect_circle(point1,point2,circle_center,radius):
	lab = calc_euclidean_distance((point1.x,point1.y),(point2.x,point2.y))

	dx = (point2.x-point1.x)/lab
	dy = (point2.y-point1.y)/lab

	t = dx * (circle_center.x-point1.x) + dy * (circle_center.y-point1.y)

	ex = t * dx + ax
	ey = t * dy + ay

	lec = calc_euclidean_distance((ex,ey),(circle_center.x,circle_center.y))

	if(lec < radius):
		dt = math.sqrt(math.pow(radius,2)-math.pow(lec,2))

		fx = (t-dt) * dx + point1.x
		fy = (t-dt) * dy + point1.y

		gx = (t+dt) * dx + point1.x
		gy = (t+dt) * dy + point1.y

		return (Point(fx,fy),Point(gx,gy))
	return None


def init_poly_list(poly_sides,num_poly):
	# poly_list = []
	# for i in range(0,num_poly):
	# 	vert_list=[]
	# 	for j in range(0,poly_sides):
	# 		vert_list.append((random.randint(0,800),random.randint(0,600)))
	# 	poly_list.append(vert_list)
	# return poly_list
	return [[(random.randint(0,800),random.randint(0,600)) for j in range(0, poly_sides)] for i in range(0, num_poly)]

def drone(gameDisplay, droneSprite, x,y):
	gameDisplay.blit(droneSprite,(x-30,y-30))

def update_pos(drone_x,drone_y,speedX,speedY):
	drone_x += speedX
	drone_y += speedY
	return drone_x,drone_y

def move_to(current_x,current_y,desiredX,desiredY,kp):
	move_x = kp*(desiredX-current_x)
	move_y = kp*(desiredY-current_y)
	return move_x,move_y

def is_pos_equal(pos1,pos2):
	return math.fabs((pos1[0]-pos2[0]))<=1 and math.fabs((pos1[1]-pos2[1]))<=1




#if __name__ == "__main__":
	
'''pygame.init()
screen = pygame.display.set_mode((800,800))	
done = False
points_list = init_radius_points(800,800,30)
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	screen.fill((255,255,255))
	draw_waypoints(screen,points_list)
	pygame.display.flip()'''
 