"""Utilities that help with training neural networks."""

from tqdm import tqdm

import torch
from torch import nn
from torch.nn.modules.loss import CrossEntropyLoss
from torch.optim import Optimizer
from torch.utils.data import DataLoader


def fit(device: str, dataloader: DataLoader[torch.Tensor], model: nn.Module,
        loss_fn: CrossEntropyLoss, optimizer: Optimizer) -> tuple[float, float]:
    """
    Trains the given model for a single epoch.
    """
    loss_sum = 0.0
    correct_item_count = 0
    item_count = 0

    model.to(device)
    model.train()

    for (x, y) in tqdm(dataloader):
        x = x.float().to(device)
        y = y.long().to(device)

        (y_prime, loss) = _fit_one_batch(x, y, model, loss_fn, optimizer)

        correct_item_count += (y_prime.argmax(1) == y).sum().item()
        loss_sum += loss.item()
        item_count += len(x)

    average_loss = loss_sum / item_count
    accuracy = correct_item_count / item_count

    return (average_loss, accuracy)


def _fit_one_batch(x: torch.Tensor, y: torch.Tensor, model: nn.Module,
                   loss_fn: CrossEntropyLoss,
                   optimizer: Optimizer) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Trains a single minibatch (backpropagation algorithm).
    """
    y_prime = model(x)
    loss = loss_fn(y_prime, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return (y_prime, loss)


def evaluate(device: str, dataloader: DataLoader[torch.Tensor],
             model: nn.Module,
             loss_fn: CrossEntropyLoss) -> tuple[float, float]:
    """
    Evaluates the given model for the whole dataset once.
    """
    loss_sum = 0.0
    correct_item_count = 0
    item_count = 0

    model.to(device)
    model.eval()

    with torch.no_grad():
        for (x, y) in dataloader:
            x = x.float().to(device)
            y = y.long().to(device)

            (y_prime, loss) = _evaluate_one_batch(x, y, model, loss_fn)

            correct_item_count += (y_prime.argmax(1) == y).sum().item()
            loss_sum += loss.item()
            item_count += len(x)

        average_loss = loss_sum / item_count
        accuracy = correct_item_count / item_count

    return (average_loss, accuracy)


def _evaluate_one_batch(
        x: torch.Tensor, y: torch.Tensor, model: nn.Module,
        loss_fn: CrossEntropyLoss) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Evaluates a single minibatch.
    """
    with torch.no_grad():
        y_prime = model(x)
        loss = loss_fn(y_prime, y)

    return (y_prime, loss)
