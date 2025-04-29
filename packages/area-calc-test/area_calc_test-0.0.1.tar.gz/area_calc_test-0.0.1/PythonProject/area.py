import math

class Area():

    def __init__(self, figure_type, **kwargs):
        self.figure_type = figure_type
        self.kwargs = kwargs

    def calc_area(self):

        if self.figure_type == "circle":
            try:
                area = math.pi * self.kwargs["r"] ** 2
                return area
            except KeyError:
                print("No radius provided")

        elif self.figure_type == "triangle":
            try:
                sides = [self.kwargs["a"], self.kwargs["b"], self.kwargs["c"]]
                sides.sort()
                a, b, c = sides
                if a ** 2 + b ** 2 == c ** 2:
                    area = a * b / 2
                else:
                    p = (a + b + c) / 2
                    x = p * (p - a) * (p - b) * (p - c)
                    try:
                        area = math.sqrt(x)
                        return area
                    except ValueError:
                        print("Wrong triangle sides")

            except KeyError:
                print("Wrong sides of the triangle provided")

        else:
            print("For this figure type function is not implemented")
            raise NotImplementedError