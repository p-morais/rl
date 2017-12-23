import math

import torch
import torch.nn as nn
from torch.autograd import Variable


class DiagonalGaussian(nn.Module):
    def __init__(self, num_outputs, init_std=1):
        super(DiagonalGaussian, self).__init__()

        self.logstd = nn.Parameter(
            torch.ones(1, num_outputs) * math.log(init_std)
        )

    def forward(self, x):
        mean = x

        std = self.logstd.exp()
        
        return mean, std

    def sample(self, x, deterministic):
        if deterministic is False:
            action = self.evaluate(x).sample()
        else:
            action, _ = self(x)

        return action

    def evaluate(self, x):
        mean, std = self(x)
        return torch.distributions.Normal(mean, std)
