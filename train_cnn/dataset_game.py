import torch
from torch.utils import data
import numpy as np

WALL = -1
WHITE = 0
EMPTY = 1
BLACK = 2
SIZE = 8

def numpy2tensor():
    X = np.load('X.npy')
    y = np.load('y.npy')
    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.long)
    torch.save([X, y], 'data')

def load_data(batch_size):
    """随即划分数据集并返回DataLoader数据生成器"""
    X, y = torch.load("data")
    dataset = data.TensorDataset(X, y)
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size],
                                                                generator=torch.Generator().manual_seed(42))
    return data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True), data.DataLoader(
        dataset=test_dataset, batch_size=batch_size, shuffle=False)

if __name__ == '__main__':
    # othello_data.get_learning_data()
    # numpy2tensor()
    X, y = torch.load("data")
    print(X.shape, y.shape)
    print(X[0:100], y[0:100])




