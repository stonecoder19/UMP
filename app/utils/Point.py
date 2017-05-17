"""
Point Class - Represents a point on the map
"""
class Point:
    
    def __init__(self, x, y):
        """
        Initializes the x and y coord of a point of the map
        """
        self.x = x
        self.y = y

    def get_x(self):
        """
        Returns x coord
        """
        return self.x

    def get_y(self):
        """
        Returns y coord
        """
        return self.y

