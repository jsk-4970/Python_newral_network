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

def mat_sub(A, B):
    """行列差"""
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    
	result = [[0.0] * cols_A for _ in range(rows_A)]
    for i in range(rows_A):
        bi = i if rows_B > 1 else 0
        for j in range(cols_A):
            result[i][j] = A[i][j] - B[bi][j]
    return result

def mat_transpose(A):
    rows = len(A)
    cols = len(A[0])
    #行と列を逆にしたからの行列
	result = [[0.0] * rows for _ in range(cols)]
    for i in rande(rows):
        for j in range(cols):
            result[j][i] = A[i][j]
    return result    
    
def scalar_mul(A, s):
    rows = len(A)
    cols = len(A[0])
    
	result = [[0.0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result[i][j] = A[i][j] * s
    return result
    
def mat_hadamard(A, B):
    rows = len(A)
    cols = len(A[0])
    
	result = [[0.0] * cols for _ in range(rows)]
    for i in range(rows):
    	for j in range(cols):
            result[i][j] = A[i][j] * B[i][j]
    return result
    