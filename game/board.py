
""" Othello游戏规则和主要逻辑 """

from config import WHITE, BLACK, EMPTY
from copy import deepcopy

class Board:
    """ 游戏规则设定 """
    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]     #以列表的形式初始化一个8*8的棋盘对象
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[3][3] = WHITE
        self.board[4][4] = WHITE                    #设置棋盘中心四个点的棋子
        self.valid_moves = []                       #创建一个有效落子的对象

    def __getitem__(self, i, j):
        return self.board[i][j]                     #返回棋盘上一个位置

    def lookup(self, row, column, color):
        """ 寻找已知放置位置和颜色的棋子在棋盘8个方向上可以放置一个相同颜色棋子的可能空位
        已知棋子必须与该空位处于同一水平、垂直或对角直线上，且中间已有连续放置的与其颜色相反的棋子 """
        if color == BLACK:
            other = WHITE
        else:
            other = BLACK
        places = []
        if row < 0 or row > 7 or column < 0 or column > 7:
            return places                       #规定查找范围不能超过棋盘大小
        # 每一个方向都进行遍历搜索，共8个方向
        for (x, y) in [
                (-1, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
                (1, 0),
                (1, -1),
                (0, -1),
                (-1, -1)]:
            pos = self.check_direction(row, column, x, y, other)
            if pos:
                places.append(pos)              #若某个方向存在可以放置的空位，将其位置加入列表
        return places

    def check_direction(self, row, column, row_add, column_add, other_color):
        """ 检查特定方向上是否存在相同颜色的棋子 """
        i = row + row_add
        j = column + column_add                 #设定某个探索方向
        if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other_color):
            i += row_add
            j += column_add                     #若选定方向的第一个即为相同颜色的棋子则直接停止，否则继续搜索
            while (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other_color):
                i += row_add
                j += column_add
            if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == EMPTY):
                return (i, j)                   #直到该方向的直线出现空位，搜索停止

    def get_valid_moves(self, color):
        """ 获取某一给定颜色的棋子在棋盘上所有可以落子的位置。
        我们将搜索该棋盘上所有与给定颜色相同棋子所有方向可以放置的空位。
        必须在apply_move之前调用该函数。
        """
        if color == BLACK:
            other = WHITE
        else:
            other = BLACK
        places = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color:
                    #调用lookup函数寻找各个方向上可以落子的空位
                    places = places + self.lookup(i, j, color)
        places = list(set(places))      #对place列表去重并按从小到大排序
        self.valid_moves = places
        return places

    def apply_move(self, move, color):
        """ 判断get_valid_moves中获取的位置是否合法
        """
        if move in self.valid_moves:
            self.board[move[0]][move[1]] = color
            for i in range(1, 9):
                self.flip(i, move, color)   #调用flip函数实现每个方向“吃子”

    def flip(self, direction, position, color):
        """ 将两个处于同一直线且颜色相同的棋子之间的颜色不同的棋子的颜色翻转 """
        if direction == 1:
            # 南方向
            row_inc = -1
            col_inc = 0
        elif direction == 2:
            # 东南方向
            row_inc = -1
            col_inc = 1
        elif direction == 3:
            # 东方向
            row_inc = 0
            col_inc = 1
        elif direction == 4:
            # 东北方向
            row_inc = 1
            col_inc = 1
        elif direction == 5:
            # 北方向
            row_inc = 1
            col_inc = 0
        elif direction == 6:
            # 西北方向
            row_inc = 1
            col_inc = -1
        elif direction == 7:
            # 西方向
            row_inc = 0
            col_inc = -1
        elif direction == 8:
            # 西南方向
            row_inc = -1
            col_inc = -1

        places = []     # 需要翻转的位置
        i = position[0] + row_inc
        j = position[1] + col_inc

        if color == WHITE:
            other = BLACK
        else:
            other = WHITE

        if i in range(8) and j in range(8) and self.board[i][j] == other:
            # 确保至少要有一个棋子翻转
            places = places + [(i, j)]
            i = i + row_inc
            j = j + col_inc
            while i in range(8) and j in range(8) and self.board[i][j] == other:
                # 寻找更多需要翻转的棋子
                places = places + [(i, j)]
                i = i + row_inc
                j = j + col_inc
            if i in range(8) and j in range(8) and self.board[i][j] == color:
                # 找到需要翻转的棋子的终点
                for pos in places:
                    self.board[pos[0]][pos[1]] = color

    def get_changes(self):
        """ 对两种棋子的颜色计数 """
        whites, blacks, empty = self.count_stones()
        return (self.board, blacks, whites)

    def game_ended(self):
        """ 设置游戏终止条件 """
        # 棋盘上没有空位或黑子白子中有一方数量归零则结束
        whites, blacks, empty = self.count_stones()
        if whites == 0 or blacks == 0 or empty == 0:
            return True

        # 黑子和白子均没有可以继续落子的地方也会结束
        if self.get_valid_moves(BLACK) == [] and \
        self.get_valid_moves(WHITE) == []:
            return True
        return False

    def print_board(self):
        """ 绘制棋盘 """
        for i in range(8):
            print(i, ' |', end=' ')
            for j in range(8):
                if self.board[i][j] == BLACK:
                    print('B', end=' ')
                elif self.board[i][j] == WHITE:
                    print('W', end=' ')
                else:
                    print(' ', end=' ')
                print('|', end=' ')
            print()

    def count_stones(self):
        """ 统计棋盘中所有黑子和白子以及空位的数量
        """
        whites = 0
        blacks = 0
        empty = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == WHITE:
                    whites += 1
                elif self.board[i][j] == BLACK:
                    blacks += 1
                else:
                    empty += 1
        return whites, blacks, empty

    def compare(self, otherBoard):
        """返回一个只包含那些在一些棋盘上为空而其他棋盘上不为空的位置的棋盘
        """
        diffBoard = Board()
        diffBoard.board[3][4] = 0
        diffBoard.board[3][3] = 0
        diffBoard.board[4][3] = 0
        diffBoard.board[4][4] = 0
        for i in range(8):
            for j in range(8):
                if otherBoard.board[i][j] != self.board[i][j]:
                    diffBoard.board[i][j] = otherBoard.board[i][j]
        return otherBoard

    def get_adjacent_count(self, color):
        """ 统计某个特定的棋子旁边有多少个空位 """
        adjCount = 0
        for x, y in [(a, b) for a in range(8) for b in range(8) if self.board[a][b] == color]:
            for i, j in [(a, b) for a in [-1, 0, 1] for b in [-1, 0, 1]]:
                if 0 <= x + i <= 7 and 0 <= y + j <= 7:
                    if self.board[x + i][y + j] == EMPTY:
                        adjCount += 1
        return adjCount

    def next_states(self, color):
        """给定一个玩家的颜色，返回该玩家可以落子的所有地方所产生的棋盘。该棋盘将用于AI算法迭代预测。
        """
        valid_moves = self.get_valid_moves(color)
        for move in valid_moves:
            newBoard = deepcopy(self)   #深复制完全独立出棋盘
            newBoard.apply_move(move, color)
            yield newBoard
