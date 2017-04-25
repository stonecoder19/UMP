import pygame
import random
from MST import *
import math
import sys






pygame.init()
gameDisplay = pygame.display.set_mode((800,600))

pygame.display.set_caption('New Window')
clock = pygame.time.Clock()

screenColor = (255,255,255)
droneSprite = pygame.image.load('drone.png')
crashed = False

def init_waypoint_list(graph):
	lst = []
	for n in graph.get_nodes():
		node = graph.get_node(n)
		lst.append(node.get_pos())
	return lst



def init_radius_points(width,height,radius):
	pos_lst=[]
	num_rows = width/(radius*2)
	num_cols = height/(radius*2)
	for i in range(0,num_rows):
		for j in range(0,num_cols):
			pos_lst.append(((i*(radius*2)+(radius)),(j*(radius*2))+(radius)))
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


class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Rect:
	def __init__(self,pos,width,height):
		self.top_left = pos
		self.bottom_left = Point(pos.x,pos.y+height)
		self.top_right = Point(pos.x+width,self.top_left.y)
		self.bottom_right = Point(pos.x+width,pos.y+height) 

class Polygon:
	def __init__(self,color):
		self.color = color
		self.vertices=[]

	def add_verts(self,points):
		for p in points:
			self.vertices.append(p)
	
	def add_vert(self,point):
		self.vertices.append(point)

	def get_vert_list(self):
		vert_lst=[]
		for v in self.vertices:
			vert_lst.append((v.x,v.y))
		return vert_lst

	def get_far_left(self):
		prev_low=sys.maxint
		for vert in self.vertices:
			if vert.x<prev_low:
				prev_low = vert.x
		return prev_low
		

	def get_far_right(self):
		prev_high=0
		for vert in self.vertices:
			if vert.x>=prev_high:
				prev_high=vert.x
		return prev_high

	def get_far_top(self):
		prev_low=sys.maxint
		for vert in self.vertices:
			if vert.y <= prev_low:
				prev_low = vert.y
		return prev_low
	
	def get_far_bottom(self):
		prev_high=0
		for vert in self.vertices:
			if vert.y>=prev_high:
				prev_high = vert.y
		return prev_high

	
	def get_height(self):
		return math.fabs(self.get_far_top()-self.get_far_bottom())

	def get_width(self):
		return math.fabs(self.get_far_right()-self.get_far_left())




def init_mst_way_list(mst_graph):
	current_node = mst_graph.get_nodes()[0]
	prev_node = current_node
	visited=[]
	way_lst=[]
	visited.append(current_node)

	while(len(visited)<len(mst_graph.get_nodes())):
		next_node = get_closest_unvisited_node(mst_graph,visited,current_node)
		if(next_node not in visited):
			visited.append(next_node)
		path = compute_path(mst_graph,current_node,next_node)
		
		for n in path:
			if n not in visited:
				visited.append(n)
			way_lst.append(mst_graph.get_node(n).get_pos())
		current_node = next_node
	return way_lst


def calc_euclidean_distance(pos1,pos2):
	return math.sqrt(math.pow((pos1[0]-pos2[0]),2) + math.pow((pos1[1]-pos2[1]),2))



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
		fScore[node] = sys.maxint
	
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
				openSet+=[neighbor]
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







def init_map(width,height,drone_radius):
	points_list = init_radius_points(width,height,drone_radius)
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

	return poly_list,new_points_list


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



def create_graph_from_map(poly_list,points_list):
	
	graph = Graph()
	
	for i in range(0,len(points_list)):
		graph.add_node(str(i),points_list[i])

	print("Number of Points "+ str(len(points_list)))
	tot_count = len(points_list) * len(points_list)
	count = 0

	for j in range(0,len(points_list)):
		for k in range (0, len(points_list)):
			count+=1
			print(str(count) +"/"+ str(tot_count))
			if(j!=k):
				isIntersect = False
				for poly in poly_list:
					if(check_if_edge_interects_poly(poly,Point(points_list[j][0],points_list[j][1]),Point(points_list[k][0],points_list[k][1]))):
						isIntersect = True
						break
				if(isIntersect==False):
					graph.add_edge(str(j),str(k))

	for node_id in graph.get_nodes():
		node = graph.get_node(node_id)
		if(len(node.get_neighbors())<=0):
			graph.remove_node(node_id)

	return graph


	
