import os
import torch
import torch.nn as nn
import torch.nn.functional as F

class LocalizationNetwork(nn.Module):
    def __init__(self):
        super(LocalizationNetwork, self).__init__()
        self.localization = nn.Sequential(
            nn.Conv2d(1024,64,kernel_size=1),
            nn.Conv2d(64, 8, kernel_size=7),
            nn.MaxPool2d(2, stride=2),
            nn.ReLU(True),
            nn.Conv2d(8, 10, kernel_size=5),
            nn.MaxPool2d(2, stride=2),
            nn.ReLU(True)
        )

        self.fc_loc = nn.Sequential(
            nn.Linear(10 * 3 * 3, 32),
            nn.ReLU(True),
            nn.Linear(32, 3 * 2)
        )

    def forward(self, x):
        xs = self.localization(x)
        xs = xs.view(-1, 10 * 3 * 3)
        theta = self.fc_loc(xs)
        theta = theta.view(-1, 2, 3)
        return theta
    
    def parameters(self):
        return super(LocalizationNetwork, self).parameters()

    def train(self, mode=True):
        super(LocalizationNetwork, self).train(mode)
