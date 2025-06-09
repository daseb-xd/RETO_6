from math import pi, acos


class Point:
    definition: str = "Entidad geometrica abstracta que representa una ubicación en un espacio."

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def compute_distance(self, point: "Point") -> float:
        distance = ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5
        return distance

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, startp: "Point", endp: "Point"):
        self.startp = startp
        self.endp = endp

    def compute_length(self) -> float:
        return self.startp.compute_distance(self.endp)

    def __repr__(self):
        return f"Line({self.startp}, {self.endp})"


class Shape:
    def __init__(self, is_regular: bool, vertices: list[Point], edges: list[Line] = None):
        self.is_regular = is_regular
        self._vertices = vertices
        if edges is not None:
            self._edges = edges
        else:
            self._edges = [
                Line(vertices[i], vertices[(i + 1) % len(vertices)])
                for i in range(len(vertices))
            ]

    def get_vertices(self) -> list[Point]:
        return self._vertices

    def get_edges(self) -> list[Line]:
        return self._edges

    def get_inner_angles(self) -> list[float]:
        return self._inner_angles

    def set_is_regular(self, is_regular: bool):
        self.is_regular = is_regular

    def set_edges(self, edges: list[Line]):
        self._edges = edges

    def set_vertices(self, vertices: list[Point]):
        self._vertices = vertices

    def set_inner_angles(self, inner_angles: list[float]):
        self._inner_angles = self.compute_inner_angles()
    
    # Abstract methods to be implemented by subclasses, raises error if not implemented
    def compute_area(self) -> float:
        raise NotImplementedError("compute_area() not implemented in this shape")

    def compute_perimeter(self) -> float:
        raise NotImplementedError("compute_perimeter() not implemented in this shape")

    def compute_inner_angles(self) -> list[float]:
        raise NotImplementedError("compute_inner_angles() not implemented in this shape")


