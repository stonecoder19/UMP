import pygame
import random
from MST import *
import math






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
		lst+=[node.get_pos()]
	return lst

def init_poly_list(poly_sides,num_poly):
	poly_list = []
	for i in range(0,num_poly):
		vert_list=[]
		for j in range(0,poly_sides):
			vert_list+= [(random.randint(0,800),random.randint(0,600))]
		poly_list+=[vert_list]
	return poly_list

def drone(x,y):
	gameDisplay.blit(droneSprite,(x-30,y-30))

def draw_waypoint(pos):
	pygame.draw.circle(gameDisplay,(0,0,255),pos,6)

def draw_polygon(vert_list):
	pygame.draw.polygon(gameDisplay,(0,255,0),vert_list)

def draw_map(wapoint_list,polygon_list):
	for point in wapoint_list:
		draw_waypoint(point)

	for polygon in polygon_list:
		draw_polygon(polygon)
def draw_line(point1,point2):
	pygame.draw.line(gameDisplay, (0,255,0), [point1[0], point1[1]], [point2[0],point2[1]], 5)

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
	
	g.add_node('D',(50,50))
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













poly_list = init_poly_list(5,2)
graph = create_graph()
way_lst = init_waypoint_list(graph)

print(way_lst)

drone_x=way_lst[0][0]
drone_y=way_lst[0][1]
#drone_y=300-30
#drone_x=400-30
#print((drone_x-20,drone_y))

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

while not crashed:

	for event in pygame.event.get():
		if(event.type== pygame.QUIT):
			crashed = True
		print(event)
	gameDisplay.fill(screenColor)
	#pygame.draw.line(gameDisplay, (0,255,0), [0, 0], [50,30], 5)
	#pygame.draw.circle(gameDisplay,(0,0,255),(500,500),6)
	#pygame.draw.polygon(gameDisplay,(255,0,0),[(400,200),(400,400),(200,400),(200,200)])
	#draw_map(way_lst,poly_list)
	draw_graph(graph)
	#draw_waypoint((120,250))
	drone(drone_x,drone_y)

	#print(drone_x)
	#print(drone_y)

	if counter<graph.num_vertices-1:
		if is_pos_equal((drone_x,drone_y),way_lst[counter]):
			print("Im here")
			print((drone_x,drone_y))
			counter+=1
			print(counter)
	destX = way_lst[counter][0]
	destY = way_lst[counter][1]
	print(destX,destY)

	#drone_x,drone_y = update_pos(drone_x,drone_y,2,0)
	move_x,move_y = move_to(drone_x,drone_y,destX,destY,0.05)
	drone_x,drone_y = update_pos(drone_x,drone_y,move_x,move_y)


	if(drone_x>=600):
		mst = MST(graph)
		graph = mst.compute_MST()
		graph.print_graph()
	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()



