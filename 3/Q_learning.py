#!/usr/bin/env python3
"""
TicTacToe Q学習エージェント
課題 #3: Q学習エージェントの実装とランダムエージェントとの対戦

結果（各10万回対戦）:
============================================================
【対戦ルール1】先手:ランダム、後手:Q学習エージェント
  - 最終結果: Q学習勝利: 72.65%, 引き分け: 13.18%, ランダム勝利: 14.16%
  - 学習推移: 1万回目 60.2% → 5万回目 74.1% → 10万回目 75.3%
  - 後手不利にも関わらず、学習により70%以上の勝率を達成

【対戦ルール2】先手:Q学習エージェント、後手:ランダム
  - 最終結果: Q学習勝利: 90.08%, 引き分け: 5.54%, ランダム勝利: 4.38%
  - 学習推移: 1万回目 84.4% → 5万回目 90.3% → 10万回目 92.1%
  - 先手の有利さ + 学習効果で90%以上の高勝率

【対戦ルール3】勝者が次の対局で後手になる
  - 最終結果: Q学習勝利: 73.87%, 引き分け: 12.46%, ランダム勝利: 13.68%
  - 学習推移: 1万回目 63.5% → 5万回目 75.9% → 10万回目 76.2%
  - 先手後手が入れ替わるため、両方の状況を学習
============================================================
"""

from TicTacToe import TicTacToe, Player, State
from Agent_vs_Agent import Agent, RandomAgent
import random


class QLearningAgent(Agent):
    """
    Q学習エージェント
    - alpha: 学習率 (0 < alpha <= 1)
    - gamma: 割引率 (0 <= gamma <= 1)
    - epsilon: 探索率 (ε-greedy法)
    """

    def __init__(self, alpha=0.3, gamma=0.9, epsilon=0.2):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.history = []  # (state, action)の履歴を保存

    def get_state_key(self, board):
        """盤面をハッシュ可能なタプルに変換"""
        return tuple(tuple(cell for cell in row) for row in board)

    def get_available_actions(self, board):
        """利用可能なアクション（空きマス）を取得"""
        actions = []
        n = len(board)
        for x in range(n):
            for y in range(n):
                if board[x][y] == Player.EMPTY:
                    actions.append((x, y))
        return actions

    def get_q_value(self, state, action):
        """Q値を取得（未登録なら0）"""
        if state not in self.q_table:
            return 0.0
        return self.q_table[state].get(action, 0.0)

    def set_q_value(self, state, action, value):
        """Q値を設定"""
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = value

    def play(self, board):
        """
        次の手を決定
        - epsilon の確率でランダムに探索
        - それ以外は最大Q値の行動を選択
        """
        actions = self.get_available_actions(board)
        if not actions:
            return None

        state = self.get_state_key(board)

        # ε-greedy法
        if random.random() < self.epsilon:
            action = random.choice(actions)
        else:
            # 最大Q値の行動を選択（同じQ値なら最初に見つかったものを選択）
            best_action = actions[0]
            best_q = self.get_q_value(state, actions[0])
            for action in actions[1:]:
                q = self.get_q_value(state, action)
                if q > best_q:
                    best_q = q
                    best_action = action
            action = best_action

        # 履歴に追加
        self.history.append((state, action))
        return action

    def update_from_result(self, reward):
        """
        ゲーム終了時に履歴を使ってQ値を更新
        - 終端状態から遡って更新（TD学習）
        """
        # 逆順に履歴を処理
        next_max_q = 0.0
        for state, action in reversed(self.history):
            current_q = self.get_q_value(state, action)
            # Q学習の更新式: Q(s,a) = Q(s,a) + α * (r + γ * max_a' Q(s',a') - Q(s,a))
            new_q = current_q + self.alpha * (reward + self.gamma * next_max_q - current_q)
            self.set_q_value(state, action, new_q)

            # 次の状態の最大Q値を現在の状態の行動のQ値に設定
            next_max_q = new_q
            # 報酬は終端状態でのみ与える（中間ステップは0）
            reward = 0.0

        # 履歴をクリア
        self.history = []

    def clear_history(self):
        """履歴をクリア"""
        self.history = []


