from main import FigureFactory, Figure, Triangle, Circle
import pytest
import math


def test_create_triangle():
    """Правильное создание треугольника"""

    data1 = {"a": 3, "b": 4, "c": 5}
    fig1 = FigureFactory.create_figure("triangle", data1)

    assert type(fig1) is Triangle

    """Неправильное создание треугольника"""

    # Не хватает сторон
    with pytest.raises(ValueError):
        FigureFactory.create_figure("triangle", {"a": 3})

    # Стороны отрицательные
    with pytest.raises(ValueError):
        FigureFactory.create_figure("triangle", {"a": -1, "b": 2, "c": 3})

    # Несуществующий треугольник
    with pytest.raises(ValueError):
        FigureFactory.create_figure("triangle", {"a": 1, "b": 1, "c": 10})


def test_create_circle():
    """Правильное создание круга"""

    data1 = {"r": 3}
    fig1 = FigureFactory.create_figure("circle", data1)

    assert type(fig1) is Circle

    """Неправильное создание круга"""

    # Неправильное название радиуса
    with pytest.raises(ValueError):
        FigureFactory.create_figure("circle", {"a": 3})

    # Радиус отрицательный
    with pytest.raises(ValueError):
        FigureFactory.create_figure(
            "circle",
            {
                "r": -1,
            },
        )


def test_is_right_angled():
    # Правильный треугольник
    data1 = {"a": 3, "b": 4, "c": 5}
    fig1 = FigureFactory.create_figure("triangle", data1)

    assert fig1.is_right_angled() == True

    # "Почти" правильный треугольник
    data2 = {"a": 3.00000001, "b": 4, "c": 5}
    fig2 = FigureFactory.create_figure("triangle", data2)

    assert fig2.is_right_angled() == False

    с
    data3 = {"a": 3, "b": 4, "c": 5.00000001}
    fig3 = FigureFactory.create_figure("triangle", data3)

    assert fig3.is_right_angled() == False


def test_squares():
    # Площадь треугольника
    data1 = {"a": 3, "b": 4, "c": 5}
    fig1 = FigureFactory.create_figure("triangle", data1)

    assert math.isclose(fig1.square(), 6.0, rel_tol=1e-9)

    # Площадь круга
    data2 = {"r": 3}
    fig2 = FigureFactory.create_figure("circle", data2)

    expected_area = math.pi * 3 * 3
    assert math.isclose(fig2.square(), expected_area, rel_tol=1e-9)

    # Площадь "почти" правильного треугольника
    data3 = {"a": 3, "b": 4, "c": 5.00000001}
    fig3 = FigureFactory.create_figure("triangle", data3)

    p = (data3["a"] + data3["b"] + data3["c"]) / 2
    assert math.isclose(fig3.square(), math.sqrt(p * (p - data3["a"]) * (p - data3["b"]) * (p - data3["c"])), rel_tol=1e-9)


def test_add_new_figure():
    """Создание и регистрация новой фигуры"""

    class Rectangle(Figure):
        def __init__(self, data: dict):
            if "a" not in data.keys() or "b" not in data.keys():
                raise ValueError("Не найдены нужные стороны")
            if not (data["a"] > 0 and data["b"] > 0):
                raise ValueError("Стороны должны быть положительными")
            self.a = data["a"]
            self.b = data["b"]

        def square(self):
            return self.a * self.b

    FigureFactory.register_figure("rectangle", Rectangle)
    assert FigureFactory._figures.__contains__("rectangle")

    data3 = {"a": 3, "b": 4}
    fig3 = FigureFactory.create_figure("rectangle", data3)
    assert type(fig3) == Rectangle
    assert fig3.square() == 12

    """Регистрация существующей фигуры"""
    with pytest.raises(ValueError):
        FigureFactory.register_figure("triangle", Triangle)
    with pytest.raises(ValueError):
        FigureFactory.register_figure("rectangle", Rectangle)
