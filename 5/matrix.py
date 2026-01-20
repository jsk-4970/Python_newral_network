#!/usr/bin/env python3
import random
import math


def mat_mul(A, B):
    """行列積 A @ B"""
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])

    result = [[0.0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result


def mat_add(A, B):
    """行列和 (ブロードキャスト対応)"""
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)

    result = [[0.0] * cols_A for _ in range(rows_A)]
    for i in range(rows_A):
        bi = i if rows_B > 1 else 0
        for j in range(cols_A):
            result[i][j] = A[i][j] + B[bi][j]
    return result


def apply_func(mat, f):
    """各要素に関数を適用"""
    rows = len(mat)
    cols = len(mat[0])
    result = [[0.0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result[i][j] = f(mat[i][j])
    return result
