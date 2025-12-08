import random

class TicTacToe:
	def __init__(self, size):
		self.__size = size
		self.__next = 1
		self.__board = [[0] * size for _ in range(size)]
		self.__state = 0
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
		if not (0 <= x <self.size) or not (0 <= y < self.size):
			return 0
		if not self.__board[x][y] == 0:
			return 0
		if not player == self.__next:
			return 0
		if not self.state == 0:
			return 0
		self.__board[x][y] = player
		if self.__next == 1:
			self.__next = 2
		elif self.__next == 2:
			self.__next = 1
		self.__count += 1
		self.check_winner(x, y)

	def check_winner(self, x, y):
		player = self.__board[x][y]
		n = self.size
		if all(self.__board[x][c] == player for c in range(n)):
			self.__winner = player
			self.__state = 2
			self.__next = None
			return player
		if all(self.__board[r][y] == player for r in range(n)):
			self.__winner = player
			self.__state = 2
			self.__next = None
			return player
		if x == y:
			if all(self.__board[i][i] == player for i in range(n)):
				self.__winner = player
				self.__state = 2
				self.__next = None
				return player
		if x + y == n - 1:
			if all(self.__board[i][n - i - 1] == player for i in range(n)):
				self.__winner = player
				self.__state = 2
				self.__next = None
				return player
		if self.__count == n * n:
			self.__state = 1
			self.__next = None
			return 0
		
	def print_board(self):
		for row in self.__board:
			print(row)
			
		
if __name__ == "__main__":
	n = 10
	game = TicTacToe(n)
	for i in range(n * n):
		if game.state != 0:
			break
		x = random.randint(0, n - 1)
		y = random.randint(0, n - 1)
		print(f"Player {game.next}'s turn ({x}, {y})")
		game.play(game.next, x, y)
		game.print_board()
		print("-----")
