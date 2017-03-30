import pygame
import random






pygame.init()
gameDisplay = pygame.display.set_mode((800,600))

pygame.display.set_caption('New Window')
clock = pygame.time.Clock()

screenColor = (255,255,255)
droneSprite = pygame.image.load('drone.png')
crashed = False

def init_waypoint_list():
	lst = []
	for i in range(0,30):
		lst+= [(random.randint(0,800),random.randint(0,600))]
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
	gameDisplay.blit(droneSprite,(x,y))

def draw_waypoint(pos):
	pygame.draw.circle(gameDisplay,(0,0,255),pos,6)

def draw_polygon(vert_list):
	pygame.draw.polygon(gameDisplay,(0,255,0),vert_list)

def draw_map(wapoint_list,polygon_list):
	for point in wapoint_list:
		draw_waypoint(point)

	for polygon in polygon_list:
		draw_polygon(polygon)






way_lst = init_waypoint_list()
poly_list = init_poly_list(5,2)

drone_x=0
drone_y=0
def update_pos(drone_x,drone_y,speedX,speedY):
	drone_x+=speedX
	drone_y+=speedY
	return drone_x,drone_y


while not crashed:

	for event in pygame.event.get():
		if(event.type== pygame.QUIT):
			crashed = True
		print(event)
	gameDisplay.fill(screenColor)
	#pygame.draw.line(gameDisplay, (0,255,0), [0, 0], [50,30], 5)
	#pygame.draw.circle(gameDisplay,(0,0,255),(500,500),6)
	#pygame.draw.polygon(gameDisplay,(255,0,0),[(400,200),(400,400),(200,400),(200,200)])
	draw_map(way_lst,poly_list)
	drone(drone_x,drone_y)
	drone_x,drone_y = update_pos(drone_x,drone_y,2,0)
	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()



