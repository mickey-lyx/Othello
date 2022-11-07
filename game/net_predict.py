import torch
from config import BLACK
import torch.nn.functional as F

class net_predictor():
    def __init__(self):
        pass
    def predict(self, net, color, board, prob=0):
        """
        基于CNN的预测
        输入棋盘双通道数据，经过CNN前向传播给出下一步预测
        """
        board_tmp = torch.tensor(board.board, dtype=torch.float32)
        dim0, dim1 = board_tmp.shape
        X_1 = board_tmp
        X_2 = board_tmp.clone()

        for i in range(dim0):
            for j in range(dim1):
                if X_1[i, j] == 2:
                     X_1[i, j] = 0
        for i in range(dim0):
            for j in range(dim1):
                if X_2[i, j] == 1:
                    X_2[i, j] = 0
                elif X_2[i, j] == 2:
                    X_2[i, j] = 1
        if color == BLACK:
            X = torch.stack((X_1, X_2), dim=0)
        else:
            X = torch.stack((X_2, X_1), dim=0)
        X = torch.unsqueeze(X, dim=0)
        y = F.softmax(net(X), dim=1)
        y = torch.squeeze(y, dim=0)
        valid_moves = board.get_valid_moves(color)
        flag = False

        # 首个预测是否在valid move中？
        y_max, y_predict = torch.max(y, dim=0)
        row, column = (y_predict.item() // 8, y_predict.item() % 8)

        # 若不在valid move中或者softmax输出概率小于prob，则交给minimax算法
        if (row, column) not in valid_moves or y_max.item() < prob:
            flag = True
        for i in range(y.shape[0]):
            row, column = (i // 8, i % 8)
            if (row, column) not in valid_moves:
                y[i] = 0
        y_max, y_predict = torch.max(y, dim=0)
        # print(y_max)
        row, column = (y_predict.item() // 8, y_predict.item() % 8)
        return row, column, flag


