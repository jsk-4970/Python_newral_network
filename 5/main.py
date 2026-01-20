#!/usr/bin/env python3
"""
実行結果:
=== 3層ネットワーク (入力3 -> 中間4 -> 出力2) ===
入力: [1.0, 2.0, 3.0]
出力: [-0.00586487744949979, 0.005139314168384684]

=== 4層ネットワーク (2 -> 4 -> 4 -> 1) ===
入力: [0.5, -0.5]
出力: [1.4081562591426649e-06]

=== 活性化関数の比較 ===
入力:    [-2.0, -1.0, 0.0, 1.0, 2.0]
Sigmoid: [0.4864, 0.506, 0.4983, 0.505, 0.4904]
ReLU:    [0.0038, 0.0348, 0.0, 0.0, 0.0]
"""

from network import Network
from layers import Dense
from activations import Sigmoid, ReLU


def main():
    # PDFの例と同じ構成: 入力層3, 中間層4, 出力層2
    print("=== 3層ネットワーク (入力3 -> 中間4 -> 出力2) ===")
    net = Network()
    net.add(Dense(3, 4, Sigmoid()))
    net.add(Dense(4, 2))

    x = [[1.0, 2.0, 3.0]]
    y = net.predict(x)
    print(f"入力: {x[0]}")
    print(f"出力: {y[0]}")
    print()

    # 層数を変えてみる: 4層ネットワーク
    print("=== 4層ネットワーク (2 -> 4 -> 4 -> 1) ===")
    net2 = Network()
    net2.add(Dense(2, 4, ReLU()))
    net2.add(Dense(4, 4, ReLU()))
    net2.add(Dense(4, 1))

    x2 = [[0.5, -0.5]]
    y2 = net2.predict(x2)
    print(f"入力: {x2[0]}")
    print(f"出力: {y2[0]}")
    print()

    # 活性化関数を変えてみる
    print("=== 活性化関数の比較 ===")
    x3 = [[-2.0, -1.0, 0.0, 1.0, 2.0]]

    net_sigmoid = Network()
    net_sigmoid.add(Dense(5, 5, Sigmoid()))
    y_sigmoid = net_sigmoid.predict(x3)

    net_relu = Network()
    net_relu.add(Dense(5, 5, ReLU()))
    y_relu = net_relu.predict(x3)

    print(f"入力:    {x3[0]}")
    print(f"Sigmoid: {[round(v, 4) for v in y_sigmoid[0]]}")
    print(f"ReLU:    {[round(v, 4) for v in y_relu[0]]}")


if __name__ == "__main__":
    main()
