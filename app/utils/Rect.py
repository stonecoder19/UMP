from Point import Point

"""
Rectangle Class
"""
class Rect:
    
    def __init__(self, pos, width, height):
        """
        Initializes a rectangle

        Args:
            pos(tuple): node_id of neighbour
            width(float): width of rectangle
            height(float): height of rectangle
        """
        self.top_left = pos
        self.bottom_left = Point(pos.x, pos.y + height)
        self.top_right = Point(pos.x + width, self.top_left.y)
        self.bottom_right = Point(pos.x + width, pos.y + height)
        self.width = width
        self.height = height 

    def get_width(self):
        """
        Returns width of rect
        """
        return self.width

    def get_height(self):
        """
        Returns height of rect
        """
        return self.height

