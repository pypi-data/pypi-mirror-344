import math


class Figure:
    def square(self) -> float:
        pass


class Triangle(Figure):
    def __init__(self, data: dict):
        if "a" not in data.keys() or "b" not in data.keys() or "c" not in data.keys():
            print(data)
            raise ValueError("Не найдены нужные стороны")
        if not (data["a"] > 0 and data["b"] > 0 and data["c"] > 0):
            raise ValueError("Стороны должны быть положительными")
        if not (
            data["a"] + data["b"] > data["c"]
            and data["a"] + data["c"] > data["b"]
            and data["b"] + data["c"] > data["a"]
        ):
            raise ValueError("Такого треугольника не может существовать")
        self.a = data["a"]
        self.b = data["b"]
        self.c = data["c"]

    def square(self) -> float:
        p = (self.a + self.b + self.c) / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def is_right_angled(self) -> bool:
        sides = sorted([self.a, self.b, self.c])
        return math.isclose(sides[0] ** 2 + sides[1] ** 2, sides[2] ** 2, rel_tol=1e-9)


class Circle(Figure):
    def __init__(self, data: dict):
        if "r" not in data.keys():
            raise ValueError("Не найден радиус")
        if data["r"] <= 0:
            raise ValueError("Радиус должен быть положительным")
        self.r = data["r"]

    def square(self) -> float:
        return math.pi * self.r * self.r


class FigureFactory:
    _figures = {"triangle": Triangle, "circle": Circle}

    @classmethod
    def create_figure(cls, fig_type: str, data: dict) -> Figure:
        fig_class = cls._figures.get(fig_type)
        if not fig_class:
            raise ValueError("Неизвестный тип фигуры")
        return fig_class(data)

    @classmethod
    def register_figure(cls, name: str, product_class: type):
        if name in cls._figures.keys() or product_class in cls._figures.values():
            raise ValueError("Такая фигура уже зарегистрирована")
        cls._figures[name] = product_class
