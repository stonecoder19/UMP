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