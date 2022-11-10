from minimax import Minimax
from model import CNN
from net_predict import net_predictor
import torch
from config import BLACK, WHITE, INFINITY
import time
import numpy as np
# function()   执行的程序
# time_end = time.clock()  # 记录结束时间
# time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
# print(time_sum)


def change_color(color):
    if color == BLACK:
        return WHITE
    else:
        return BLACK


class Player(object):
    def __init__(self, color):
        self.color = color

    def get_move(self):
        raise NotImplementedError

    def get_current_board(self, board):
        raise NotImplementedError


class Human(Player):
    """人类玩家获取鼠标点击"""

    def __init__(self, gui, color="black"):
        super().__init__(color)
        self.gui = gui

    def get_move(self):
        validMoves = self.current_board.get_valid_moves(self.color)
        while True:
            move = self.gui.get_mouse_input()
            if move in validMoves:
                break
        self.current_board.apply_move(move, self.color)
        return 0, self.current_board

    def get_current_board(self, board):
        self.current_board = board


class Computer(Player):
    """Minimax算法电脑玩家"""

    def __init__(self, color, level):
        super().__init__(color)
        self.level = level
        # self.time = []

    def get_current_board(self, board):
        self.current_board = board

    def get_move(self):
        whites, blacks, empty = self.current_board.count_stones()
        stage = whites + blacks
        # 自适应深度：前期后期选择较少，设置深度较高，游戏中期选择多，设定深度较低, 最后期直接搜到游戏结束
        ''' easy: level == 1 
            medium: level == 2
            hard: level == 3
        '''
        if stage <= 9:
            depth = self.level + 4
        elif stage >= 45 and stage < 52:
            depth = self.level + 4
        elif stage >= 52:
            # 搜到游戏结束
            depth = INFINITY
        else:
            depth = self.level + 3
        # time_start = time.perf_counter()
        self.minimaxObj = Minimax(self.color, stage)
        score, board = self.minimaxObj.minimax(self.current_board, depth,
                                               self.color, change_color(self.color))
        # time_end = time.perf_counter()  # 记录结束时间
        # time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
        # self.time.append(time_sum)
        # print(np.mean(self.time))
        return score, board


class AI(Player):
    """CNN训练的AI"""

    def __init__(self, color):
        super().__init__(color)
        self.net = CNN()
        # 导入模型参数
        self.net.load_state_dict(torch.load('cnn.params'))
        self.predictor = net_predictor()
        # self.time = []

    def get_current_board(self, board):
        self.current_board = board

    def get_move(self):
        # start_time = time.perf_counter()
        row, column, flag = self.predictor.predict(self.net, self.color, self.current_board)
        # print(row, column)
        self.current_board.apply_move((row, column), self.color)
        # end_time = time.perf_counter()
        # sum_time = end_time - start_time
        # self.time.append(sum_time)
        # print(f'CNN_time: {np.mean(self.time)}')
        return 0, self.current_board


class Combination(Player):
    """Minimax结合深度神经网络"""

    def __init__(self, color, level):
        super().__init__(color)
        self.net = CNN()
        self.net.load_state_dict(torch.load('cnn.params'))
        self.predictor = net_predictor()
        self.assist = Computer(color, level)
        # 转换阈值prob，当最大的softmax概率输出小于prob时，将控制权转交minimax算法
        self.prob = 0.5
        # self.time = []
    def get_current_board(self, board):
        self.current_board = board

    def get_move(self):
        # start_time = time.perf_counter()
        row, column, flag = self.predictor.predict(self.net, self.color, self.current_board, self.prob)
        # print(row, column)
        # flag用于记录是否使用minimax
        if flag == False:
            self.current_board.apply_move((row, column), self.color)
            # end_time = time.perf_counter()
            # sum_time = end_time - start_time
            # self.time.append(sum_time)
            # print(f'Combination_time: {np.mean(self.time)}')
            return 0, self.current_board
        else:
            # 调用minimax算法辅助
            Computer.current_board = self.current_board
            score, board = self.assist.get_move()
            # end_time = time.perf_counter()
            # sum_time = end_time - start_time
            # self.time.append(sum_time)
            # print(f'Combination_time: {np.mean(self.time)}')
            return score, board
