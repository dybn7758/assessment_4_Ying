import xgboost as xgb
import numpy as np

# Features:
# user_id, product_id, user_activity_score
X = np.array([
    [1, 101, 2],
    [1, 102, 4],
    [2, 101, 3],
    [2, 103, 7],
    [3, 102, 5],
    [3, 104, 8],
    [4, 103, 6],
    [4, 105, 9],
], dtype=float)

# Recommendation score
y = np.array([
    0.1,
    0.3,
    0.2,
    0.7,
    0.5,
    0.8,
    0.6,
    0.9,
])

dtrain = xgb.DMatrix(X, label=y)

params = {
    "objective": "reg:squarederror",
    "max_depth": 3,
    "eta": 0.3,
}

model = xgb.train(params, dtrain, num_boost_round=20)

model.save_model("models/recommendations/xgboost-model")

print("Recommendations model created successfully.")