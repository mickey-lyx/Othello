from __future__ import division
import struct
import glob
import os
import numpy as np
import othello_simulate

WALL = -1
WHITE = 0
EMPTY = 1
BLACK = 2
SIZE = 8


def read_wthor(file_name):
    with open(file_name, mode='rb') as f:
        header = struct.unpack("<BBBBIHHBBBB", f.read(16))
        games = header[4]
        year = header[6]
        board_size = header[7]
        assert board_size == 0 or board_size == 8

        for i in range(games):
            game_info = struct.unpack("<HHHBB", f.read(8))
            true_score = game_info[3]
            moves = struct.unpack('<' + 'B' * 60, f.read(60))
            yield true_score, moves


def read_all(path):
    """生成器，获取对局move信息"""
    for wtb in glob.glob(os.path.join(path, '*.wtb')):
        for true_score, moves in read_wthor(wtb):
            yield true_score, moves


def get_learning_data(path='wthor_data'):
    """获取训练数据"""
    games = read_all(path)
    l_X = []
    l_y = []
    for i, (true_score, moves) in enumerate(games):
        if i % 1000 == 0:
            print(i)
        for board, player, move in moves2data(true_score, moves):
            if player == WHITE:
                board = othello_simulate.inverted(board)
            channel1 = np.expand_dims(np.maximum(board - 1, 0), axis=0)
            channel2 = np.expand_dims(np.maximum(-board + 1, 0), axis=0)
            channel = np.concatenate((channel1, channel2), axis=0)
            l_X.append(channel)
            row, column = othello_simulate.decode_move(move)
            y = (row - 1) * SIZE + column - 1
            l_y.append(y)
    X = np.array(l_X)
    y = np.array(l_y)
    np.save('X', X)
    np.save('y', y)


def moves2data(true_score, moves):
    """对局信息转换为棋盘和移动数据（通过模拟下棋）"""
    board = othello_simulate.new_board()
    player = othello_simulate.BLACK
    for i in range(len(moves) - 1):
        if moves[i] == 0:
            assert moves[i + 1] == 0

    moves = [m for m in moves if m != 0]
    for move in moves:
        row, col = othello_simulate.decode_move(move)
        if not othello_simulate.is_valid_move(board, (row, col), player):
            player = othello_simulate.opponent(player)
            assert othello_simulate.is_valid_move(board, (row, col), player)
        yield board[1:-1, 1:-1], player, move
        othello_simulate.make_move(board, (row, col), player)
        player = othello_simulate.opponent(player)
