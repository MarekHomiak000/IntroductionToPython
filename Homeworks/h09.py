# Meno: Homiak, Marek
# Spolupráca: 
# Použité zdroje: 
# Čas: 

# Podrobný popis je dostupný na: https://github.com/ianmagyar/introduction-to-python/blob/master/homeworks/homework09.md

# Hodnotenie: /1b


# Bridge
# Abstraction - Shape
# RefinedAbstraction - CircleShape
# Implementor - draw_circle
# ConcreteImplementor - DrawingAPI1, DrawingAPI2

class DrawingAPI1:
    def draw_circle(self, x, y, radius):
        print("API1 drawing circle at ({}, {}) with radius {}".format(x, y, radius))

class DrawingAPI2:
    def draw_circle(self, x, y, radius):
        print("API2 drawing circle at ({}, {}) with radius {}".format(x, y, radius))

class Shape:
    def __init__(self, drawing_api):
        self.drawing_api = drawing_api

    def draw(self):
        pass

    def resize_by_percentage(self, percent):
        pass

class CircleShape(Shape):
    def __init__(self, x, y, radius, drawing_api):
        super().__init__(drawing_api)
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        self.drawing_api.draw_circle(self.x, self.y, self.radius)

    def resize_by_percentage(self, percent):
        self.radius *= percent / 100.0
