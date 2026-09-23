import xgboost as xgb
import numpy as np

# Features:
# previous_day_sales, seven_day_average, day_of_week
X = np.array([
    [100, 105, 1],
    [110, 108, 2],
    [120, 112, 3],
    [130, 118, 4],
    [125, 121, 5],
    [150, 130, 6],
    [160, 140, 7],
    [140, 135, 1],
], dtype=float)

# Next-day sales
y = np.array([
    110,
    120,
    130,
    125,
    150,
    160,
    140,
    145,
], dtype=float)

dtrain = xgb.DMatrix(X, label=y)

params = {
    "objective": "reg:squarederror",
    "max_depth": 3,
    "eta": 0.3,
}

model = xgb.train(params, dtrain, num_boost_round=20)

model.save_model("models/forecasting/xgboost-model")

print("Forecasting model created successfully.")