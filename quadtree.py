import pygame

class Quadtree:
    def __init__(self, boundary : pygame.Rect, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width / 2
        h = self.boundary.height / 2

        ne_boundary = Rectangle(x + w/2, y - h/2, w, h)
        self.northeast = Quadtree(ne_boundary, self.capacity)

        nw_boundary = Rectangle(x - w/2, y - h/2, w, h)
        self.northwest = Quadtree(nw_boundary, self.capacity)

        se_boundary = Rectangle(x + w/2, y + h/2, w, h)
        self.southeast = Quadtree(se_boundary, self.capacity)

        sw_boundary = Rectangle(x - w/2, y + h/2, w, h)
        self.southwest = Quadtree(sw_boundary, self.capacity)

        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northeast.insert(point): return True
            if self.northwest.insert(point): return True
            if self.southeast.insert(point): return True
            if self.southwest.insert(point): return True

    def query(self, range : pygame.Rect):
        result = []
        if not self.boundary.contains(range):
            return result
        else:
            for p in self.points:
                if range.contains(p):
                    result.append(p)

            if self.divided:
                result += self.northeast.query(range)
                result += self.northwest.query(range)
                result += self.southeast.query(range)
                result += self.southwest.query(range)

        return result

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point):
        return (self.x - self.width / 2 <= point.x <= self.x + self.width / 2 and
                self.y - self.height / 2 <= point.y <= self.y + self.height / 2)

    def intersects(self, range):
        return not (range.x - range.width / 2 > self.x + self.width / 2 or
                    range.x + range.width / 2 < self.x - self.width / 2 or
                    range.y - range.height / 2 > self.y + self.height / 2 or
                    range.y + range.height / 2 < self.y - self.height / 2)


#Singleton class for QuadTreeService
class QuadTreeService:

    _instance = None

    def __init__(self):
        if QuadTreeService._instance != None:
            raise Exception("This class is a singleton!")
        else:
            QuadTreeService._instance = self
        self.quadtreeDict = {}

    def add_quadtree(self, key : str, quadtree : Quadtree):
        self.quadtreeDict[key] = quadtree

    def get_quadtree(self, key : str):
        return self.quadtreeDict[key]

    @staticmethod
    def get_instance():
        if QuadTreeService._instance == None:
             return QuadTreeService()
        return QuadTreeService._instance
