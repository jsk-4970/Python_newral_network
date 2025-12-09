#!usr/bin/env python3

from kadai12 import *
from abc import ABC, abstractmethod
import random

class Agent(ABC):
	@abstractmethod
	def play(self, board):
		pass

class RandomAgent(Agent):
	def play(self, board):
		random_choice = []
		n = len(board)
		for x in range(n):
			for y in range(n):
				if board[x][y] == Player.EMPTY:
					random_choice.append((x, y))
		if not random_choice:
			return None
		return random.choice(random_choice)

if __name__ == "__main__":
	n = 3
	num_trials = 100000

	# 統計を記録する変数
	x_wins = 0
	o_wins = 0
	draws = 0

	print(f"10万回の試行を開始します...\n")

	for trial in range(num_trials):
		game = TicTacToe(n)
		player1 = RandomAgent()
		player2 = RandomAgent()

		while True:
			if game.state != State.PLAYING:
				if game.state == State.DRAW:
					draws += 1
				elif game.state == State.WON:
					if game.winner == Player.X:
						x_wins += 1
					elif game.winner == Player.O:
						o_wins += 1
				break

			if game.next == Player.X:
				choice = player1.play(game.board)
				if choice:
					game.play(Player.X, choice[0], choice[1])
			elif game.next == Player.O:
				choice = player2.play(game.board)
				if choice:
					game.play(Player.O, choice[0], choice[1])

		# 進捗表示（1万回ごと）
		if (trial + 1) % 10000 == 0:
			print(f"{trial + 1}回完了...")

	# 結果を表示
	print("\n" + "="*50)
	print(f"試行回数: {num_trials}回")
	print("="*50)
	print(f"Player X の勝利: {x_wins}回 ({x_wins/num_trials*100:.2f}%)")
	print(f"Player O の勝利: {o_wins}回 ({o_wins/num_trials*100:.2f}%)")
	print(f"引き分け: {draws}回 ({draws/num_trials*100:.2f}%)")
	print("="*50)

