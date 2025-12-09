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

class HumanAgent(Agent):
	def play(self, board):
		print("enter a (x, y)")
		input_str = input()
		new_list = input_str.split()
		x = int(new_list[0])
		y = int(new_list[1])
		return (x, y)

if __name__ == "__main__":
	n = 3
	game = TicTacToe(n)
	player1 = RandomAgent()
	player2 = HumanAgent()
	user_choice = []
	while True:
		if game.state != State.PLAYING:
			if game.state == State.DRAW:
				print("it's a DRAW\n")
			if game.state == State.WON:
				print(f"Player{game.winner} won!\n")
			break
		elif game.next == Player.X:
			user_choice = player1.play(game.board)
			game.play(Player.X, user_choice[0], user_choice[1])
			print("computer's choice")
			game.print_board()
			print("\n")
		elif game.next == Player.O:
			user_choice = player2.play(game.board)
			game.play(Player.O, user_choice[0], user_choice[1])
			print("user's choice")
			game.print_board()