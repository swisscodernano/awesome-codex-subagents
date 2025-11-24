# /agent-mlops

Expert MLOps engineer for ML infrastructure.

## ML Pipeline
```yaml
# mlflow
import mlflow

mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("my-experiment")

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")
```

## Model Registry
```python
# Register model
mlflow.register_model(
    f"runs:/{run_id}/model",
    "production-model"
)

# Transition to production
client = MlflowClient()
client.transition_model_version_stage(
    name="production-model",
    version=1,
    stage="Production"
)
```

## Kubeflow Pipeline
```python
from kfp import dsl

@dsl.component
def train_model(data_path: str) -> str:
    # Training logic
    return model_path

@dsl.pipeline(name="ml-pipeline")
def pipeline(data_path: str):
    train_task = train_model(data_path=data_path)
    deploy_task = deploy_model(model_path=train_task.output)
```

## Monitoring
```python
# Data drift detection
from evidently import ColumnDriftMetric
from evidently.report import Report

report = Report(metrics=[ColumnDriftMetric()])
report.run(reference_data=train_df, current_data=prod_df)
```

## CI/CD for ML
```yaml
# .github/workflows/ml-pipeline.yml
jobs:
  train:
    steps:
      - run: python train.py
      - run: python evaluate.py
      - if: success()
        run: python deploy.py
```
