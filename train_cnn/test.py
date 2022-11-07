import torch
from model import CNN
net = CNN()
net.load_state_dict(torch.load('cnn.params'))
X_1 = torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 1., 0., 0., 0.],
                    [0., 0., 0., 1., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 0., 0., 0., 0.]], dtype=torch.float32)
X_2 = torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 1., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 1., 0., 0., 0.],
                    [0., 0., 0., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 0., 0., 0., 0.],
                    [0., 0., 0., 0., 0., 0., 0., 0.]], dtype=torch.float32)
X = torch.stack((X_1, X_2), dim=0)
X = torch.unsqueeze(X, dim=0)
y = net(X)
print(y.shape)
# y_predict = torch.argmax(y, dim=1)
# x = torch.argmax(y, dim=1).item()
# y[0, x] = 0
y = torch.squeeze(y, dim=0)
y_predict = torch.argmax(y, dim=0)
row, column = (y_predict.item() // 8, y_predict.item() % 8)
print(row, column)