def run_experiment_rule1(num_trials=100000, report_interval=10000):
    """
    対戦ルール1: 先手後手固定
    先手:ランダムエージェント、後手:Q学習エージェント
    """
    print("=" * 60)
    print("【対戦ルール1】先手:ランダム、後手:Q学習エージェント")
    print("=" * 60)

    n = 3
    q_agent = QLearningAgent(alpha=0.3, gamma=0.9, epsilon=0.2)
    random_agent = RandomAgent()

    q_wins = 0
    random_wins = 0
    draws = 0

    # 区間ごとの統計
    interval_q_wins = 0
    interval_random_wins = 0
    interval_draws = 0

    for trial in range(num_trials):
        game = TicTacToe(n)
        q_agent.clear_history()

        while game.state == State.PLAYING:
            if game.next == Player.X:
                # 先手: ランダムエージェント
                choice = random_agent.play(game.board)
                if choice:
                    game.play(Player.X, choice[0], choice[1])
            else:
                # 後手: Q学習エージェント
                choice = q_agent.play(game.board)
                if choice:
                    game.play(Player.O, choice[0], choice[1])

        # 結果の記録と学習
        if game.state == State.WON:
            if game.winner == Player.O:
                q_wins += 1
                interval_q_wins += 1
                q_agent.update_from_result(1.0)  # 勝利報酬
            else:
                random_wins += 1
                interval_random_wins += 1
                q_agent.update_from_result(-1.0)  # 敗北ペナルティ
        else:
            draws += 1
            interval_draws += 1
            q_agent.update_from_result(0.2)  # 引き分けは小さな正の報酬

        # 進捗表示
        if (trial + 1) % report_interval == 0:
            total = interval_q_wins + interval_random_wins + interval_draws
            print(f"{trial + 1:>6}回: Q学習勝利={interval_q_wins/total*100:5.1f}%, "
                  f"引き分け={interval_draws/total*100:5.1f}%, "
                  f"ランダム勝利={interval_random_wins/total*100:5.1f}%")
            interval_q_wins = 0
            interval_random_wins = 0
            interval_draws = 0

    print("-" * 60)
    print(f"最終結果 ({num_trials}回):")
    print(f"  Q学習勝利: {q_wins}回 ({q_wins/num_trials*100:.2f}%)")
    print(f"  引き分け: {draws}回 ({draws/num_trials*100:.2f}%)")
    print(f"  ランダム勝利: {random_wins}回 ({random_wins/num_trials*100:.2f}%)")
    print()

    return q_wins, draws, random_wins


def run_experiment_rule2(num_trials=100000, report_interval=10000):
    """
    対戦ルール2: 先手後手固定
    先手:Q学習エージェント、後手:ランダムエージェント
    """
    print("=" * 60)
    print("【対戦ルール2】先手:Q学習エージェント、後手:ランダム")
    print("=" * 60)

    n = 3
    q_agent = QLearningAgent(alpha=0.3, gamma=0.9, epsilon=0.2)
    random_agent = RandomAgent()

    q_wins = 0
    random_wins = 0
    draws = 0

    interval_q_wins = 0
    interval_random_wins = 0
    interval_draws = 0

    for trial in range(num_trials):
        game = TicTacToe(n)
        q_agent.clear_history()

        while game.state == State.PLAYING:
            if game.next == Player.X:
                # 先手: Q学習エージェント
                choice = q_agent.play(game.board)
                if choice:
                    game.play(Player.X, choice[0], choice[1])
            else:
                # 後手: ランダムエージェント
                choice = random_agent.play(game.board)
                if choice:
                    game.play(Player.O, choice[0], choice[1])

        # 結果の記録と学習
        if game.state == State.WON:
            if game.winner == Player.X:
                q_wins += 1
                interval_q_wins += 1
                q_agent.update_from_result(1.0)
            else:
                random_wins += 1
                interval_random_wins += 1
                q_agent.update_from_result(-1.0)
        else:
            draws += 1
            interval_draws += 1
            q_agent.update_from_result(0.2)

        if (trial + 1) % report_interval == 0:
            total = interval_q_wins + interval_random_wins + interval_draws
            print(f"{trial + 1:>6}回: Q学習勝利={interval_q_wins/total*100:5.1f}%, "
                  f"引き分け={interval_draws/total*100:5.1f}%, "
                  f"ランダム勝利={interval_random_wins/total*100:5.1f}%")
            interval_q_wins = 0
            interval_random_wins = 0
            interval_draws = 0

    print("-" * 60)
    print(f"最終結果 ({num_trials}回):")
    print(f"  Q学習勝利: {q_wins}回 ({q_wins/num_trials*100:.2f}%)")
    print(f"  引き分け: {draws}回 ({draws/num_trials*100:.2f}%)")
    print(f"  ランダム勝利: {random_wins}回 ({random_wins/num_trials*100:.2f}%)")
    print()

    return q_wins, draws, random_wins


