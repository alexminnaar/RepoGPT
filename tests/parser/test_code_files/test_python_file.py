# Using a class definition
class RectangleClass:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_area(self):
        return self.length * self.width

    def calculate_perimeter(self):
        return 2 * (self.length + self.width)


# Using a function to create an object (Factory function)
def create_square(side_length):
    return {"side_length": side_length}

def square_area(square):
    return square["side_length"] ** 2

def square_perimeter(square):
    return 4 * square["side_length"]


# Using a class with @staticmethod decorator
class CircleStatic:
    def __init__(self, radius):
        self.radius = radius

    @staticmethod
    def calculate_area(radius):
        return 3.14159 * radius * radius

    @staticmethod
    def calculate_circumference(radius):
        return 2 * 3.14159 * radius


# Using a class with @classmethod decorator
class CircleClassMethod:
    def __init__(self, radius):
        self.radius = radius

    @classmethod
    def create_circle(cls, diameter):
        return cls(diameter / 2)

    def calculate_area(self):
        return 3.14159 * self.radius * self.radius

    def calculate_circumference(self):
        return 2 * 3.14159 * self.radius