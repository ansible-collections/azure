"""Neural network class."""

import torch
from torch import nn


class NeuralNetwork(nn.Module):
    """
    Neural network that classifies Fashion MNIST-style images.
    """

    def __init__(self) -> None:
        super().__init__()
        self.sequence = nn.Sequential(nn.Flatten(), nn.Linear(28 * 28, 20),
                                      nn.ReLU(), nn.Linear(20, 10))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y_prime = self.sequence(x)
        return y_prime
