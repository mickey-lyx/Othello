import numpy as np
from config import INFINITY, WHITE, BLACK, WINNER_SCORE

def change_color(color):
    if color == BLACK:
        return WHITE
    else:
        return BLACK

# 权重矩阵
Vmap = np.array([[500, -25, 10, 5, 5, 10, -25, 500],
                    [-25, -45, 1, 1, 1, 1, -45, -25],
                    [10, 1, 3, 2, 2, 3, 1, 10],
                    [5, 1, 2, 1, 1, 2, 1, 5],
                    [5, 1, 2, 1, 1, 2, 1, 5],
                    [10, 1, 3, 2, 2, 3, 1, 10],
                    [-25, -45, 1, 1, 1, 1, -45, -25],
                    [500, -25, 10, 5, 5, 10, -25, 500]])

# 获取稳定点个数
def getstable(board, color):
    """部分稳定子： 角, 边, 八个方向都无空格
    stable[0]: 角上稳定子
    stable[1]: 边上稳定子（前提是有角）
    stable[2]: 八个方向全满的稳定子"""
    stable = [0, 0, 0]
    cond1 = [0, 0, 7, 7]
    cond2 = [0, 7, 7, 0]
    inc1 = [0, 1, 0, -1]
    inc2 = [1, 0, -1, 0]
    stop = [0, 0, 0, 0]
    for i in range(4):
        # 遍历角
        if board[cond1[i]][cond2[i]] == color:
            stop[i] = 1
            stable[0] += 1
            for j in range(1, 7):
                # 遍历一条边（有角的前提下）
                if board[cond1[i]+inc1[i] * j][cond2[i]+inc2[i] * j] != color:
                    break
                else:
                    stop[i] = j + 1
                    stable[1] += 1
    # 断了继续数
    for i in range(4):
        if board[cond1[i]][cond2[i]] == color:
            for j in range(1, 7-stop[i-1]):
                if board[cond1[i]-inc1[i-1] * j][cond2[i]-inc2[i-1] * j] != color:
                    break
                else:
                    stable[1] += 1
    colfull = np.zeros((8, 8), dtype=np.int)
    # 满列设为True
    colfull[:, np.sum(abs(board), axis=0) == 8] = True
    rowfull = np.zeros((8, 8), dtype=np.int)
    # 满行设为True
    rowfull[np.sum(abs(board), axis=1) == 8, :] = True
    diag1full = np.zeros((8, 8), dtype=np.int)
    # diag1full: 从左上到右下 15条对角线
    for i in range(15):
        diagsum = 0
        if i <= 7:
            sind1 = i
            sind2 = 0
            jrange = i + 1
        else:
            sind1 = 7
            sind2 = i - 7
            jrange = 15 - i
        for j in range(jrange):
            diagsum += abs(board[sind1 - j][sind2 + j])
        if diagsum == jrange:      # 若整个对角线全满
            for k in range(jrange):
                # 判定是否为己方颜色，满列和满行则无需判断，后面逻辑与会处理
                if board[sind1 - k][sind2 + k] == color:
                    diag1full[sind1 - k][sind2 + k] = True  # 对角线全设为True
    diag2full = np.zeros((8, 8), dtype=np.int)
    for i in range(15):
        diagsum = 0
        if i <= 7:
            sind1 = i
            sind2 = 7
            jrange = i + 1
        else:
            sind1 = 7
            sind2 = 14 - i
            jrange = 15 - i
        for j in range(jrange):
            diagsum += abs(board[sind1 - j][sind2 - j])
        if diagsum == jrange:
            for k in range(jrange):
                diag2full[sind1 - k][sind2 - k] = True
    stable[2] = sum(sum(np.logical_and(np.logical_and(np.logical_and(colfull, rowfull), diag1full), diag2full)))
    return stable

# 计算棋盘权重
def mapweightsum(board, mycolor):
    return sum(sum(board * Vmap)) * mycolor

class Minimax(object):
    """极大极小算法"""
    def __init__(self, color, stage):
        self.color = color
        self.stage = stage

    def minimax(self, board, depth, player, opponent,
                alfa=-INFINITY, beta=INFINITY):
        """递归调用，传入alpha, beta,返回score, bestchild"""
        best_child = board
        # 叶子节点或游戏结束时评估并返回, 评估函数传入real_player,而不是当前的player
        if board.game_ended():
            # 搜索到胜利或失败或平局直接返回分数
            whites, blacks, empty = board.count_stones()
            if whites > blacks:
                winner = WHITE
            elif blacks > whites:
                winner = BLACK
            else:
                winner = None
            if winner == self.color:
                return WINNER_SCORE, board
            elif winner == change_color(self.color):
                return -WINNER_SCORE, board
            else:
                return 0, board
        if depth == 0:
            return self.eval_score(board, self.color, change_color(self.color)), board
        if player == self.color:
            # 若是max层, 更新beta=min(child_alpha, child_beta, alpha)
            for child in board.next_states(player):
                score, _ = self.minimax(child, depth - 1, opponent, player, alfa, beta)
                if score > alfa:
                    alfa = score
                    best_child = child
                if beta <= alfa:
                    # 剪枝
                    return beta, best_child
            return alfa, best_child
        else:
            # 若是min层，更新beta=min(child_alpha, child_beta, beta)
            for child in board.next_states(player):
                score, _ = self.minimax(child, depth - 1, opponent, player, alfa, beta)
                if score < beta:
                    beta = score
                    best_child = child
                if beta <= alfa:
                    # 剪枝
                    return alfa, best_child
            return beta, best_child

    def eval_score(self, board, player, opponent):
        """
        估值函数为权值表+行动力+稳定子
        """
        moves = board.get_valid_moves(player)
        moves_ = board.get_valid_moves(opponent)
        if player == 2:
            player = -1
        brd = np.array(board.board)
        for i in range(8):
            for j in range(8):
                if brd[i][j] == 2:
                    brd[i][j] = -1
        stable = getstable(brd, player)
        map_value = mapweightsum(brd, player)
        mobility = len(moves) - len(moves_)
        # print(mobility)
        # print(stable)
        # print(board.board)
        # print(moves, moves_)
        # print(len(moves), len(moves_))
        if self.stage < 30:
            value = map_value + 20 * mobility + 10 * sum(stable)
        else:
            value = map_value + 15 * mobility + 15 * sum(stable)
        # print(value)
        return int(value)