class Triangle(Shape):
    def __init__(self, is_regular: bool, vertices: list[Point], edges: list[Line]):
        super().__init__(is_regular, vertices, edges)
        self.a = self._edges[0].compute_length()
        self.b = self._edges[1].compute_length()
        self.c = self._edges[2].compute_length()
        # Triangle inequality check
        if not (
            self.a + self.b > self.c and
            self.a + self.c > self.b and
            self.b + self.c > self.a 
            ):
            raise ValueError("The provided vertices/edges do not form a valid triangle (triangle inequality violated)")
        self._area = self.compute_area()
        self._perimeter = self.compute_perimeter()
        self._inner_angles = self.compute_inner_angles()

    def compute_area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        area = (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5
        return area

    def compute_perimeter(self) -> float:
        return self.a + self.b + self.c

    def compute_inner_angles(self) -> list[float]:
        A = round(acos((self.b ** 2 + self.c ** 2 - self.a ** 2) / (2 * self.b * self.c)) * 180 / pi, 2)
        B = round(acos((self.a ** 2 + self.c ** 2 - self.b ** 2) / (2 * self.a * self.c)) * 180 / pi, 2)
        C = round(acos((self.a ** 2 + self.b ** 2 - self.c ** 2) / (2 * self.a * self.b)) * 180 / pi, 2)
        return [A, B, C]


class Isosceles(Triangle):
    def __init__(self, vertices: list[Point], edges: list[Line]):
        super().__init__(False, vertices, edges)
        sides = [round(self.a, 5), round(self.b, 5), round(self.c, 5)]
        unique_lengths = len(set(sides))
        # Check for isosceles triangle conditions
        if unique_lengths == 1:
            raise ValueError("Isosceles triangle cannot have 3 equal sides")
        if unique_lengths == 3:
            raise ValueError("Isosceles triangle must have exactly two equal sides")


class Equilateral(Triangle):
    def __init__(self, vertices: list[Point], edges: list[Line]):
        super().__init__(True, vertices, edges)
        self.a = self._edges[0].compute_length()
        self.b = self.a
        self.c = self.b
        # Check if all sides are equal
        if round(self.a, 2) != round(self.b, 2) or round(self.b, 2) != round(self.c, 2):
            raise ValueError("Equilateral triangle must have equal sides")


class Scalene(Triangle):
    def __init__(self, vertices: list[Point], edges: list[Line]):
        super().__init__(False, vertices, edges)
        # Check if all sides are different
        if self.a == self.b or self.b == self.c or self.a == self.c:
            raise ValueError("Scalene triangle cannot have equal sides")


class RightTriangle(Triangle):
    def __init__(self, vertices: list[Point], edges: list[Line]):
        super().__init__(False, vertices, edges)
        # Check if one angle is 90 degrees
        if not any(abs(angle - 90) < 1e-2 for angle in self._inner_angles):
            raise ValueError("Right triangle must have one right angle")


class Rectangle(Shape):
    def __init__(self, is_regular: bool, vertices: list[Point], edges: list[Line]):
        super().__init__(False, vertices, edges)
        self.a = self._edges[0].compute_length()
        self.b = self._edges[1].compute_length()
        self._area = self.compute_area()
        self._perimeter = self.compute_perimeter()
        self._inner_angles = self.compute_inner_angles()

    def compute_area(self) -> float:
        return self.a * self.b

    def compute_perimeter(self) -> float:
        return (self.a + self.b) * 2

    def compute_inner_angles(self) -> list[float]:
        return [90, 90, 90, 90]


class Square(Rectangle):
    def __init__(self, vertices: list[Point], edges: list[Line] = None):
        super().__init__(True, vertices, edges)
        self.is_regular = True
        self.a = self._edges[0].compute_length()
        self.b = self.a
        # Check if all sides are equal
        if self.a != self.b:
            raise ValueError("Square must have equal sides")

    def compute_area(self) -> float:
        return self.a * self.a

    def compute_perimeter(self) -> float:
        return self.a * 4

#Usage example
if __name__ == "__main__":
    t1 = RightTriangle([Point(0, 0), Point(3, 0), Point(0, 4)], None)
    print("Triángulo Rectángulo")
    print("Área:", t1._area)
    print("Perímetro:", t1._perimeter)
    print("Ángulos internos:", t1._inner_angles)
    print("Vértices:", t1._vertices)
    print("Lados:", t1._edges)
    print("¿Es regular?:", t1.is_regular)
    print("\n")

    t2 = Scalene([Point(0, 0), Point(3, 0), Point(1, 4)], None)
    print("Triángulo Escaleno")
    print("Área:", t2._area)
    print("Perímetro:", t2._perimeter)
    print("Ángulos internos:", t2._inner_angles)
    print("Vértices:", t2._vertices)
    print("Lados:", t2._edges)
    print("¿Es regular?:", t2.is_regular)
    print("\n")

    t3 = Isosceles([Point(0, 0), Point(3, 0), Point(1.5, 4)], None)
    print("Triángulo Isósceles")
    print("Área:", t3._area)
    print("Perímetro:", t3._perimeter)
    print("Ángulos internos:", t3._inner_angles)
    print("Vértices:", t3._vertices)
    print("Lados:", t3._edges)
    print("¿Es regular?:", t3.is_regular)
    print("\n")

    t4 = Equilateral([Point(0, 0), Point(3, 0), Point(1.5, 2.598)], None)
    print("Triángulo Equilátero")
    print("Perímetro:", t4._perimeter)
    print("Ángulos internos:", t4._inner_angles)
    print("Vértices:", t4._vertices)
    print("Lados:", t4._edges)
    print("¿Es regular?:", t4.is_regular)
    print("\n")

    r1 = Rectangle(False, [Point(0, 0), Point(3, 0), Point(3, 4), Point(0, 4)], None)
    print("Rectángulo")
    print("Área:", r1._area)
    print("Perímetro:", r1._perimeter)
    print("Ángulos internos:", r1._inner_angles)
    print("Vértices:", r1._vertices)
    print("Lados:", r1._edges)
    print("¿Es regular?:", r1.is_regular)
    print("\n")

    s1 = Square([Point(0, 0), Point(3, 0), Point(3, 3), Point(0, 3)], None)
    print("Cuadrado")
    print("Área:", s1._area)
    print("Perímetro:", s1._perimeter)
    print("Ángulos internos:", s1._inner_angles)
    print("Vértices:", s1._vertices)
    print("Lados:", s1._edges)
    print("¿Es regular?:", s1.is_regular)
    print("\n")







