import math

def sphere(position):
    x = position["x"]
    y = position["y"]
    v = x * x + y * y
    return v

def rastrigin(position):
    x = position["x"]
    y = position["y"]
    v = 20 + ((x * x - 10 * math.cos(2 * math.pi * x)) + (y * y - 10 * math.cos(2 * math.pi * y)))
    return v

def rosenbrock(position):
    x = position["x"]
    y = position["y"]
    v = (100 * (y - x * x) * (y - x * x)) + ((1 - x) * (1 - x))
    return v

def griewank(position):
    x = position["x"]
    y = position["y"]
    v = 1 + ((x * x + y * y) / 4000) - math.cos(x / math.sqrt(1)) * math.cos(y / math.sqrt(2))
    return v

def alpine(position):
    x = position["x"]
    y = position["y"]
    v = abs(x * math.sin(x) + 0.1 * x) + abs(y * math.sin(y) + 0.1 * y)
    return v

def two_n_minima(position):
    x = position["x"]
    y = position["y"]
    v = (x * x * x * x - 16 * x * x + 5 * x) + (y * y * y * y - 16 * y * y + 5 * y)
    return v