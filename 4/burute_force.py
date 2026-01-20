#!/usr/bin/env python3

from itertools import combinations


def idx_to_xy(idx, n):
	return (idx // n, idx % n)
	
def xy_to_idx(x, y, n):
	return (x * n + y)

def rotate_90(x, y, n):
	return (y, n - 1 - x)

def rotate_180(x, y, n):
	return (n - 1 - x, n - 1 - y)

def rotate_270(x, y, n):
	return (n - 1 - y, x)

def flip_h(x, y, n):
	return (n - 1 - x, y)

def flip_v(x, y, n):
	return (x, n - 1 - y)

def flip_diag_main(x, y, n):
	return (y, x)

def flip_diag_anti(x, y, n):
	return (n - 1 - y, n - 1 - x)

def transform_board(board, n, coord_transform):
	new_board = [0] * (n * n)

	for i in range(n * n):
		x, y = idx_to_xy(i, n)
		nx, ny = coord_transform(x, y, n)
		new_idx = xy_to_idx(nx, ny, n)
		new_board[new_idx] = board[i]

	return (tuple(new_board))

def canonical(board, n):
	all_transforms = [
		board,
		transform_board(board, n, rotate_90),
		transform_board(board, n, rotate_180),
		transform_board(board, n, rotate_270),
		transform_board(board, n, flip_h),
		transform_board(board, n, flip_v),
		transform_board(board, n, flip_diag_main),
		transform_board(board, n, flip_diag_anti)
	]
	return min(all_transforms)


def count_patterns(n, num_o, num_x):
	"""○がnum_o個、×がnum_x個の局面のユニークパターン数を数える"""
	positions = list(range(n * n))
	unique = set()

	for o_positions in combinations(positions, num_o):
		remaining = [p for p in positions if p not in o_positions]
		for x_positions in combinations(remaining, num_x):
			board = [0] * (n * n)
			for p in o_positions:
				board[p] = 1
			for p in x_positions:
				board[p] = 2
			board = tuple(board)
			unique.add(canonical(board, n))

	return len(unique)


if __name__ == "__main__":
	n = 3
	total = 0

	print(f"n = {n} の各手数のユニークパターン数:")
	print("-" * 30)

	# 0手目（空の盤面）
	print(f"手数 0: 1")
	total += 1

	# 1手目〜n²手目
	for move in range(1, n * n + 1):
		num_o = (move + 1) // 2  # ○の数（先手）
		num_x = move // 2        # ×の数（後手）
		count = count_patterns(n, num_o, num_x)
		print(f"手数 {move}: {count}")
		total += count

	print("-" * 30)
	print(f"合計: {total}")


# ========================================
# 実行結果 (n=3)
# ========================================
# 手数 0: 1
# 手数 1: 3
# 手数 2: 12
# 手数 3: 38
# 手数 4: 108
# 手数 5: 174
# 手数 6: 228
# 手数 7: 174
# 手数 8: 89
# 手数 9: 23
# ------------------------------
# 合計: 850
