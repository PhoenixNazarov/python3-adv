import numpy as np


class Matrix:
    def __init__(self, data):
        self.data = [list(row) for row in data]
        self.shape = (len(self.data), len(self.data[0])) if self.data else (0, 0)

    def __add__(self, other):
        if self.shape != other.shape:
            raise ValueError()
        return Matrix([
            [
                self.data[i][j] + other.data[i][j] for j in range(self.shape[1])
            ] for i in range(self.shape[0])
        ])

    def __mul__(self, other):
        if self.shape != other.shape:
            raise ValueError()
        return Matrix([
            [
                self.data[i][j] * other.data[i][j] for j in range(self.shape[1])
            ] for i in range(self.shape[0])
        ])

    def __matmul__(self, other):
        if self.shape[1] != other.shape[0]:
            raise ValueError()
        return Matrix([
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.shape[1])) for j in range(other.shape[1])
            ] for i in range(self.shape[0])
        ])


np.random.seed(0)

matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))


def save(matrix, path):
    with open(path, "w") as file:
        for row in matrix.data:
            file.write(" ".join(map(str, row)) + "\n")


save(matrix1 + matrix2, 'artifacts/1/matrix+.txt')
save(matrix1 * matrix2, 'artifacts/1/matrix*.txt')
save(matrix1 @ matrix2, 'artifacts/1/matrix@.txt')
