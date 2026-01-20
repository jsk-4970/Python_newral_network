#!/usr/bin/env python3
import random
from matrix import mat_mul, mat_add
from activations import Linear


class Dense:
    def __init__(self, n_in, n_out, activation=None):
        # ウェイト: 小さいランダム値で初期化
        self.W = [[random.gauss(0, 0.01) for _ in range(n_out)]
                  for _ in range(n_in)]
        # バイアス: 0で初期化
        self.b = [[0.0] * n_out]
        # 活性化関数
        self.act = activation if activation else Linear()

    def forward(self, x):
        # バックプロパゲーション用に保存
        self.x = x
        self.z = mat_add(mat_mul(x, self.W), self.b)
        self.y = self.act(self.z)
        return self.y
    
    def backward(self, DL_dy):
        dL_dz = dL_dy @ act.deriv(z)