def run_experiment_rule3(num_trials=100000, report_interval=10000):
    """
    対戦ルール3: 勝者が次の対局で後手になる
    初戦はQ学習エージェントが先手
    """
    print("=" * 60)
    print("【対戦ルール3】勝者が次の対局で後手になる")
    print("=" * 60)

    n = 3
    q_agent = QLearningAgent(alpha=0.3, gamma=0.9, epsilon=0.2)
    random_agent = RandomAgent()

    q_wins = 0
    random_wins = 0
    draws = 0

    interval_q_wins = 0
    interval_random_wins = 0
    interval_draws = 0

    # Q学習エージェントが先手かどうか (初戦は先手)
    q_is_first = True

    for trial in range(num_trials):
        game = TicTacToe(n)
        q_agent.clear_history()

        if q_is_first:
            q_player = Player.X
            random_player = Player.O
        else:
            q_player = Player.O
            random_player = Player.X

        while game.state == State.PLAYING:
            if game.next == q_player:
                choice = q_agent.play(game.board)
                if choice:
                    game.play(q_player, choice[0], choice[1])
            else:
                choice = random_agent.play(game.board)
                if choice:
                    game.play(random_player, choice[0], choice[1])

        # 結果の記録と学習、次の先手後手の決定
        if game.state == State.WON:
            if game.winner == q_player:
                q_wins += 1
                interval_q_wins += 1
                q_agent.update_from_result(1.0)
                q_is_first = False  # Q学習が勝ったので次は後手
            else:
                random_wins += 1
                interval_random_wins += 1
                q_agent.update_from_result(-1.0)
                q_is_first = True  # ランダムが勝ったのでQ学習は次は先手
        else:
            draws += 1
            interval_draws += 1
            q_agent.update_from_result(0.2)
            # 引き分けの場合は先手後手を維持

        if (trial + 1) % report_interval == 0:
            total = interval_q_wins + interval_random_wins + interval_draws
            print(f"{trial + 1:>6}回: Q学習勝利={interval_q_wins/total*100:5.1f}%, "
                  f"引き分け={interval_draws/total*100:5.1f}%, "
                  f"ランダム勝利={interval_random_wins/total*100:5.1f}%")
            interval_q_wins = 0
            interval_random_wins = 0
            interval_draws = 0

    print("-" * 60)
    print(f"最終結果 ({num_trials}回):")
    print(f"  Q学習勝利: {q_wins}回 ({q_wins/num_trials*100:.2f}%)")
    print(f"  引き分け: {draws}回 ({draws/num_trials*100:.2f}%)")
    print(f"  ランダム勝利: {random_wins}回 ({random_wins/num_trials*100:.2f}%)")
    print()

    return q_wins, draws, random_wins


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TicTacToe Q学習エージェント vs ランダムエージェント")
    print("各ルールで10万回対戦を行い、学習の推移を観察")
    print("=" * 60 + "\n")

    # 対戦回数
    num_trials = 100000
    report_interval = 10000

    # 各ルールで実験を実行
    run_experiment_rule1(num_trials, report_interval)
    run_experiment_rule2(num_trials, report_interval)
    run_experiment_rule3(num_trials, report_interval)

    print("=" * 60)
    print("全ての実験が完了しました")
    print("=" * 60)


