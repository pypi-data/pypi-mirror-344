# test_figures_package

## Using

1. Triangle

```
data = {"a": 3, "b": 4, "c": 5}
figure = FigureFactory.create_figure("triangle", data)
figure.square() # result: 6.0
figure.is_right_angled() # result: True
```

2. Create circle

```
data = {"r": 3}
figure = FigureFactory.create_figure("circle", data)
figure.square()
```

3. Create new figure and register in FigureFactory

```
class Rectangle(Figure):
        def __init__(self, data: dict):
            if "a" not in data.keys() or "b" not in data.keys():
                raise ValueError("Do not finded correct shapes")
            if not (data["a"] > 0 and data["b"] > 0):
                raise ValueError("Shapes must be greated than zero")
            self.a = data["a"]
            self.b = data["b"]

        def square(self):
            return self.a * self.b

FigureFactory.register_figure("rectangle", Rectangle)
```