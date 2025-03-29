import numbers

import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin


class MatrixMixin:
    def __init__(self, value):
        self._value = np.asarray(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    def to_file(self, filename):
        np.savetxt(filename, self.value, fmt='%d')

    def __str__(self):
        return "\n".join(" ".join(map(str, row)) for row in self.value)


class Matrix(NDArrayOperatorsMixin, MatrixMixin):
    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """
        Использовано из документации о NDArrayOperatorsMixin, пример с ArrayLike
        """
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (Matrix,)):
                return NotImplemented

        inputs = tuple(x.value if isinstance(x, Matrix) else x for x in inputs)
        if out:
            kwargs['out'] = tuple(x.value if isinstance(x, Matrix) else x for x in out)

        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(Matrix(x) for x in result)
        elif method == 'at':
            return None
        else:
            return Matrix(result)


np.random.seed(0)

matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

(matrix1 + matrix2).to_file('artifacts/2/matrix+.txt')
(matrix1 * matrix2).to_file('artifacts/2/matrix*.txt')
(matrix1 @ matrix2).to_file('artifacts/2/matrix@.txt')
