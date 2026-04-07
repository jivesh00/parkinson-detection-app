import os
# Remove old graphs
if os.path.exists("static/importance.png"):
    os.remove("static/importance.png")

if os.path.exists("static/prediction.png"):
    os.remove("static/prediction.png")

if os.path.exists("static/distribution.png"):
    os.remove("static/distribution.png")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import pickle
from xgboost import XGBClassifier

# Load dataset
data = pd.read_csv("dataset/parkinsons.csv")

X = data.drop("Target", axis=1)
y = data["Target"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train XGBoost model
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)

# GRAPH 1: Feature Importance
plt.figure(figsize=(6,4))
plt.bar(X.columns, model.feature_importances_)
plt.title("Feature Importance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("static/importance.png")
plt.close()

# GRAPH 2: Actual vs Predicted
plt.figure(figsize=(6,4))
plt.plot(list(y_test.values), label="Actual")
plt.plot(list(y_pred), label="Predicted")
plt.legend()
plt.title("Prediction Comparison")
plt.tight_layout()
plt.savefig("static/prediction.png")
plt.close()

# GRAPH 3: Dataset Distribution
plt.figure(figsize=(6,4))
data["Target"].value_counts().plot(kind="bar")
plt.title("Dataset Distribution")
plt.tight_layout()
plt.savefig("static/distribution.png")
plt.close()
# Save model
pickle.dump(model, open("model.pkl", "wb"))