# /agent-data-scientist

Expert data scientist for ML and statistical analysis.

## Capabilities
- Exploratory data analysis
- Statistical modeling
- Machine learning
- Data visualization
- Feature engineering
- A/B testing

## EDA Template

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def eda_report(df):
    """Quick EDA report."""
    print("=== Shape ===")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    print("\n=== Data Types ===")
    print(df.dtypes)

    print("\n=== Missing Values ===")
    missing = df.isnull().sum()
    print(missing[missing > 0])

    print("\n=== Statistics ===")
    print(df.describe())

    print("\n=== Unique Values ===")
    for col in df.select_dtypes(include='object'):
        print(f"{col}: {df[col].nunique()}")

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Distribution
df['target'].hist(ax=axes[0, 0])
axes[0, 0].set_title('Target Distribution')

# Correlation heatmap
sns.heatmap(df.corr(), annot=True, ax=axes[0, 1])

# Box plots
df.boxplot(column='value', by='category', ax=axes[1, 0])

# Scatter
df.plot.scatter(x='feature1', y='feature2', c='target', ax=axes[1, 1])

plt.tight_layout()
plt.savefig('eda_report.png')
```

## ML Pipeline

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

# Cross-validation
scores = cross_val_score(pipeline, X_train, y_train, cv=5)
print(f"CV Score: {scores.mean():.3f} (+/- {scores.std():.3f})")

# Train and evaluate
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))
```
