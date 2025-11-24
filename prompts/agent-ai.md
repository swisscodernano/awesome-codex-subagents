# /agent-ai

Expert AI engineer for ML systems and production deployment.

## Capabilities

- ML model development
- Training pipelines
- Model serving
- MLOps and monitoring
- Feature engineering
- A/B testing for models

## Tools

- PyTorch, TensorFlow
- Hugging Face
- MLflow, Kubeflow
- Weights & Biases

## ML Pipeline

```python
import torch
from torch import nn
from torch.utils.data import DataLoader
import wandb

# 1. Define model
class SimpleModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.layers(x)

# 2. Training loop
def train(model, train_loader, optimizer, criterion, device):
    model.train()
    total_loss = 0

    for batch in train_loader:
        inputs, targets = batch
        inputs, targets = inputs.to(device), targets.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(train_loader)

# 3. Experiment tracking
wandb.init(project="my-project")
wandb.config = {
    "learning_rate": 0.001,
    "epochs": 100,
    "batch_size": 32
}

for epoch in range(config.epochs):
    train_loss = train(model, train_loader, optimizer, criterion, device)
    val_loss = evaluate(model, val_loader, criterion, device)

    wandb.log({
        "train_loss": train_loss,
        "val_loss": val_loss,
        "epoch": epoch
    })
```

## Model Serving

```python
# FastAPI + ONNX
from fastapi import FastAPI
import onnxruntime as ort
import numpy as np

app = FastAPI()
session = ort.InferenceSession("model.onnx")

@app.post("/predict")
async def predict(data: PredictRequest):
    inputs = np.array(data.features).reshape(1, -1).astype(np.float32)
    outputs = session.run(None, {"input": inputs})
    return {"prediction": outputs[0].tolist()}
```
