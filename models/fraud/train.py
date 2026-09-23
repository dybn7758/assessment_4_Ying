import xgboost as xgb
import numpy as np

# Features:
# amount, transaction_count, account_age_days
X = np.array([
    [100, 2, 1000],
    [250, 3, 700],
    [500, 5, 500],
    [1000, 8, 300],
    [3000, 12, 200],
    [5000, 20, 100],
    [7500, 25, 50],
    [10000, 30, 20],
], dtype=float)

# 0 = legitimate, 1 = fraud
y = np.array([0, 0, 0, 0, 0, 1, 1, 1])

dtrain = xgb.DMatrix(X, label=y)

params = {
    "objective": "binary:logistic",
    "max_depth": 3,
    "eta": 0.3,
    "eval_metric": "logloss",
}

model = xgb.train(params, dtrain, num_boost_round=20)

model.save_model("models/fraud/xgboost-model")

print("Fraud model created successfully.")