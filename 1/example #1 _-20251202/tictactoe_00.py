#!/usr/bin/env python3
"""
課題 #1.1
n 目並べのクラスを実装してください。
"""

# TicTacToe クラスの実装
class TicTacToe:
	"""	N x N TicTacToe クラス. 1st player: o, 2nd player: x
	
	Args:
		n (int): ボードサイズ (デフォルト 3)
	
	Attributes:
		  size (int) : ボードサイズ
		  next (int) : 次のプレイヤーID
		 board (list): ボードの状態
		 state (int) : ゲームの状態
		winner (int) : 勝者のプレイヤーID（勝負があった場合）
		 judge (dict): 判定結果
	
	Methods:
		play(player:int, x:int, y:int):
			一手進める。
			player: プレイヤーID 1/2
			  x, y: セルのアドレス (左上が [0, 0])
		play(player:int, idx:int):
			一手進める。
			player: プレイヤーID 1/2
			   idx: セルのインデックス (左上が0)
		print_board(stat:bool=False):
			現在の盤面を表示する。
			  stat: Trueであれば、判定結果も表示する。
		is_vacant(x:int, y:int):
		is_vacant(idx:int):
			セルが空白であれば、True を返す。
	"""
	
	Mark = ' ox'
	
	
	# 初期化
	def __new__(cls, n:int=3):
		# 引数チェック
		if type(n) != int:
			raise TypeError('board size must be an integer')
		
		if n < 3:
			raise ValueError('minimum board size is 3')
		
		return super().__new__(cls)
	
	
	def __init__(self, n:int=3):
		self.__size   = n
		self.__next   = 1
		self.__board  = [0 for _ in range(self.size * self.size)]
		self.__state  = 0	# game is on going
		self.__winner = None
		self.__judge  = { 0: [0] * self.size,	# 垂直方向
						  1: [0] * self.size,	# 水平方向
						  2: [0, 0]}			# 斜め方向
	
	@property
	def size(self):
		"""	ボードサイズ	"""
		return self.__size
	
	@size.setter
	def size(self, *args):
		raise PermissionError("You CAN'T change the board!!")
		
	@property
	def next(self):
		"""	次のプレイヤー: 1 or 2		"""
		return self.__next
	
	@next.setter
	def next(self, *args):
		raise PermissionError("No, no, no!! You CAN'T change the turn!!")
	
	@property
	def board(self):
		"""	ボードの状態を返す。
			0: 空,  1, 2: それぞれのプレイヤーが選択したセル
		"""
		return [int(cell) for cell in self.__board]
		
	@board.setter
	def board(self, *args):
		raise PermissionError("You CAN'T change the board!!")
	
	@property
	def judge(self):
		"""	盤面の判定結果を保持する。
			judge[DIR][POS]
			DIR: 0: 垂直方向の各線の状態 [n]
					 POS: 0, ..., n-1
				 1: 水平方向の各線の状態 [n]
					 POS: 0, ..., n-1
				 2: 斜め方向の各線の状態 [2]
					 POS: 0: 左上から右下方向 \
						  1: 右上から左下方向 /
			VAL: 0: 未定		o o
				 1: 引分		o x
				 2: 勝負あり	ooo
		"""
		return self.__judge
		
	@judge.setter
	def judge(self, *args):
		raise PermissionError("You CAN'T change the board state!!")
	
	@property
	def state(self):
		"""	ゲームの状態: 0: 進行中
		                1: 引き分け
		                2: 勝負あり
		"""
		return self.__state
		
	@state.setter
	def state(self, *args):
		raise PermissionError("You CAN'T change the game state!!")
	
	@property
	def winner(self):
		"""	ゲームの勝者: None, 1 or 2	"""
		return self.__winner
		
	@winner.setter
	def winner(self, *args):
		raise PermissionError("You CAN'T change the WINNER!!")
	
	
	def play(self, player:int, x:int, y:int=None):
		"""	ゲームを一手進める。
		
		Args:
			player: プレイヤーID 1/2
			  x, y: セルのアドレス (左上が [0, 0]), もしくはインデックス (左上が0)
		Returns:
			ゲームの状態と勝者 ID (勝敗が決した場合)
		Raises:
			PermissionError: プレイヤーIDが不適切、空いていないセルを指定した。
			IndexError: セルの指定が範囲外。
		"""
		# 諸々チェック
		if self.state != 0:
			raise PermissionError('GAME IS OVER!!')
			
		if not player in [1, 2]:	# プレイヤーIDが変
			raise PermissionError('you are NOT a player.')
		
		if player != self.__next:			# プレイヤーが違う
			raise PermissionError(f'next turn is player {self.__next}')
		
		if not y:	# インデックスをアドレスに
			y = x // self.size
			x %= self.size
		
		if (not x in range(self.size)) or (not y in range(self.size)):	# アドレスが範囲外
			raise IndexError(f'({x}, {y}) is out of range.')
		
		if not self.is_vacant(x, y):	# セルが空ではない
			raise PermissionError(f'({x}, {y}) is NOT vacant.')
		
		# play
		self.__board[x + y * self.size] = player
		
		# 判定
		ret = self._judge()
		
		# ゲームの状態の更新
		if self.state == 0:
			self.__next = 2 - ((self.__next + 1) & 1)
		else:
			self.__next = None
		
		return ret
	
	def is_vacant(self, x:int, y:int=None):
		"""	盤上の空きを確認。
		
		Args:
			x, y: セルのアドレス (左上が [0, 0]), もしくはインデックス (左上が 0)
		Returns:
			セルが空であれば True、それ以外は False。
		Raises:
			None
		"""
		if not y:	# インデックスをアドレスに
			y = x // self.size
			x %= self.size
		
		if self.state == 0:
			return self.board[x + y * self.size] == 0
		else:
			False
	
	def print_board(self, stat:bool=False):
		""" 現在の盤面の状態をターミナルに出力する。
		
		Args:
			stat: True なら、判定結果も出力する。
		Returns:
			None
		Raises:
			None
		"""
		pad = 4		# MUST BE > 2
		hdiv = ' ' * pad + '+---' * self.size + '+'
		
		print()
		
		if stat:
			print(' ' * (pad - 2), end='')
			print('%d' % self.judge[2][0], end='')
			for x in range(self.size):
				print('   %d' % self.judge[0][x], end='')
			print('   %d' % self.judge[2][1])
			
		for y in range(self.size):
			print(hdiv)
			print(' ' * pad + '|', end='')
			for x in range(self.size):
				print(' %.1s |' % self.Mark[self.board[x + y * self.size]], end='')
			if stat:
				print(' %d' % self.judge[1][y], end='')
			print()
		print(hdiv)
		print()
	
	def _judge(self):
		"""	現在の盤面の状態を評価し判定する。
		play() から呼びだされ、結果は judge, state, winner に保存されるため、明示的に呼び出す必要は無い。
		
		Args:
			None
		Returns:
			ゲームの状態と勝者 ID (勝敗が決した場合)
		Raises:
			None
		"""
		
		if self.state == 0:	# ゲーム終了後は判定しない
			# 各方向のチェック用にサブルーチンを定義
			def check_linestate_hz(direction:int):
				"""	水平/垂直方向のチェック用サブルーチン。結果は judge に保存される。
				
				Args:
					direction: 方向。0=垂直方向、2=水平方向
				Returns:
					None
				Raises:
					None
				"""
				for p0 in range(self.size):
					if self.judge[direction][p0] == 0:	# ラインの状態が未確定
						s1 = s2 = 0
						
						for p1 in range(self.size):
							if direction == 0:	# 垂直方向
								x = p0;	y = p1
							else:				# 水平方向
								x = p1;	y = p0
							
							c = self.board[x + y * self.size]
							if   c == 1:	s1 += 1
							elif c == 2:	s2 += 1
						
						if s1 and s2:
							self.__judge[direction][p0] = 1	# 引き分け
						elif s1 == self.size:
							self.__judge[direction][p0] = 2	# 勝負あり
							self.__state  = 2	# game over
							self.__winner = 1
						elif s2 == self.size:
							self.__judge[direction][p0] = 2	# 勝負あり
							self.__state  = 2	# game over
							self.__winner = 2
			
			# 斜め方向のチェック用サブルーチン
			def check_linestate_x(direction:int):
				"""	斜め方向のチェック用サブルーチン。結果は judge に保存される。
				
				Args:
					direction: 方向。0=左上から右下 \、1=右上から左下 /
				Returns:
					None
				Raises:
					None
				"""
				if self.judge[2][direction] == 0:	# ラインの状態が未確定
					s1 = s2 = 0
				
					for x in range(self.size):
						if direction == 0:	# \
							y = x
						else:				# /
							y = self.size - x - 1
						
						c = self.board[x + y * self.size]
						if   c == 1:	s1 += 1
						elif c == 2:	s2 += 1
				
					if s1 and s2:
						self.__judge[2][direction] = 1	# 引き分け
					elif s1 == self.size:
						self.__judge[2][direction] = 2	# 勝負あり
						self.__state  = 2	# game over
						self.__winner = 1
					elif s2 == self.size:
						self.__judge[2][direction] = 2	# 勝負あり
						self.__state  = 2	# game over
						self.__winner = 2
			
			
			# 各方向のチェック
			check_linestate_hz(0)	# 垂直方向
			check_linestate_hz(1)	# 水平方向
			check_linestate_x(0)	# \
			check_linestate_x(1)	# /
			
			# 引き分けのチェック - 全てのラインが引き分けなら、ゲームも引き分け
			if  self.judge[2][0] == 1 \
			and self.judge[2][1] == 1:					# 斜め方向
				for p in range(self.size):
					if self.judge[0][p] != 1:	break	# 垂直方向
					if self.judge[1][p] != 1:	break	# 水平方向
				else:
					self.__state = 1	# 引き分け
		
		return self.__state, self.__winner




if __name__ == '__main__':
	# テスト用コード
	from random import randint
	
	n = 3
	
	while n >= 3:
		game = TicTacToe(n)
		nn = n**2
		
		for i in range(nn):
			e = [idx for idx, val in enumerate(game.board) if val==0]
			c = e[randint(0, len(e)-1)]
			print(f'#{i+1}: {TicTacToe.Mark[game.next]} = {c+1}')
		
			game.play(game.next, c)
			game.print_board(stat=True)
	
			if game.state == 1:
				print('Result: DRAW')
				break
			elif game.state == 2:
				print('Result: Player %d (%.1s) WON' % (game.winner, TicTacToe.Mark[game.winner]))
				break
			
		while True:
			try:
				n = int(input('\n次は何目並べにしますか?（3未満で終了）: '))
				break
			except:
				print('整数を入力してください。')
			
