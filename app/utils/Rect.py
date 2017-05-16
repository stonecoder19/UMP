from Point import Point

class Rect:
	def __init__(self,pos,width,height):
		self.top_left = pos
		self.bottom_left = Point(pos.x,pos.y+height)
		self.top_right = Point(pos.x+width,self.top_left.y)
		self.bottom_right = Point(pos.x+width,pos.y+height)
		self.width = width
		self.height = height 