"""
============================================================
実行結果:

【対戦ルール1】先手:ランダム、後手:Q学習エージェント
============================================================
 10000回: Q学習勝利= 60.2%, 引き分け= 16.1%, ランダム勝利= 23.8%
 20000回: Q学習勝利= 71.0%, 引き分け= 13.7%, ランダム勝利= 15.3%
 30000回: Q学習勝利= 72.7%, 引き分け= 14.1%, ランダム勝利= 13.2%
 40000回: Q学習勝利= 73.3%, 引き分け= 13.5%, ランダム勝利= 13.2%
 50000回: Q学習勝利= 74.1%, 引き分け= 13.1%, ランダム勝利= 12.8%
 60000回: Q学習勝利= 74.7%, 引き分け= 13.0%, ランダム勝利= 12.3%
 70000回: Q学習勝利= 75.0%, 引き分け= 12.3%, ランダム勝利= 12.7%
 80000回: Q学習勝利= 75.1%, 引き分け= 12.3%, ランダム勝利= 12.7%
 90000回: Q学習勝利= 75.2%, 引き分け= 11.8%, ランダム勝利= 13.1%
100000回: Q学習勝利= 75.3%, 引き分け= 12.0%, ランダム勝利= 12.7%
最終結果: Q学習勝利: 72.65%, 引き分け: 13.18%, ランダム勝利: 14.16%

考察:
- 後手は不利だが、Q学習により70%以上の勝率を達成
- 学習初期は勝率60%程度だが、2万回目で71%に急上昇
- 約5万回程度で収束傾向（75%前後で安定）

============================================================
【対戦ルール2】先手:Q学習エージェント、後手:ランダム
============================================================
 10000回: Q学習勝利= 84.4%, 引き分け=  7.8%, ランダム勝利=  7.7%
 20000回: Q学習勝利= 88.6%, 引き分け=  6.2%, ランダム勝利=  5.2%
 30000回: Q学習勝利= 89.6%, 引き分け=  5.9%, ランダム勝利=  4.5%
 40000回: Q学習勝利= 90.7%, 引き分け=  5.4%, ランダム勝利=  3.8%
 50000回: Q学習勝利= 90.3%, 引き分け=  5.5%, ランダム勝利=  4.2%
 60000回: Q学習勝利= 91.2%, 引き分け=  5.2%, ランダム勝利=  3.6%
 70000回: Q学習勝利= 91.2%, 引き分け=  5.3%, ランダム勝利=  3.6%
 80000回: Q学習勝利= 91.2%, 引き分け=  4.9%, ランダム勝利=  3.9%
 90000回: Q学習勝利= 91.5%, 引き分け=  4.8%, ランダム勝利=  3.7%
100000回: Q学習勝利= 92.1%, 引き分け=  4.4%, ランダム勝利=  3.5%
最終結果: Q学習勝利: 90.08%, 引き分け: 5.54%, ランダム勝利: 4.38%

考察:
- 先手の有利さ + 学習効果で90%以上の高勝率
- ランダムvs.ランダムの先手勝率(約58%)と比較して大幅に向上
- 学習初期から84%と高い勝率を示し、さらに90%超まで向上

============================================================
【対戦ルール3】勝者が次の対局で後手になる
============================================================
 10000回: Q学習勝利= 63.5%, 引き分け= 14.0%, ランダム勝利= 22.4%
 20000回: Q学習勝利= 71.6%, 引き分け= 13.4%, ランダム勝利= 15.1%
 30000回: Q学習勝利= 73.5%, 引き分け= 12.8%, ランダム勝利= 13.7%
 40000回: Q学習勝利= 75.1%, 引き分け= 12.4%, ランダム勝利= 12.5%
 50000回: Q学習勝利= 75.9%, 引き分け= 12.2%, ランダム勝利= 11.9%
 60000回: Q学習勝利= 75.7%, 引き分け= 12.0%, ランダム勝利= 12.3%
 70000回: Q学習勝利= 76.0%, 引き分け= 11.7%, ランダム勝利= 12.3%
 80000回: Q学習勝利= 75.1%, 引き分け= 12.3%, ランダム勝利= 12.6%
 90000回: Q学習勝利= 76.1%, 引き分け= 11.7%, ランダム勝利= 12.2%
100000回: Q学習勝利= 76.2%, 引き分け= 12.0%, ランダム勝利= 11.8%
最終結果: Q学習勝利: 73.87%, 引き分け: 12.46%, ランダム勝利: 13.68%

考察:
- 先手後手両方の状況で学習できる
- ルール1に近い結果（勝つと後手になるため）
- 勝利すると後手になるため、後手での強さが重要
- 5万回程度で76%前後に収束
============================================================

総合考察:
1. Q学習エージェントは未学習状態から対戦を始めても、
   数万回の対戦で十分に学習し、高い勝率を達成する
2. 先手の方が有利（ルール2: 90% > ルール3: 74% ≈ ルール1: 73%）
3. 学習の収束は約3-5万回程度で安定する傾向
4. ε-greedy法(ε=0.2)による探索と活用のバランスが重要
5. 引き分け率は12-13%程度で安定（完全な学習では引き分けに持ち込む戦略も学習）
"""
