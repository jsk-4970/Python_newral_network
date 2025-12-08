#!/usr/bin/env python3
"""
課題 #1.2
enum モジュールを利用して TicTacToe クラスを実装してください。
"""

from enum import IntEnum

# TicTacToe クラスの実装
class TicTacToe:
	"""	N x N TicTacToe クラス. 1st player: o, 2nd player: x
	
	Args:
		n (int): ボードサイズ (デフォルト 3)
	
	Attributes:
		  size (int)      : ボードサイズ
		  next (Player)   : 次のプレイヤーID
		 board (list)     : ボードの状態
		 state (GameState): ゲームの状態
		winner (Player)   : 勝者のプレイヤーID（勝負があった場合）
		 judge (dict)     : 判定結果
	
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
	
	# enumerations
	class Player(IntEnum):
		"""	プレイヤー ID: FIRST, SECOND	"""
		FIRST  = 1
		SECOND = 2
	
	class GameState(IntEnum):
		"""	ゲームの状態: ONGOING, DRAW, OVER	"""
		ONGOING = 0
		DRAW    = 1
		OVER    = 2
	
	class CellState(IntEnum):
		"""	セルの状態: EMPTY, FIRST, SECOND	"""
		EMPTY	= 0
		FIRST	= 1		# = Player.FIRST
		SECOND	= 2		# = Player.SECOND
	
	class LineState(IntEnum):
		"""	盤上の各線の状態: PENDING, DRAW, FIXED	"""
		PENDING = 0
		DRAW    = 1
		FIXED   = 2
	
	class Direction(IntEnum):
		"""	線の向き: COLUMN, ROW, DIAGONAL	"""
		COLUMN   = 0	# vertical
		ROW      = 1	# horizontal
		DIAGONAL = 2
	
	class Diagonal(IntEnum):
		"""	斜線の向き: TL2BR, TR2BL	"""
		TL2BR = 0	# \ Top-Left to Bottom-Right
		TR2BL = 1	# / Top-Right to Bottom-Left
		
	
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
		self.__next   = self.Player.FIRST
		self.__board  = [self.CellState.EMPTY for _ in range(self.size * self.size)]
		self.__state  = self.GameState.ONGOING
		self.__winner = None
		self.__judge  = { self.Direction.COLUMN:   [self.LineState.PENDING] * self.size,
						  self.Direction.ROW:      [self.LineState.PENDING] * self.size,
						  self.Direction.DIAGONAL: [self.LineState.PENDING, self.LineState.PENDING]}
	
	@property
	def size(self):
		"""	ボードサイズ	"""
		return self.__size
	
	@size.setter
	def size(self, *args):
		raise PermissionError("You CAN'T change the board!!")
		
	@property
	def next(self):
		"""	次のプレイヤー: Player.FIRST or Player.SECOND	"""
		return self.__next
	
	@next.setter
	def next(self, *args):
		raise PermissionError("No, no, no!! You CAN'T change the turn!!")
	
	@property
	def board(self):
		"""	ボードの状態を返す。
			0: 空, Player.FIRST, Player.SECOND はそれぞれのプレイヤーが選択したセル
			ここでは整数に置換して返す。
		"""
		return [int(cell) for cell in self.__board]
		
	@board.setter
	def board(self, *args):
		raise PermissionError("You CAN'T change the board!!")
	
	@property
	def judge(self):
		"""	盤面の判定結果を保持する。
			judge[DIR][POS]
			DIR: Direction.COLUMN  : 垂直方向の各線の状態 [n]
					 POS: 0, ..., n-1
				 Direction.ROW     : 水平方向の各線の状態 [n]
					 POS: 0, ..., n-1
				 Direction.DIAGONAL: 斜め方向の各線の状態 [2]
					 POS: Diagonal.TL2BR: 左上から右下方向 \
						  Diagonal.TR2BL: 右上から左下方向 /
			VAL: LineState.PENDING: 未定		o o
				 LineState.DRAW   : 引分		o x
				 LineState.FIXED  : 勝負あり	ooo
		"""
		return self.__judge
		
	@judge.setter
	def judge(self, *args):
		raise PermissionError("You CAN'T change the board state!!")
	
	@property
	def state(self):
		"""	ゲームの状態: GameState.ONGOING: 進行中
		                GameState.DRAW: 引き分け
		                GameState.OVER: 勝負あり
		"""
		return self.__state
		
	@state.setter
	def state(self, *args):
		raise PermissionError("You CAN'T change the game state!!")
	
	@property
	def winner(self):
		"""	ゲームの勝者: None, Player.FIRST or Player.SECOND	"""
		return self.__winner
		
	@winner.setter
	def winner(self, *args):
		raise PermissionError("You CAN'T change the WINNER!!")
	
	
	def play(self, player:Player, x:int, y:int=None):
		"""	ゲームを一手進める。
		
		Args:
			player: Player.FIRST or Player.SECOND
			  x, y: セルのアドレス (左上が [0, 0]), もしくはインデックス (左上が0)
		Returns:
			ゲームの状態と勝者 ID (勝敗が決した場合)
		Raises:
			PermissionError: プレイヤーIDが不適切、空いていないセルを指定した。
			IndexError: セルの指定が範囲外。
		"""
		# 諸々チェック
		if self.state != self.GameState.ONGOING:
			raise PermissionError('GAME IS OVER!!')
			
		if not player in list(self.Player):	# プレイヤーIDが変
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
		self.__board[x + y * self.size] = self.CellState(player)
		
		# 判定
		ret = self._judge()
		
		# ゲームの状態の更新
		if self.state == self.GameState.ONGOING:
			self.__next = self.Player(2 - ((self.__next + 1) & 1))
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
		
		if self.state == self.GameState.ONGOING:
			return self.board[x + y * self.size] == self.CellState.EMPTY
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
			print('%d' % self.judge[self.Direction.DIAGONAL][self.Diagonal.TL2BR], end='')
			for x in range(self.size):
				print('   %d' % self.judge[self.Direction.COLUMN][x], end='')
			print('   %d' % self.judge[self.Direction.DIAGONAL][self.Diagonal.TR2BL])
			
		for y in range(self.size):
			print(hdiv)
			print(' ' * pad + '|', end='')
			for x in range(self.size):
				print(' %.1s |' % self.Mark[self.board[x + y * self.size]], end='')
			if stat:
				print(' %d' % self.judge[self.Direction.ROW][y], end='')
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
		
		if self.state == self.GameState.ONGOING:	# ゲーム終了後は判定しない
			# 各方向のチェック用にサブルーチンを定義
			def check_linestate_hz(direction:self.Direction):
				"""	水平/垂直方向のチェック用サブルーチン。結果は judge に保存される。
				
				Args:
					direction: 方向。Direction.COLUMN or Direction.ROW
				Returns:
					None
				Raises:
					None
				"""
				for p0 in range(self.size):
					if self.judge[direction][p0] == self.LineState.PENDING:
						s1 = s2 = 0
						
						for p1 in range(self.size):
							if direction == self.Direction.COLUMN:
								x = p0;	y = p1
							else:			   # Direction.ROW
								x = p1;	y = p0
							
							c = self.board[x + y * self.size]
							if   c == self.CellState.FIRST:  s1 += 1
							elif c == self.CellState.SECOND: s2 += 1
						
						if s1 and s2:
							self.__judge[direction][p0] = self.LineState.DRAW
						elif s1 == self.size:
							self.__judge[direction][p0] = self.LineState.FIXED
							self.__state = self.GameState.OVER
							self.__winner = self.Player.FIRST
						elif s2 == self.size:
							self.__judge[direction][p0] = self.LineState.FIXED
							self.__state = self.GameState.OVER
							self.__winner = self.Player.SECOND
			
			# 斜め方向のチェック用サブルーチン
			def check_linestate_x(direction:self.Diagonal):
				"""	斜め方向のチェック用サブルーチン。結果は judge に保存される。
				
				Args:
					direction: 方向。Diagonal.TL2BR or Diagonal.TR2BL
				Returns:
					None
				Raises:
					None
				"""
				if self.judge[self.Direction.DIAGONAL][direction] == self.LineState.PENDING:
					s1 = s2 = 0
				
					for x in range(self.size):
						if direction == self.Diagonal.TL2BR:
							y = x
						else:			   # Diagonal.TR2BL
							y = self.size - x - 1
						
						c = self.board[x + y * self.size]
						if   c == self.CellState.FIRST:  s1 += 1
						elif c == self.CellState.SECOND: s2 += 1
				
					if s1 and s2:
						self.__judge[self.Direction.DIAGONAL][direction] = self.LineState.DRAW
					elif s1 == self.size:
						self.__judge[self.Direction.DIAGONAL][direction] = self.LineState.FIXED
						self.__state = self.GameState.OVER
						self.__winner = self.Player.FIRST
					elif s2 == self.size:
						self.__judge[self.Direction.DIAGONAL][direction] = self.LineState.FIXED
						self.__state = self.GameState.OVER
						self.__winner = self.Player.SECOND
			
			
			# 各方向のチェック
			check_linestate_hz(self.Direction.COLUMN)
			check_linestate_hz(self.Direction.ROW)
			check_linestate_x(self.Diagonal.TL2BR)
			check_linestate_x(self.Diagonal.TR2BL)
			
			# 引き分けのチェック - 全てのラインが引き分けなら、ゲームも引き分け
			if  self.judge[self.Direction.DIAGONAL][self.Diagonal.TL2BR] == self.LineState.DRAW \
			and self.judge[self.Direction.DIAGONAL][self.Diagonal.TR2BL] == self.LineState.DRAW:
				for p in range(self.size):
					if self.judge[self.Direction.COLUMN][p] != self.LineState.DRAW:	break
					if self.judge[self.Direction.ROW   ][p] != self.LineState.DRAW:	break
				else:
					self.__state = self.GameState.DRAW
		
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
	
			if game.state == game.GameState.DRAW:
				print('Result: DRAW')
				break
			elif game.state == game.GameState.OVER:
				print('Result: Player %d (%.1s) WON' % (game.winner, TicTacToe.Mark[game.winner]))
				break
			
		while True:
			try:
				n = int(input('\n次は何目並べにしますか?（3未満で終了）: '))
				break
			except:
				print('整数を入力してください。')
			
