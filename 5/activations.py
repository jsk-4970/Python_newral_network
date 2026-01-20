#!/usr/bin/env python3
import math
from matrix import apply_func


class Sigmoid:
    def __call__(self, x):
        def sigmoid(v):
            if v < -500:
                return 0.0
            if v > 500:
                return 1.0
            return 1.0 / (1.0 + math.exp(-v))
        return apply_func(x, sigmoid)

    def deriv(self, y):
        # y = sigmoid(x) として、導関数は y * (1 - y)
        return apply_func(y, lambda v: v * (1 - v))


class ReLU:
    def __call__(self, x):
        return apply_func(x, lambda v: max(0.0, v))

    def deriv(self, x):
        return apply_func(x, lambda v: 1.0 if v > 0 else 0.0)


class Linear:
    def __call__(self, x):
        return x

    def deriv(self, x):
        rows = len(x)
        cols = len(x[0])
        return [[1.0] * cols for _ in range(rows)]
