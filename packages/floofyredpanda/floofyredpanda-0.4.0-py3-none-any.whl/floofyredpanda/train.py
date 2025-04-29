import os
import torch
from torch import nn as nn_module
from torch.utils.data import TensorDataset, DataLoader
from .nn import _raw_to_tensor


def train(
        raw_inputs,
        raw_outputs,
        layers=None,  # Now optional
        activation='relu',
        lr=1e-3,
        epochs=10,
        batch_size=32,
        device=None,
        model=None  # <-- NEW
):
    """
    Train a simple feed-forward net on any inputs/outputs.

    args:
      raw_inputs:  list of numbers, lists, file-paths, bytes…
      raw_outputs: list of same length, matching targets
      layers:      list of hidden layer sizes, e.g. [64,32]
      activation:  'relu' or 'tanh'
      lr:          learning rate
      epochs:      epochs to train
      batch_size:  batch size
      device:      'cpu' or 'cuda'; defaults to cpu
      model:       existing model to continue training (optional)

    returns:
      a trained torch.nn.Module
    """

    if len(raw_inputs) != len(raw_outputs):
        raise ValueError("raw_inputs and raw_outputs must be same length")

    if device:
        device = device
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    # convert & flatten
    X = [_raw_to_tensor(x).flatten() for x in raw_inputs]
    Y = [_raw_to_tensor(y).flatten() for y in raw_outputs]

    X = torch.stack(X).to(device)
    Y = torch.stack(Y).to(device)

    in_dim, out_dim = X.size(1), Y.size(1)

    if model is None:
        # Must build a new model
        if layers is None:
            raise ValueError("If no model is provided, 'layers' must be specified.")

        dims = [in_dim] + layers + [out_dim]

        seq = []
        act_fn = nn_module.ReLU if activation == 'relu' else nn_module.Tanh
        for i in range(len(dims) - 1):
            seq.append(nn_module.Linear(dims[i], dims[i + 1]))
            if i < len(dims) - 2:
                seq.append(act_fn())

        model = nn_module.Sequential(*seq).to(device)
    else:
        model = model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn_module.MSELoss()

    loader = DataLoader(TensorDataset(X, Y), batch_size=batch_size, shuffle=True)

    model.train()
    for epoch in range(1, epochs + 1):
        total = 0.0
        for xb, yb in loader:
            optimizer.zero_grad()
            pred = model(xb)
            loss = criterion(pred, yb)
            loss.backward()
            optimizer.step()
            total += loss.item() * xb.size(0)
        avg = total / len(loader.dataset)
        print(f"epoch {epoch}/{epochs} – loss: {avg:.4f}")

    return model
