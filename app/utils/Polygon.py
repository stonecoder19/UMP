import sys
import math



"""
Polygon class
"""
class Polygon:
    def __init__(self, color):
        self.color = color
        self.vertices = []

    def add_verts(self, points):
        """
        Adds a list of vertices to the polygon

        Args:
            points(list): list of vertices to be added
        """
        for point in points:
            self.vertices.append(point)
    
    def add_vert(self, point):
        """
        Adds a vertex to the polygon

        Args:
            point(Point): vertex to be added
        """
        self.vertices.append(point)

    
    def get_vert_list(self):
        """
        Returns a the list of vertices as tuples

        Returns:
            list: list of vertices
        """
        vert_lst = []
        for vert in self.vertices:
            vert_lst.append((vert.x, vert.y))
        return vert_lst

    def get_far_left(self):
        """
        Returns the minimum x coord of the polygon
        
        Returns:
            float: min x coord
        """
        prev_low = sys.maxint
        for vert in self.vertices:
            if vert.x < prev_low:
                prev_low = vert.x
        return prev_low
    
    def get_far_right(self):
        """
        Returns the maximum x coord of the polygon

        Returns:
            float:max x coord

        """
        prev_high = self.vertices[0].x
        for vert in self.vertices:
            if vert.x >= prev_high:
                prev_high = vert.x
        return prev_high

    def get_far_top(self):
        """
        Returns the minimum y coord of the polygon

        Returns:
            float: min y coord

        """
        prev_low = sys.maxint
        for vert in self.vertices:
            if vert.y <= prev_low:
                prev_low = vert.y
        return prev_low
    
    def get_far_bottom(self):
        """
        Returns the maximum y coord of the polygon

        Returns:
            float: min y coord

        """
        prev_high = 0
        for vert in self.vertices:
            if vert.y >= prev_high:
                prev_high = vert.y
        return prev_high

    
    def get_height(self):
        """
        Returns the height of the polygon

        Returns:
            float:height
        """
        return math.fabs(self.get_far_top()-self.get_far_bottom())

    def get_width(self):
        """
        Returns the width of the polygon

        Returns:
            float:width

        """
        return math.fabs(self.get_far_right()-self.get_far_left())

