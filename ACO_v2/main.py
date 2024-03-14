sample: list[str] = ['a', '3', 'c', 2]

from abc import ABCMeta, abstractmethod


class Shape(metaclass=ABCMeta):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14 * self.radius


# Attempting to instantiate Shape will raise an error since it's abstract
# shape = Shape()  # This will raise an error

# But Circle, which implements all abstract methods, can be instantiated
if __name__ == '__main__':
    circle = Circle(5)
    print("Area:", circle.area())
    print("Perimeter:", circle.perimeter())
