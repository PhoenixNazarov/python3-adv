from functools import cache

import numpy as np

from matrix_1 import Matrix


class MatrixHashable(Matrix):
    def __hash__(self):
        hash_value = 0
        for i, row in enumerate(self.data):
            for value in row:
                # Суммируем все элементу, умножая на 2 в степени индекса строки
                hash_value += value * (2 ** i)
        # Потом берем остаток от деления на 1000, чтобы кеш был не сильно большой и его можно было найти)
        return int(hash_value % 1000)

    def __eq__(self, other):
        return np.array_equal(self.data, other.data)


@cache
def cache_matmul(a, b):
    print('res')
    return a @ b


np.random.seed(0)

B = MatrixHashable(np.random.randint(0, 10, (10, 10)))
D = B


def save(matrix, path):
    with open(path, "w") as file:
        for row in matrix.data:
            file.write(" ".join(map(str, row)) + "\n")


while True:
    A = MatrixHashable(np.random.randint(0, 10, (10, 10)))
    C = MatrixHashable(np.random.randint(0, 10, (10, 10)))
    if (hash(A) == hash(C)) and (A != C) and (B == D) and (A @ B != C @ D):
        save(A, 'artifacts/3/A.txt')
        save(B, 'artifacts/3/B.txt')
        save(C, 'artifacts/3/C.txt')
        save(A @ B, 'artifacts/3/AB.txt')
        save(C @ D, 'artifacts/3/CD.txt')
        with open('artifacts/3/hash.txt', 'w') as file:
            file.write(str(hash(A)))
        break