def init_poly_list(poly_sides,num_poly):
	poly_list = []
	for i in range(0,num_poly):
		vert_list=[]
		for j in range(0,poly_sides):
			vert_list.append((random.randint(0,800),random.randint(0,600)))
		poly_list.append(vert_list)
	return poly_list

def drone(x,y):
	gameDisplay.blit(droneSprite,(x-30,y-30))

def draw_waypoint(pos):
	pygame.draw.circle(gameDisplay,(0,0,255),pos,2)

def draw_waypoints(points_list):
	for point in points_list:
		pygame.draw.circle(gameDisplay,(0,0,255),point,2)

def draw_polys(poly_list):
	for polygon in poly_list:
		draw_polygon(polygon)


def draw_polygon(polygon):
	print(polygon.get_vert_list())
	pygame.draw.polygon(gameDisplay,(255,0,0),polygon.get_vert_list())

def draw_map(wapoint_list,polygon_list):
	for point in wapoint_list:
		draw_waypoint(point)

	for polygon in polygon_list:
		draw_polygon(polygon)

def draw_line(point1,point2):
	pygame.draw.line(gameDisplay, (0,255,0), [point1[0], point1[1]], [point2[0],point2[1]], 1)

def draw_graph(graph):

	for n in graph.get_nodes():
		node = graph.get_node(n)
		draw_waypoint(node.get_pos())
		for neighbor_id in node.get_neighbors():
			neighbour_node = graph.get_node(neighbor_id)
			draw_line(node.get_pos(),neighbour_node.get_pos())

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




#the following code below has to do with the pygame graphics and display




#points = init_radius_points(800,600,30)

''' initializes the graph both obstacles and waypoints
	and calculates minimum spanning tree
'''
print("Finding Points..")
poly_list,points = init_map(800,600,30)
print("Creating graph")
graph = create_graph_from_map(poly_list,points)
'''mst = MST(graph)
print("Calculating mst")
graph = mst.computeMST()
print("Calculating waypoint list")
way_lst = init_mst_way_list(graph)

#first waypoint on graph
drone_x=way_lst[0][0]
drone_y=way_lst[0][1]

#final waypoint on the graph
finalX = way_lst[len(way_lst)-1][0]
finalY = way_lst[len(way_lst)-1][1]'''


counter = 1
def update_pos(drone_x,drone_y,speedX,speedY):
	drone_x+=speedX
	drone_y+=speedY
	return drone_x,drone_y

def move_to(current_x,current_y,desiredX,desiredY,kp):
	move_x = kp*(desiredX-current_x)
	move_y = kp*(desiredY-current_y)
	return move_x,move_y

def is_pos_equal(pos1,pos2):
	if(math.fabs((pos1[0]-pos2[0]))<=1 and math.fabs((pos1[1]-pos2[1]))<=1):
		return True
	else:
		return False
'''def main():
	print("Hello")
	graph = create_graph()
	mst = MST(graph)
	graph = mst.computeMST()
	graph.print_graph()
	for node in graph.get_nodes():
		print(node + " " + str(graph.get_node(node).get_pos()))

	path = init_mst_way_list(graph)
	print(path)
	print("Done")

if __name__ == "__main__":
	main()'''



while not crashed:

	for event in pygame.event.get():
		if(event.type== pygame.QUIT):
			crashed = True

	gameDisplay.fill(screenColor)
	draw_graph(graph)
	#drone(drone_x,drone_y)
	draw_polys(poly_list)

	print(graph.num_vertices)
	print(counter)
	'''if counter<len(way_lst)-1:
		if is_pos_equal((drone_x,drone_y),way_lst[counter]):
			print("Im here")
			print((drone_x,drone_y))
			counter+=1
			print(counter)
	destX = way_lst[counter][0]
	destY = way_lst[counter][1]
	print(destX,destY)

	move_x,move_y = move_to(drone_x,drone_y,destX,destY,0.05)
	drone_x,drone_y = update_pos(drone_x,drone_y,move_x,move_y)'''


	'''if(is_pos_equal((drone_x,drone_y),(finalX,finalY))):
		mst = MST(graph)
		graph = mst.computeMST()
		graph.print_graph()
		counter = 1
		way_lst = init_mst_way_list(graph)
		print(way_lst)'''

	pygame.display.update()
	clock.tick(60)


pygame.quit()
quit()



