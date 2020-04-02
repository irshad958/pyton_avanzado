class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.x},{self.y})"


def obtener_pares(size=10000000):
    for i in range(size):
        yield i


def obtener_pares(size=10):
    lista = []
    for i in range(size):
        lista.append(i)
    return lista


if __name__ == '__main__':
    a = Vector(1, 2)
    b = Vector(2, 4)
    c = a + b
