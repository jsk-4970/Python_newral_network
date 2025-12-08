from enum import Enum, auto
import random

class Player(Enum):
	EMPTY = 0
	X = 1
	O = 2

	def __str__(self):
		if self == Player.EMPTY:
			return "."
		return self.name

class State(Enum):
	PLAYING = 0
	DRAW = 1
	WON = 2

class TicTacToe:
	def __init__(self, size):
		self.__size = size
		self.__next = Player.X
		self.__board = [[Player.EMPTY] * size for _ in range(size)]
		self.__state = State.PLAYING
		self.__winner = None
		self.__count = 0

	@property
	def size(self):
		return self.__size

	@property
	def next(self):
		return self.__next

	@property
	def board(self):
		return self.__board

	@property
	def state(self):
		return self.__state

	@property
	def winner(self):
		return self.__winner
	
	@property
	def count(self):
		return self.__count

	def play(self, player, x, y):
		if not (0 <= x < self.size) or not (0 <= y < self.size):
			return False
		if not self.__board[x][y] == Player.EMPTY:
			return False
		if not player == self.__next:
			return False
		if not self.state == State.PLAYING:
			return False
		self.__board[x][y] = player
		if self.__next == Player.X:
			self.__next = Player.O
		elif self.__next == Player.O:
			self.__next = Player.X
		self.__count += 1
		self.check_winner(x, y)
		return True

	def check_winner(self, x, y):
		player = self.__board[x][y]
		n = self.size
		if all(self.__board[x][c] == player for c in range(n)):
			self.__winner = player
			self.__state = State.WON
			self.__next = None
			return player
		if all(self.__board[r][y] == player for r in range(n)):
			self.__winner = player
			self.__state = State.WON
			self.__next = None
			return player
		if x == y:
			if all(self.__board[i][i] == player for i in range(n)):
				self.__winner = player
				self.__state = State.WON
				self.__next = None
				return player
		if x + y == n - 1:
			if all(self.__board[i][n - i - 1] == player for i in range(n)):
				self.__winner = player
				self.__state = State.WON
				self.__next = None
				return player
		if self.__count == n * n:
			self.__state = State.DRAW
			self.__next = None
			return 0
		
	def print_board(self):
		for row in self.__board:
			print(' '.join(str(cell) for cell in row))
			
		
if __name__ == "__main__":
	n = 10
	game = TicTacToe(n)
	for i in range(n * n):
		if game.state != State.PLAYING:
			break
		while True:
			x = random.randint(0, n - 1)
			y = random.randint(0, n - 1)
			current_player = game.next
			if game.play(current_player, x, y):
				print(f"Player {current_player}'s turn ({x}, {y})")
				break
		game.print_board()
		print("-----")

	if game.state == State.WON:
		print(f"Player {game.winner} won!")
	elif game.state == State.DRAW:
		print("It's a draw!")
